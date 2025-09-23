#!/usr/bin/env python3
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple

# Shared tolerant JSON loader
_LINE_COMMENT_RE = re.compile(r"(^|\s)//.*?$", re.MULTILINE)
_BLOCK_COMMENT_RE = re.compile(r"/\*.*?\*/", re.DOTALL)

def strip_json_comments(text: str) -> str:
    text = _BLOCK_COMMENT_RE.sub("", text)
    text = _LINE_COMMENT_RE.sub("", text)
    return text

def load_json_tolerant(path: Path) -> Any:
    raw = path.read_text(encoding="utf-8")
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return json.loads(strip_json_comments(raw))

def iter_dicts(obj: Any) -> Iterable[Dict[str, Any]]:
    if isinstance(obj, dict):
        yield obj
        for v in obj.values():
            yield from iter_dicts(v)
    elif isinstance(obj, list):
        for it in obj:
            yield from iter_dicts(it)

ID_KEYS_PRIORITY = [
    "control_id", "id", "rule_id", "section_id", "number", "controlId", "check_id", "recommendation_id"
]

def find_id(d: Dict[str, Any]) -> Optional[str]:
    for k in ID_KEYS_PRIORITY:
        if k in d and isinstance(d[k], (str, int)):
            return str(d[k])
    for key in ("rule", "recommendation", "control"):
        v = d.get(key)
        if isinstance(v, dict):
            for k in ID_KEYS_PRIORITY:
                if k in v and isinstance(v[k], (str, int)):
                    return str(v[k])
    return None


def build_duplicate_map(base_dir: Path) -> Dict[str, str]:
    mapping_file = base_dir / "etl-job_mapping _final_fn_name_generator" / "fn_list_finalisation" / "aws" / "complete_fn_list" / "all_duplicates_min.json"
    if not mapping_file.exists():
        return {}
    try:
        data = load_json_tolerant(mapping_file)
    except Exception:
        return {}
    m: Dict[str, str] = {}
    if isinstance(data, list):
        for entry in data:
            if isinstance(entry, dict):
                repl = entry.get("replacement_function")
                for dup in entry.get("duplicates") or []:
                    if isinstance(dup, str) and repl and dup and dup != repl:
                        m[dup] = repl
    return m


def normalize_functions(fns: List[Any], dup_map: Dict[str, str]) -> List[str]:
    out: List[str] = []
    seen: Set[str] = set()
    for fn in fns:
        if not isinstance(fn, str):
            continue
        name = dup_map.get(fn, fn)
        if name not in seen:
            seen.add(name)
            out.append(name)
    return out


def service_from_function(fn: str) -> str:
    if "_" in fn:
        return fn.split("_", 1)[0]
    return fn


def main(argv: List[str]) -> int:
    script_path = Path(__file__).resolve()
    base_dir = script_path.parents[2]
    aws_root = base_dir / "final_complaince_database_with_fn_name" / "aws_function_complaince_mapping"
    if not aws_root.exists():
        print(f"AWS folder not found: {aws_root}", file=sys.stderr)
        return 2

    dup_map = build_duplicate_map(base_dir)

    files: List[Path] = []
    for dirpath, _, filenames in os.walk(aws_root):
        for fn in filenames:
            if not fn.lower().endswith(".json"):
                continue
            if fn.lower().endswith(".json.bak") or fn.lower().endswith(".bak.json"):
                continue
            p = Path(dirpath) / fn
            # Skip our outputs if present
            if p.name in {"aws_combined_control_functions.json", "aws_function_names_unique.json", "aws_compliance_to_functions.json", "aws_coverage_report.json"}:
                continue
            files.append(p)

    # Coverage counters
    coverage: Dict[str, Dict[str, int]] = {}
    # compliance -> set(functions)
    compliance_functions: Dict[str, Set[str]] = {}
    # Global unique functions
    unique_functions: Set[str] = set()

    for fp in files:
        try:
            data = load_json_tolerant(fp)
        except Exception:
            continue
        # compliance name is top-level directory under aws_root
        rel = fp.relative_to(aws_root)
        compliance = rel.parts[0] if len(rel.parts) > 1 else fp.stem

        cov = coverage.setdefault(compliance, {"files": 0, "nodes_with_fn_key": 0, "nodes_with_non_empty_fns": 0, "nodes_with_empty_fns": 0})
        cov["files"] += 1

        for d in iter_dicts(data):
            if "function_names" in d and isinstance(d["function_names"], list):
                cov["nodes_with_fn_key"] += 1
                norm = normalize_functions(d["function_names"], dup_map)
                if len(norm) > 0:
                    cov["nodes_with_non_empty_fns"] += 1
                    compliance_functions.setdefault(compliance, set()).update(norm)
                    unique_functions.update(norm)
                else:
                    cov["nodes_with_empty_fns"] += 1

    # Load combined file to verify consistency
    combined_path = aws_root / "aws_combined_control_functions.json"
    combined_ok = False
    combined_items: List[Dict[str, Any]] = []
    if combined_path.exists():
        try:
            combined_items = load_json_tolerant(combined_path)
            if isinstance(combined_items, list):
                combined_ok = True
        except Exception:
            combined_ok = False

    # If invalid, attempt regenerating by invoking the index builder
    if not combined_ok:
        from subprocess import run
        builder = base_dir / "etl-job_mapping _final_fn_name_generator" / "ai_function" / "build_aws_combined_functions_index.py"
        run([sys.executable, str(builder)], check=False)
        try:
            combined_items = load_json_tolerant(combined_path)
            combined_ok = isinstance(combined_items, list)
        except Exception:
            combined_ok = False

    # Write outputs
    (aws_root / "aws_function_names_unique.json").write_text(
        json.dumps(sorted(unique_functions), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    compliance_functions_out = [
        {"compliance": comp, "function_names": sorted(fns)}
        for comp, fns in sorted(compliance_functions.items(), key=lambda kv: kv[0].lower())
    ]
    (aws_root / "aws_compliance_to_functions.json").write_text(
        json.dumps(compliance_functions_out, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    # Coverage report JSON
    coverage_out = {
        "files_scanned": len(files),
        "compliances": coverage,
        "unique_functions_count": len(unique_functions),
        "combined_file_valid": combined_ok,
        "outputs": {
            "combined": str(combined_path),
            "unique_functions": str(aws_root / "aws_function_names_unique.json"),
            "compliance_to_functions": str(aws_root / "aws_compliance_to_functions.json"),
        },
    }
    (aws_root / "aws_coverage_report.json").write_text(
        json.dumps(coverage_out, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print(f"Files scanned: {coverage_out['files_scanned']}")
    print(f"Compliances found: {len(coverage)}")
    print(f"Unique functions: {coverage_out['unique_functions_count']}")
    print(f"Combined file valid: {combined_ok}")
    print("Wrote:")
    for k, v in coverage_out["outputs"].items():
        print(f"- {k}: {v}")
    print(f"- coverage: {aws_root / 'aws_coverage_report.json'}")

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
