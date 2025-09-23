import json
import os
import glob
from typing import Any, Dict, List, Set, Tuple

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SERVICE_PROMPTS_DIR = os.path.join(BASE_DIR, 'fn_list_finalisation', 'aws', 'complete_fn_list', 'service_prompts')
COMBINED_PATH = os.path.join(BASE_DIR, 'fn_list_finalisation', 'aws', 'complete_fn_list', 'combined_services_functions.json')


def load_service_files() -> List[str]:
    patterns = [
        os.path.join(SERVICE_PROMPTS_DIR, '*', '*_compliance_output.json'),
        os.path.join(SERVICE_PROMPTS_DIR, '*', '*_compliance_output (1).json'),
        os.path.join(SERVICE_PROMPTS_DIR, '*', '*_compliance_output*.json'),
    ]
    files: List[str] = []
    for p in patterns:
        files.extend(glob.glob(p))
    # Dedupe order-preserving
    seen = set()
    ordered = []
    for f in files:
        if f not in seen:
            seen.add(f)
            ordered.append(f)
    return ordered


def folder_service_name(path: str) -> str:
    return os.path.basename(os.path.dirname(path)).lower()


def extract_source_functions(path: str) -> Tuple[str, List[Dict[str, Any]]]:
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    svc = None
    arr: List[Any] = []
    if isinstance(data, dict) and 'services' in data and isinstance(data['services'], dict):
        # prefer folder name
        folder = folder_service_name(path)
        block = data['services'].get(folder)
        if block and isinstance(block, dict) and 'check_functions' in block:
            svc = folder
            arr = block.get('check_functions') or []
        else:
            # fallback first
            for k, v in data['services'].items():
                if isinstance(v, dict) and 'check_functions' in v:
                    svc = k
                    arr = v.get('check_functions') or []
                    break
    elif isinstance(data, dict) and 'check_functions' in data:
        svc = data.get('service_name') or folder_service_name(path)
        arr = data.get('check_functions') or []
    if svc is None:
        svc = folder_service_name(path)
    # Normalize to list of dicts with function_name and flags
    norm: List[Dict[str, Any]] = []
    for it in arr:
        if isinstance(it, str):
            norm.append({'function_name': it, 'raw': it})
        elif isinstance(it, dict):
            fn = it.get('function_name') or it.get('name')
            if not fn:
                # keep placeholder to detect missing name inputs
                norm.append({'function_name': None, 'raw': it})
            else:
                entry = {'function_name': fn, 'raw': it}
                entry['is_duplicate'] = (it.get('category') == 'DUPLICATE') or ('replacement_function' in it)
                exec_type = (it.get('execution_type') or '').lower()
                entry['is_manual'] = exec_type.startswith('manual effort') or exec_type.startswith('hybrid approach')
                norm.append(entry)
    return svc, norm


def extract_combined_functions(combined: Dict[str, Any], svc: str) -> Tuple[Set[str], Set[str], Set[str], List[Dict[str, Any]]]:
    svc_block = (combined.get('services') or {}).get(svc) or {}
    prog = (svc_block.get('programmable_functions') or {})
    uniq = prog.get('unique') or []
    dups = prog.get('duplicates') or []
    manual = svc_block.get('manual_functions') or []

    def names(lst: List[Any]) -> Set[str]:
        out: Set[str] = set()
        for it in lst:
            if isinstance(it, dict) and 'function_name' in it and it['function_name']:
                out.add(it['function_name'])
        return out

    uniq_names = names(uniq)
    dup_names = names(dups)
    manual_names = names(manual)

    # Detect schema issues: entries missing function_name
    schema_issues: List[Dict[str, Any]] = []
    for lst_name, lst in [('unique', uniq), ('duplicates', dups), ('manual', manual)]:
        for idx, it in enumerate(lst):
            if not (isinstance(it, dict) and it.get('function_name')):
                schema_issues.append({'list': lst_name, 'index': idx, 'entry': it})

    return uniq_names, dup_names, manual_names, schema_issues


def main():
    files = load_service_files()
    with open(COMBINED_PATH, 'r', encoding='utf-8') as f:
        combined = json.load(f)

    source_services: Set[str] = set()
    missing_services: List[str] = []
    per_service_report: List[Dict[str, Any]] = []
    total_missing_functions = 0
    total_schema_issues = 0

    for p in files:
        svc, src_entries = extract_source_functions(p)
        source_services.add(svc)
        uniq, dups, manual, schema_issues = extract_combined_functions(combined, svc)

        # Build expected sets from source
        src_all: List[str] = []
        for e in src_entries:
            fn = e.get('function_name')
            if fn:
                src_all.append(fn)
        src_set = set(src_all)

        combined_all = uniq | dups | manual

        missing = sorted(list(src_set - combined_all))
        extra = sorted(list(combined_all - src_set))

        report = {
            'service': svc,
            'source_functions': len(src_all),
            'combined_unique': len(uniq),
            'combined_duplicates': len(dups),
            'combined_manual': len(manual),
            'missing_in_combined': missing[:50],
            'missing_count': len(missing),
            'extra_in_combined': extra[:50],
            'extra_count': len(extra),
            'schema_issues_count': len(schema_issues),
        }
        total_missing_functions += len(missing)
        total_schema_issues += len(schema_issues)
        per_service_report.append(report)

    combined_services = set((combined.get('services') or {}).keys())
    missing_service_blocks = sorted(list(source_services - combined_services))

    summary = {
        'source_service_files': len(files),
        'source_services_detected': len(source_services),
        'combined_services_blocks': len(combined_services),
        'missing_service_blocks': missing_service_blocks[:50],
        'missing_service_blocks_count': len(missing_service_blocks),
        'total_missing_functions': total_missing_functions,
        'total_schema_issues': total_schema_issues,
    }

    print(json.dumps({'summary': summary, 'per_service': per_service_report[:30]}, indent=2))


if __name__ == '__main__':
    main()
