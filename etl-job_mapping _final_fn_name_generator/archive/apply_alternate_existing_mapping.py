import os
import json
from typing import Dict, List

SUGGESTIONS = 'aws_unified_function_suggestions.json'
BY_SERVICE = 'aws_functions_by_service.json'


def build_alt_map(suggestions_path: str) -> Dict[str, str]:
	with open(suggestions_path, 'r', encoding='utf-8') as f:
		items = json.load(f)
	mapping: Dict[str, str] = {}
	for entry in items:
		alt = entry.get('alternate_existing_function')
		funcs: List[str] = entry.get('functions', [])
		if not alt or not funcs:
			continue
		for fn in funcs:
			mapping[fn] = alt
	return mapping


def apply_mapping(by_service_path: str, mapping: Dict[str, str]) -> Dict[str, List[str]]:
	with open(by_service_path, 'r', encoding='utf-8') as f:
		data: Dict[str, List[str]] = json.load(f)
	updated: Dict[str, List[str]] = {}
	for category, functions in data.items():
		seen = set()
		new_list: List[str] = []
		for fn in functions:
			repl = mapping.get(fn, fn)
			if repl not in seen:
				seen.add(repl)
				new_list.append(repl)
		updated[category] = new_list
	return updated


def main() -> int:
	etl_dir = os.path.dirname(os.path.abspath(__file__))
	suggestions_path = os.path.join(etl_dir, SUGGESTIONS)
	by_service_path = os.path.join(etl_dir, BY_SERVICE)
	if not (os.path.exists(suggestions_path) and os.path.exists(by_service_path)):
		print('Required files not found')
		return 1
	alt_map = build_alt_map(suggestions_path)
	updated = apply_mapping(by_service_path, alt_map)
	with open(by_service_path, 'w', encoding='utf-8') as f:
		json.dump(updated, f, indent=2, sort_keys=True)
	print(f'Updated {by_service_path} using alternate_existing_function mapping')
	return 0


if __name__ == '__main__':
	exit(main()) 