"""
Create Clear, Human-Readable Duplicate Analysis
Focus on TRUE duplicates - functions doing EXACTLY the same thing
"""

import json
from pathlib import Path
from collections import defaultdict

OUTPUT_DIR = Path("/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule")
AWS_FILE = OUTPUT_DIR / "aws_functions_by_service_2025-11-08.json"

print("=" * 80)
print("AWS FUNCTION TRUE DUPLICATE ANALYSIS")
print("=" * 80)
print()

# Load AWS functions
with open(AWS_FILE, 'r') as f:
    data = json.load(f)

# Collect all functions
all_functions = []
for service_name, service_data in data['services'].items():
    for func_name, func_data in service_data['functions'].items():
        all_functions.append({
            'service': service_name,
            'function': func_name,
            'compliance_ids': set(func_data['compliance_ids']),
            'compliance_count': func_data['compliance_count']
        })

print(f"Analyzing {len(all_functions)} AWS functions...")
print()

# TRUE DUPLICATE CHECK 1: Functions with IDENTICAL compliance IDs
print("=" * 80)
print("CHECK 1: Functions Mapped to IDENTICAL Compliance Controls")
print("=" * 80)
print()
print("If two functions have the exact same compliance IDs, they likely do")
print("the same job and one might be redundant.")
print()

# Group by compliance ID sets
by_compliance_set = defaultdict(list)
for func in all_functions:
    # Convert set to sorted tuple for hashing
    id_key = tuple(sorted(func['compliance_ids']))
    by_compliance_set[id_key].append(func)

# Find groups with multiple functions
identical_compliance_groups = []
for id_set, funcs in by_compliance_set.items():
    if len(funcs) > 1 and len(id_set) > 0:  # Skip empty sets
        identical_compliance_groups.append({
            'compliance_ids': list(id_set),
            'compliance_count': len(id_set),
            'functions': funcs
        })

# Sort by number of functions in group
identical_compliance_groups.sort(key=lambda x: len(x['functions']), reverse=True)

print(f"Found {len(identical_compliance_groups)} groups with identical compliance mappings")
print()

if identical_compliance_groups:
    print("Top 20 Groups (sorted by number of functions):")
    print("-" * 80)
    
    for i, group in enumerate(identical_compliance_groups[:20], 1):
        print(f"\n{i}. {len(group['functions'])} functions → {group['compliance_count']} compliance controls")
        print(f"   Compliance IDs: {', '.join(group['compliance_ids'][:3])}")
        if len(group['compliance_ids']) > 3:
            print(f"                   ... and {len(group['compliance_ids']) - 3} more")
        print()
        print(f"   Functions doing the SAME job:")
        for func in group['functions']:
            print(f"     • [{func['service']}] {func['function']}")
        print()
        print(f"   ⚠️  ANALYSIS: Are these really the same? Review needed!")

# TRUE DUPLICATE CHECK 2: Functions in same service with high compliance overlap
print()
print("=" * 80)
print("CHECK 2: Functions in SAME Service with High Compliance Overlap")
print("=" * 80)
print()
print("Functions in the same service sharing 80%+ of compliance IDs might")
print("be duplicates or one might be a subset of the other.")
print()

# Group by service
by_service = defaultdict(list)
for func in all_functions:
    by_service[func['service']].append(func)

same_service_overlaps = []
for service, funcs in by_service.items():
    if len(funcs) < 2:
        continue
    
    # Compare each pair
    for i, func1 in enumerate(funcs):
        for func2 in funcs[i+1:]:
            # Calculate overlap
            if not func1['compliance_ids'] or not func2['compliance_ids']:
                continue
            
            shared = func1['compliance_ids'] & func2['compliance_ids']
            total_unique = func1['compliance_ids'] | func2['compliance_ids']
            
            if len(total_unique) == 0:
                continue
            
            overlap_pct = len(shared) / len(total_unique) * 100
            
            # High overlap (80%+)
            if overlap_pct >= 80 and len(shared) > 0:
                same_service_overlaps.append({
                    'service': service,
                    'func1': func1,
                    'func2': func2,
                    'shared_count': len(shared),
                    'shared_ids': list(shared),
                    'overlap_pct': overlap_pct,
                    'func1_only': list(func1['compliance_ids'] - func2['compliance_ids']),
                    'func2_only': list(func2['compliance_ids'] - func1['compliance_ids'])
                })

# Sort by overlap percentage
same_service_overlaps.sort(key=lambda x: (x['overlap_pct'], x['shared_count']), reverse=True)

print(f"Found {len(same_service_overlaps)} pairs with 80%+ overlap")
print()

if same_service_overlaps:
    print("Top 20 Pairs (sorted by overlap %):")
    print("-" * 80)
    
    for i, pair in enumerate(same_service_overlaps[:20], 1):
        print(f"\n{i}. Service: {pair['service'].upper()}")
        print(f"   Overlap: {pair['overlap_pct']:.1f}% ({pair['shared_count']} shared)")
        print()
        print(f"   Function 1: {pair['func1']['function']}")
        print(f"     Total mappings: {pair['func1']['compliance_count']}")
        if pair['func1_only']:
            print(f"     Unique to this: {len(pair['func1_only'])} IDs")
        print()
        print(f"   Function 2: {pair['func2']['function']}")
        print(f"     Total mappings: {pair['func2']['compliance_count']}")
        if pair['func2_only']:
            print(f"     Unique to this: {len(pair['func2_only'])} IDs")
        print()
        
        if pair['overlap_pct'] == 100:
            print(f"   ⚠️  EXACT MATCH - These are TRUE duplicates!")
        elif not pair['func1_only'] or not pair['func2_only']:
            print(f"   ⚠️  One is SUBSET of other - Possible duplicate or refinement")
        else:
            print(f"   ℹ️  Significant overlap but each has unique mappings")

# TRUE DUPLICATE CHECK 3: Very similar names in same service
print()
print("=" * 80)
print("CHECK 3: Nearly Identical Function Names in Same Service")
print("=" * 80)
print()
print("Functions with very similar names (90%+ word match) in same service")
print("might be duplicates with slight naming variations.")
print()

name_similar = []
for service, funcs in by_service.items():
    if len(funcs) < 2:
        continue
    
    for i, func1 in enumerate(funcs):
        for func2 in funcs[i+1:]:
            # Tokenize names
            words1 = set(func1['function'].lower().split('_'))
            words2 = set(func2['function'].lower().split('_'))
            
            # Calculate similarity
            shared_words = words1 & words2
            total_words = words1 | words2
            
            if len(total_words) == 0:
                continue
            
            similarity = len(shared_words) / len(total_words) * 100
            
            if similarity >= 90:
                # Also check compliance overlap
                if func1['compliance_ids'] and func2['compliance_ids']:
                    comp_shared = func1['compliance_ids'] & func2['compliance_ids']
                    comp_overlap = len(comp_shared) / len(func1['compliance_ids'] | func2['compliance_ids']) * 100
                else:
                    comp_overlap = 0
                
                name_similar.append({
                    'service': service,
                    'func1': func1,
                    'func2': func2,
                    'name_similarity': similarity,
                    'compliance_overlap': comp_overlap,
                    'shared_compliance_count': len(comp_shared) if func1['compliance_ids'] and func2['compliance_ids'] else 0
                })

name_similar.sort(key=lambda x: (x['name_similarity'], x['compliance_overlap']), reverse=True)

print(f"Found {len(name_similar)} pairs with 90%+ name similarity")
print()

if name_similar:
    print("Top 20 Pairs:")
    print("-" * 80)
    
    for i, pair in enumerate(name_similar[:20], 1):
        print(f"\n{i}. Service: {pair['service'].upper()}")
        print(f"   Name Similarity: {pair['name_similarity']:.1f}%")
        print(f"   Compliance Overlap: {pair['compliance_overlap']:.1f}%")
        print()
        print(f"   • {pair['func1']['function']}")
        print(f"     ({pair['func1']['compliance_count']} mappings)")
        print()
        print(f"   • {pair['func2']['function']}")
        print(f"     ({pair['func2']['compliance_count']} mappings)")
        print()
        
        if pair['name_similarity'] >= 95 and pair['compliance_overlap'] >= 80:
            print(f"   ⚠️  LIKELY DUPLICATE - Very similar name AND compliance overlap!")
        elif pair['name_similarity'] >= 95:
            print(f"   ℹ️  Similar names but different compliance - May serve different purposes")

# Summary
print()
print("=" * 80)
print("SUMMARY & RECOMMENDATIONS")
print("=" * 80)
print()

print(f"Total functions analyzed: {len(all_functions)}")
print()
print(f"Potential Issues Found:")
print(f"  • {len(identical_compliance_groups)} groups with identical compliance mappings")
print(f"  • {len(same_service_overlaps)} pairs with 80%+ compliance overlap")
print(f"  • {len(name_similar)} pairs with 90%+ name similarity")
print()

print("Priority Review:")
print("  1. Functions with 100% compliance overlap (exact duplicates)")
print("  2. Functions with 95%+ name similarity AND high compliance overlap")
print("  3. Functions where one is complete subset of another")
print()

# Create human-readable report
report = {
    "summary": {
        "total_functions": len(all_functions),
        "identical_compliance_groups": len(identical_compliance_groups),
        "high_overlap_pairs": len(same_service_overlaps),
        "similar_name_pairs": len(name_similar)
    },
    "identical_compliance_groups": [
        {
            "function_count": len(g['functions']),
            "compliance_count": g['compliance_count'],
            "compliance_ids": g['compliance_ids'],
            "functions": [
                {
                    "service": f['service'],
                    "function": f['function'],
                    "compliance_count": f['compliance_count']
                }
                for f in g['functions']
            ]
        }
        for g in identical_compliance_groups[:30]
    ],
    "high_overlap_same_service": [
        {
            "service": p['service'],
            "overlap_percentage": round(p['overlap_pct'], 1),
            "shared_compliance_count": p['shared_count'],
            "function_1": {
                "name": p['func1']['function'],
                "total_mappings": p['func1']['compliance_count'],
                "unique_mappings": len(p['func1_only'])
            },
            "function_2": {
                "name": p['func2']['function'],
                "total_mappings": p['func2']['compliance_count'],
                "unique_mappings": len(p['func2_only'])
            },
            "analysis": "EXACT DUPLICATE" if p['overlap_pct'] == 100 else 
                       ("SUBSET RELATIONSHIP" if not p['func1_only'] or not p['func2_only'] else 
                        "SIGNIFICANT OVERLAP")
        }
        for p in same_service_overlaps[:30]
    ],
    "similar_names_same_service": [
        {
            "service": p['service'],
            "name_similarity_percentage": round(p['name_similarity'], 1),
            "compliance_overlap_percentage": round(p['compliance_overlap'], 1),
            "function_1": p['func1']['function'],
            "function_2": p['func2']['function'],
            "analysis": "LIKELY DUPLICATE" if p['name_similarity'] >= 95 and p['compliance_overlap'] >= 80 else
                       "REVIEW NEEDED"
        }
        for p in name_similar[:30]
    ]
}

report_file = OUTPUT_DIR / "aws_true_duplicates_analysis_2025-11-08.json"
with open(report_file, 'w') as f:
    json.dump(report, f, indent=2)

print(f"Clear, human-readable report saved: {report_file}")
print()

