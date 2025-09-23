#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Set

# Tolerant JSON loader
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

def collect_service_functions(service_file: Path) -> Set[str]:
    data = load_json_tolerant(service_file)
    if not isinstance(data, dict):
        return set()
    services = data.get("services") or {}
    out: Set[str] = set()
    if isinstance(services, dict):
        for svc, obj in services.items():
            if not isinstance(obj, dict):
                continue
            for key in ("programmable", "manual"):
                lst = obj.get(key)
                if isinstance(lst, list):
                    for name in lst:
                        if isinstance(name, str) and name:
                            out.add(name)
    return out


def main(argv: List[str]) -> int:
    root = Path(__file__).resolve().parents[2]
    unique_file = root / "final_complaince_database_with_fn_name" / "aws_function_complaince_mapping" / "aws_function_names_unique.json"
    service_file = root / "etl-job_mapping _final_fn_name_generator" / "fn_list_finalisation" / "aws" / "complete_fn_list" / "service_function_list_by_service.json"

    if not unique_file.exists():
        print(f"Missing unique file: {unique_file}", file=sys.stderr)
        return 2
    if not service_file.exists():
        print(f"Missing service file: {service_file}", file=sys.stderr)
        return 2

    unique_data = load_json_tolerant(unique_file)
    unique_set: Set[str] = set([x for x in unique_data if isinstance(x, str)]) if isinstance(unique_data, list) else set()

    service_set: Set[str] = collect_service_functions(service_file)

    common = sorted(unique_set & service_set)
    only_in_unique = sorted(unique_set - service_set)
    only_in_services = sorted(service_set - unique_set)

    out = {
        "counts": {
            "unique_total": len(unique_set),
            "services_total": len(service_set),
            "common": len(common),
            "only_in_unique": len(only_in_unique),
            "only_in_services": len(only_in_services),
        },
        "common": common,
        "only_in_unique": only_in_unique,
        "only_in_services": only_in_services,
        "sources": {
            "unique_file": str(unique_file),
            "service_file": str(service_file),
        },
    }

    out_path = service_file.parent / "function_set_comparison.json"
    out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote: {out_path}")
    print(json.dumps(out["counts"], indent=2))
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
