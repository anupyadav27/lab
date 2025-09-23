#!/usr/bin/env python3
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple

# Tolerant JSON loader (handles // and /* */ comments)
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
        stripped = strip_json_comments(raw)
        return json.loads(stripped)


ID_KEYS_PRIORITY = [
    "control_id", "id", "rule_id", "section_id", "number", "controlId", "check_id", "recommendation_id"
]


def find_id(d: Dict[str, Any]) -> Optional[str]:
    for k in ID_KEYS_PRIORITY:
        if k in d and isinstance(d[k], (str, int)):
            return str(d[k])
    # Some CIS files might use nested id under "rule" or similar
    for key in ("rule", "recommendation", "control"):
        v = d.get(key)
        if isinstance(v, dict):
            for k in ID_KEYS_PRIORITY:
                if k in v and isinstance(v[k], (str, int)):
                    return str(v[k])
    return None


def iter_dicts_with_functions(obj: Any) -> Iterable[Dict[str, Any]]:
    # Yield dicts that contain a function_names list
    if isinstance(obj, dict):
        if "function_names" in obj and isinstance(obj["function_names"], list):
            yield obj
        for v in obj.values():
            yield from iter_dicts_with_functions(v)
    elif isinstance(obj, list):
        for item in obj:
            yield from iter_dicts_with_functions(item)


def build_duplicate_map(base_dir: Path) -> Dict[str, str]:
    mapping_file = base_dir / "etl-job_mapping _final_fn_name_generator" / "fn_list_finalisation" / "aws" / "complete_fn_list" / "all_duplicates_min.json"
    if not mapping_file.exists():
        return {}
    try:
        data = load_json_tolerant(mapping_file)
    except Exception:
        return {}
    m = {}
    if isinstance(data, list):
        for entry in data:
            if not isinstance(entry, dict):
                continue
            repl = entry.get("replacement_function")
            dups = entry.get("duplicates") or []
            if not repl:
                continue
            for dup in dups:
                if isinstance(dup, str) and dup and dup != repl:
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


def derive_compliance_name(aws_root: Path, file_path: Path) -> str:
    rel = file_path.relative_to(aws_root)
    parts = rel.parts
    if len(parts) > 1:
        # First folder beneath aws_root
        return parts[0]
    # Fallback to filename stem
    return file_path.stem


def collect_entries_from_file(aws_root: Path, file_path: Path, dup_map: Dict[str, str]) -> List[Tuple[str, str, List[str]]]:
    try:
        data = load_json_tolerant(file_path)
    except Exception:
        return []
    compliance = derive_compliance_name(aws_root, file_path)

    entries: List[Tuple[str, str, List[str]]] = []
    for d in iter_dicts_with_functions(data):
        fns = d.get("function_names")
        if not isinstance(fns, list) or len(fns) == 0:
            continue
        id_val = find_id(d)
        # If not found directly, sometimes parent carries id; attempt simple fallback
        if not id_val:
            title = d.get("title") or d.get("control_name") or d.get("name")
            if isinstance(title, str) and title:
                id_val = title
            else:
                # Last resort: synthesis based on file and ordinal
                id_val = f"{file_path.stem}::{len(entries)+1}"
        norm_fns = normalize_functions(fns, dup_map)
        if norm_fns:
            entries.append((compliance, id_val, norm_fns))
    return entries


def main(argv: List[str]) -> int:
    # Resolve base: .../compliance_Database
    script_path = Path(__file__).resolve()
    base_dir = script_path.parents[2]
    aws_root = base_dir / "final_complaince_database_with_fn_name" / "aws_function_complaince_mapping"
    if not aws_root.exists():
        print(f"AWS mapping folder not found: {aws_root}", file=sys.stderr)
        return 2

    dup_map = build_duplicate_map(base_dir)

    combined: Dict[Tuple[str, str], Set[str]] = {}
    files_scanned = 0

    for dirpath, _, filenames in os.walk(aws_root):
        for fn in filenames:
            if not fn.lower().endswith(".json"):
                continue
            if fn.lower().endswith(".bak.json") or fn.lower().endswith(".json.bak"):
                continue
            file_path = Path(dirpath) / fn
            files_scanned += 1
            for compliance, cid, fns in collect_entries_from_file(aws_root, file_path, dup_map):
                key = (compliance, cid)
                st = combined.setdefault(key, set())
                st.update(fns)

    # Build sorted output
    out_items: List[Dict[str, Any]] = []
    for (compliance, cid), fnset in combined.items():
        out_items.append({
            "compliance": compliance,
            "id": cid,
            "function_names": sorted(fnset)
        })

    out_items.sort(key=lambda x: (x["compliance"].lower(), str(x["id"]).lower()))

    out_path = aws_root / "aws_combined_control_functions.json"
    out_path.write_text(json.dumps(out_items, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"Scanned files: {files_scanned}")
    print(f"Unique compliance-id entries: {len(out_items)}")
    print(f"Output: {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
