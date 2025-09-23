import json
import os
import glob
import time
from typing import Any, Dict, List, Tuple

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SERVICE_PROMPTS_DIR = os.path.join(BASE_DIR, 'fn_list_finalisation', 'aws', 'complete_fn_list', 'service_prompts')
OUTPUT_PATH = os.path.join(BASE_DIR, 'fn_list_finalisation', 'aws', 'complete_fn_list', 'combined_services_functions.json')


def load_service_files() -> List[str]:
    patterns = [
        os.path.join(SERVICE_PROMPTS_DIR, '*', '*_compliance_output.json'),
        os.path.join(SERVICE_PROMPTS_DIR, '*', '*_compliance_output (1).json'),
        os.path.join(SERVICE_PROMPTS_DIR, '*', '*_compliance_output*.json'),
    ]
    files: List[str] = []
    for p in patterns:
        files.extend(glob.glob(p))
    # Dedupe while keeping order
    seen = set()
    ordered: List[str] = []
    for f in files:
        if f not in seen:
            seen.add(f)
            ordered.append(f)
    return ordered


def normalize_service_name(path: str) -> str:
    # folder name under service_prompts is the service key
    return os.path.basename(os.path.dirname(path)).lower()


def entry_from_string(fn: str) -> Dict[str, Any]:
    # Default classification for raw string entries
    return {
        'function_name': fn,
        'category': 'config',
        'description': fn.replace('_', ' '),
        'execution_type': 'Code Executable - Inferred from context',
        'remediation_effort': 'Programmable'
    }


def classify_entries(service_name: str, check_functions: List[Any]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]], int]:
    """
    Returns (programmable_unique, programmable_duplicates, manual, total_input_count)
    - Manual includes both Manual Effort and Hybrid Approach entries.
    - Duplicate detection: trust explicit duplicates via category == 'DUPLICATE' or replacement_function,
      and also mark exact-name repeats as duplicates of the first occurrence.
    """
    programmable_unique: List[Dict[str, Any]] = []
    programmable_duplicates: List[Dict[str, Any]] = []
    manual: List[Dict[str, Any]] = []
    total_input_count = len(check_functions)

    seen_unique: Dict[str, Dict[str, Any]] = {}

    def push_duplicate(fn_name: str, replacement: str, reason: str = 'duplicate'):
        programmable_duplicates.append({
            'function_name': fn_name,
            'replacement_function': replacement,
            'reason': reason
        })

    for item in check_functions:
        if isinstance(item, str):
            fn = item
            if fn in seen_unique:
                push_duplicate(fn, seen_unique[fn]['function_name'], 'exact-name duplicate')
                continue
            o = entry_from_string(fn)
            seen_unique[fn] = o
            programmable_unique.append({
                'function_name': o['function_name'],
                'category': o.get('category', 'config'),
                'description': o.get('description', ''),
            })
            continue

        if isinstance(item, dict):
            fn = item.get('function_name') or item.get('name')
            if not fn:
                # skip malformed
                continue
            exec_type = (item.get('execution_type') or '').lower()
            is_manual = exec_type.startswith('manual effort') or exec_type.startswith('hybrid approach')
            is_duplicate_flag = (item.get('category') == 'DUPLICATE') or ('replacement_function' in item)

            if is_duplicate_flag:
                replacement = item.get('replacement_function', fn)
                reason = 'explicit-duplicate'
                push_duplicate(fn, replacement, reason)
                continue

            if fn in seen_unique:
                push_duplicate(fn, seen_unique[fn]['function_name'], 'exact-name duplicate')
                continue

            if is_manual:
                manual.append({
                    'function_name': fn,
                    'description': item.get('description', ''),
                })
                seen_unique[fn] = {'function_name': fn}
            else:
                programmable_unique.append({
                    'function_name': fn,
                    'category': item.get('category', 'config'),
                    'description': item.get('description', ''),
                })
                seen_unique[fn] = {'function_name': fn}
            continue

        # Unknown item type -> skip

    return programmable_unique, programmable_duplicates, manual, total_input_count


def group_duplicates(dupes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Group duplicate entries by replacement_function and list the duplicate names they replace."""
    grouped: Dict[str, List[str]] = {}
    for d in dupes:
        rep = d.get('replacement_function') or d.get('function_name')
        fn = d.get('function_name')
        if not rep or not fn:
            continue
        grouped.setdefault(rep, [])
        if fn not in grouped[rep]:
            grouped[rep].append(fn)
    out: List[Dict[str, Any]] = []
    for rep, names in grouped.items():
        out.append({
            'replacement_function': rep,
            'replaces': names
        })
    out.sort(key=lambda x: x['replacement_function'])
    return out


def consolidate() -> Dict[str, Any]:
    files = load_service_files()
    services_out: Dict[str, Any] = {}
    # Collect raw cross-service duplicates
    global_dupe_map: Dict[str, List[Dict[str, Any]]] = {}

    for path in files:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception:
            continue

        # Find service key and its check_functions
        svc_key = None
        check_functions: List[Any] = []

        if isinstance(data, dict) and 'services' in data and isinstance(data['services'], dict):
            folder_service = normalize_service_name(path)
            svc_block = data['services'].get(folder_service)
            if svc_block and isinstance(svc_block, dict) and 'check_functions' in svc_block:
                svc_key = folder_service
                check_functions = svc_block.get('check_functions') or []
            else:
                for k, v in data['services'].items():
                    if isinstance(v, dict) and 'check_functions' in v:
                        svc_key = k
                        check_functions = v.get('check_functions') or []
                        break
        if not check_functions and isinstance(data, dict) and 'check_functions' in data:
            svc_key = data.get('service_name') or normalize_service_name(path)
            check_functions = data.get('check_functions') or []

        if not svc_key or not isinstance(check_functions, list):
            continue

        prog_unique, prog_dupes, manual, total = classify_entries(svc_key, check_functions)

        # Feed raw duplicates to global map (before grouping), include service
        for d in prog_dupes:
            rep = d.get('replacement_function') or d.get('function_name')
            fn = d.get('function_name')
            if not rep or not fn:
                continue
            global_dupe_map.setdefault(rep, []).append({'service': svc_key, 'function_name': fn})

        # Group duplicates by canonical replacement function as requested
        grouped_dupes = group_duplicates(prog_dupes)

        services_out[svc_key] = {
            'programmable_functions': {
                'unique': prog_unique,
                'duplicates': grouped_dupes
            },
            'manual_functions': manual,
            'counts': {
                'total': total,
                'unique_programmable': len(prog_unique),
                'duplicate_programmable': len(prog_dupes),
                'manual': len(manual)
            }
        }

    # Build canonical owner mapping by scanning uniques across services
    canonical_owner: Dict[str, str] = {}
    for svc, block in services_out.items():
        for u in (block.get('programmable_functions') or {}).get('unique', []) or []:
            fn = u.get('function_name')
            if fn and fn not in canonical_owner:
                canonical_owner[fn] = svc

    # Build global index with deduped entries
    global_index: List[Dict[str, Any]] = []
    for rep, entries in global_dupe_map.items():
        seen_pairs = set()
        replaces: List[Dict[str, Any]] = []
        for e in entries:
            key = (e['service'], e['function_name'])
            if key in seen_pairs:
                continue
            seen_pairs.add(key)
            replaces.append({'service': e['service'], 'function_name': e['function_name']})
        replaces.sort(key=lambda x: (x['service'], x['function_name']))
        global_index.append({
            'replacement_function': rep,
            'canonical_service': canonical_owner.get(rep),
            'replaces': replaces
        })
    global_index.sort(key=lambda x: x['replacement_function'])

    consolidated = {
        'services': services_out,
        'global_duplicate_index': global_index,
        'scan_metadata': {
            'sources': 'service_prompts/*/*_compliance_output*.json',
            'generated_at': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
            'notes': 'Manual includes Hybrid entries; duplicates grouped per service and globally by replacement_function.'
        }
    }
    return consolidated


def main():
    data = consolidate()
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    print(f'Wrote consolidated file to: {OUTPUT_PATH}')
    print(f'Total services: {len(data.get("services", {}))}')


if __name__ == '__main__':
    main()
