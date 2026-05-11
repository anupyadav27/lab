#!/usr/bin/env python3
"""
Merge Matrix Additions

- Reads aws_matrix_structured_comprehensive_v2_2025-09-24.json
- Reads aws_matrix_additions_2025-09-24.json
- Dedupe by (service, resource, adapter, assertion_id)
- Writes merged to aws_matrix_structured_comprehensive_v2_merged_2025-09-24.json
"""

import json
import os
from typing import Any, Dict, List, Tuple

BASE_DIR = "/Users/apple/Desktop/compliance_Database/rule-generator-engine/Step3-matrices-per-cloud-provider"
MATRIX_IN = f"{BASE_DIR}/aws_matrix_structured_comprehensive_v2_2025-09-24.json"
ADDITIONS_IN = f"{BASE_DIR}/aws_matrix_additions_2025-09-24.json"
MATRIX_OUT = f"{BASE_DIR}/aws_matrix_structured_comprehensive_v2_merged_2025-09-24.json"


def load_json(path: str) -> Any:
  with open(path, 'r', encoding='utf-8') as f:
    return json.load(f)


def save_json(path: str, data: Any) -> None:
  os.makedirs(os.path.dirname(path), exist_ok=True)
  with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)


def key_of(row: Dict[str, Any]) -> Tuple[str, str, str, str]:
  return (
    row.get('service',''),
    row.get('resource',''),
    row.get('adapter',''),
    row.get('assertion_id','')
  )


def merge() -> Dict[str, Any]:
  matrix = load_json(MATRIX_IN)
  additions_doc = load_json(ADDITIONS_IN)

  merged = matrix
  if 'matrix' not in merged:
    merged['matrix'] = {}

  # Build existing key set for dedup
  existing_keys = set()
  for bucket, rows in merged['matrix'].items():
    for r in rows:
      existing_keys.add(key_of(r))

  added_count = 0
  buckets_added = 0

  for bucket, rows in additions_doc.get('additions', {}).items():
    if bucket not in merged['matrix']:
      merged['matrix'][bucket] = []
      buckets_added += 1
    for r in rows:
      k = key_of(r)
      if k in existing_keys:
        continue
      merged['matrix'][bucket].append(r)
      existing_keys.add(k)
      added_count += 1

  merged['total_checks'] = sum(len(v) for v in merged['matrix'].values())
  return {
    'merged': merged,
    'stats': {
      'buckets_added': buckets_added,
      'rows_added': added_count,
      'total_checks': merged['total_checks']
    }
  }


def main() -> None:
  result = merge()
  save_json(MATRIX_OUT, result['merged'])
  print(f"Merged into {MATRIX_OUT}")
  print(f"Buckets added: {result['stats']['buckets_added']}")
  print(f"Rows added: {result['stats']['rows_added']}")
  print(f"Total checks: {result['stats']['total_checks']}")

if __name__ == '__main__':
  main()
