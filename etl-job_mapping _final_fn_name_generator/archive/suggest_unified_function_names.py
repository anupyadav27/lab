import os
import json
import re
from typing import Dict, List, Tuple

IN_DUP_JSON = 'aws_duplicates_by_category.json'
OUT_SUGGESTIONS_JSON = 'aws_unified_function_suggestions.json'
OUT_MAPPING_JSON = 'aws_unified_function_map.json'

TOKEN_SPLIT_RE = re.compile(r"[^a-z0-9]+")


def slugify(text: str) -> str:
	l = text.lower()
	l = l.replace('&', 'and')
	l = l.replace('/', ' ')
	l = l.replace('-', ' ')
	tokens = [t for t in TOKEN_SPLIT_RE.split(l) if t]
	return '_'.join(tokens)


def tokens(s: str) -> List[str]:
	return [t for t in TOKEN_SPLIT_RE.split(s.lower()) if t]


def jaccard(a: List[str], b: List[str]) -> float:
	sa, sb = set(a), set(b)
	if not sa and not sb:
		return 1.0
	return len(sa & sb) / max(1, len(sa | sb))


def normalize_status_suffix(name: str) -> str:
	parts = tokens(name)
	if not parts:
		return name.lower()
	# standardize required/configured -> enabled
	standardized: List[str] = []
	enabled_found = False
	for t in parts:
		if t in ('required', 'configured'):
			enabled_found = True
			continue
		elif t == 'enabled':
			enabled_found = True
			continue
		standardized.append(t)
	# append single 'enabled' at end if any status token seen
	if enabled_found:
		standardized.append('enabled')
	return '_'.join(standardized)


def build_suggested_name(category: str, key: str, functions: List[str]) -> Tuple[str, str]:
	# Pick the most elaborative existing function: max token count, then longest, then lexicographic
	scored = sorted(functions, key=lambda fn: (-(len(tokens(fn))), -len(fn), fn))
	chosen = scored[0]
	# apply normalization rule
	suggested = normalize_status_suffix(chosen)
	alt_existing = scored[1] if len(scored) > 1 else chosen
	return suggested, alt_existing


def main() -> int:
	etl_dir = os.path.dirname(os.path.abspath(__file__))
	in_path = os.path.join(etl_dir, IN_DUP_JSON)
	out_suggestions = os.path.join(etl_dir, OUT_SUGGESTIONS_JSON)
	out_mapping = os.path.join(etl_dir, OUT_MAPPING_JSON)
	if not os.path.exists(in_path):
		print(f"Input not found: {in_path}")
		return 1
	with open(in_path, 'r', encoding='utf-8') as f:
		dup_data: Dict[str, List[Dict[str, List[str]]]] = json.load(f)

	suggestions: List[Dict[str, object]] = []
	mapping: Dict[str, str] = {}

	for category, clusters in dup_data.items():
		for cluster in clusters:
			key = cluster.get('key', '')
			functions = cluster.get('functions', [])
			if not functions:
				continue
			suggested, alt_existing = build_suggested_name(category, key, functions)
			suggestions.append({
				'category': category,
				'key': key,
				'suggested_function': suggested,
				'alternate_existing_function': alt_existing,
				'functions': sorted(functions),
			})
			for fn in functions:
				mapping[fn] = suggested

	# sort for stability
	suggestions.sort(key=lambda x: (str(x['category']), str(x['suggested_function'])))
	with open(out_suggestions, 'w', encoding='utf-8') as f:
		json.dump(suggestions, f, indent=2)
	with open(out_mapping, 'w', encoding='utf-8') as f:
		json.dump(mapping, f, indent=2, sort_keys=True)
	print(f"Wrote suggestions to {out_suggestions}")
	print(f"Wrote mapping to {out_mapping}")
	return 0


if __name__ == '__main__':
	exit(main()) 