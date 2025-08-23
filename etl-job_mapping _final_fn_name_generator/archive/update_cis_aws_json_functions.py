import os
import json
from typing import Dict, List, Tuple

# Paths relative to this script directory
SUGGESTIONS = 'aws_unified_function_suggestions.json'
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))


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


def is_aws_file(filename: str) -> bool:
	l = filename.lower()
	return l.endswith('.json') and ('aws' in l or 'amazon' in l)


def update_function_names_array(fn_list: List[str], mapping: Dict[str, str]) -> Tuple[List[str], int]:
	replacements = 0
	seen = set()
	new_list: List[str] = []
	for fn in fn_list:
		repl = mapping.get(fn, fn)
		if repl != fn:
			replacements += 1
		if repl not in seen:
			seen.add(repl)
			new_list.append(repl)
	return new_list, replacements


def update_file(path: str, mapping: Dict[str, str]) -> Tuple[bool, int]:
	"""Return (changed, replacements_count)."""
	try:
		with open(path, 'r', encoding='utf-8') as f:
			data = json.load(f)
	except Exception:
		return False, 0

	changed = False
	replacements_total = 0
	if isinstance(data, list):
		for obj in data:
			if isinstance(obj, dict) and 'function_names' in obj and isinstance(obj['function_names'], list):
				new_list, reps = update_function_names_array(obj['function_names'], mapping)
				if reps > 0:
					obj['function_names'] = new_list
					changed = True
					replacements_total += reps
	elif isinstance(data, dict):
		# Alternative structures: try top-level 'items' list
		items = data.get('items')
		if isinstance(items, list):
			for obj in items:
				if isinstance(obj, dict) and 'function_names' in obj and isinstance(obj['function_names'], list):
					new_list, reps = update_function_names_array(obj['function_names'], mapping)
					if reps > 0:
						obj['function_names'] = new_list
						changed = True
						replacements_total += reps

	if changed:
		with open(path, 'w', encoding='utf-8') as f:
			json.dump(data, f, indent=2, sort_keys=False)
	return changed, replacements_total


def main() -> int:
	etl_dir = os.path.dirname(os.path.abspath(__file__))
	suggestions_path = os.path.join(etl_dir, SUGGESTIONS)
	if not os.path.exists(suggestions_path):
		print('Suggestions file not found:', suggestions_path)
		return 1
	alt_map = build_alt_map(suggestions_path)
	if not alt_map:
		print('No alternate mapping found. Nothing to do.')
		return 0

	updated_files = 0
	total_replacements = 0
	for entry in os.listdir(REPO_ROOT):
		path = os.path.join(REPO_ROOT, entry)
		if not os.path.isfile(path):
			continue
		if not is_aws_file(entry):
			continue
		changed, reps = update_file(path, alt_map)
		if changed:
			updated_files += 1
			total_replacements += reps
			print(f'Updated {entry}: {reps} replacements')

	print(f'Completed. Files updated: {updated_files}, total replacements: {total_replacements}')
	return 0


if __name__ == '__main__':
	exit(main()) 