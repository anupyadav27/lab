#!/usr/bin/env python3
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Set

# Tolerant JSON loader (supports // and /* */ comments)
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

def extract_names_from_list(items: Any) -> List[str]:
    out: List[str] = []
    if not isinstance(items, list):
        return out
    for it in items:
        if isinstance(it, str):
            if it:
                out.append(it)
        elif isinstance(it, dict):
            name = it.get("function_name") or it.get("name")
            if isinstance(name, str) and name:
                out.append(name)
    return out

def build_duplicate_map_for_service(global_dups: List[Dict[str, Any]], service: str) -> Dict[str, str]:
    m: Dict[str, str] = {}
    for entry in (global_dups or []):
        repl = entry.get("replacement_function")
        replaces = entry.get("replaces") or []
        if not isinstance(replaces, list) or not isinstance(repl, str) or not repl:
            continue
        for r in replaces:
            if not isinstance(r, dict):
                continue
            if r.get("service") == service:
                fn = r.get("function_name")
                if isinstance(fn, str) and fn and fn != repl:
                    m[fn] = repl
    return m

def main(argv: List[str]) -> int:
    script_path = Path(__file__).resolve()
    base_dir = script_path.parents[2]  # .../compliance_Database
    src = base_dir / "etl-job_mapping _final_fn_name_generator" / "fn_list_finalisation" / "aws" / "complete_fn_list" / "combined_services_functions.json"
    if not src.exists():
        print(f"Source file not found: {src}", file=sys.stderr)
        return 2

    data = load_json_tolerant(src)
    services = data.get("services", {}) if isinstance(data, dict) else {}
    global_dups = data.get("global_duplicate_index", []) if isinstance(data, dict) else []

    result: Dict[str, Dict[str, List[str]]] = {}
    programmable_total = 0
    manual_total = 0

    for service, svc_obj in services.items():
        if not isinstance(svc_obj, dict):
            continue
        prog = svc_obj.get("programmable_functions", {}) or {}
        uniq_names: List[str] = extract_names_from_list(prog.get("unique"))

        # Also consider service-level duplicates if they explicitly list names
        svc_dup_names: List[str] = []
        svc_dups = prog.get("duplicates") or []
        if isinstance(svc_dups, list):
            for d in svc_dups:
                if isinstance(d, dict):
                    svc_dup_names += extract_names_from_list(d.get("replaces"))

        # Build duplicate mapping from global index for this service
        dup_map = build_duplicate_map_for_service(global_dups, service)

        # Normalize unique names by applying duplicate mapping
        combined_prog_set: Set[str] = set()
        for name in uniq_names:
            combined_prog_set.add(dup_map.get(name, name))
        # Add replacement functions for any duplicates found for this service
        # If service-level duplicates had explicit names, map them; also add the replacement itself
        for d in (svc_dups or []):
            if not isinstance(d, dict):
                continue
            repl = d.get("replacement_function")
            if isinstance(repl, str) and repl:
                combined_prog_set.add(repl)
            for r in (d.get("replaces") or []):
                if isinstance(r, dict):
                    fn = r.get("function_name")
                    if isinstance(fn, str) and fn:
                        combined_prog_set.add(dup_map.get(fn, repl or fn))
        # Also ensure all replacements from global map are present for this service
        for _old, new in dup_map.items():
            combined_prog_set.add(new)

        # Manual names
        manual_names: List[str] = extract_names_from_list(svc_obj.get("manual_functions"))

        result[service] = {
            "programmable": sorted(combined_prog_set),
            "manual": sorted(set(manual_names)),
        }
        programmable_total += len(result[service]["programmable"])
        manual_total += len(result[service]["manual"])

    out = {
        "services": result,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": str(src),
        "counts": {
            "services": len(result),
            "programmable_total": programmable_total,
            "manual_total": manual_total,
        },
    }

    out_path = src.parent / "service_function_list_by_service.json"
    out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote: {out_path}")
    print(f"Services: {len(result)} | Programmable total: {programmable_total} | Manual total: {manual_total}")
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
