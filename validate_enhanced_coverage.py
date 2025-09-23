#!/usr/bin/env python3
import json

def validate_enhanced_scope_coverage():
    """Validate the enhanced scope coverage"""
    
    # Load enhanced assertions
    with open('/Users/apple/Desktop/compliance_Database/rule-generator-engine/step-2-common-assercian-id/assertions_pack_final_2025-09-11T18-41-14_enhanced.json', 'r') as f:
        enhanced_assertions = json.load(f)
    
    # Load enhanced matrix
    with open('/Users/apple/Desktop/compliance_Database/rule-generator-engine/Step3-matrices-per-cloud-provider/azure_matrix_2025-01-09_enriched_complete_enhanced.json', 'r') as f:
        enhanced_matrix = json.load(f)
    
    # Extract scopes
    assertion_scopes = set(enhanced_assertions['scope_allowlist'])
    
    matrix_scopes = set()
    for assertion_key, tiers in enhanced_matrix.items():
        for tier_name, rows in tiers.items():
            for row in rows:
                if 'resource' in row:
                    matrix_scopes.add(row['resource'])
    
    print("=== ENHANCED SCOPE COVERAGE VALIDATION ===\n")
    
    print(f"Enhanced Assertions Scopes: {len(assertion_scopes)}")
    print(f"Enhanced Matrix Scopes: {len(matrix_scopes)}\n")
    
    # Check coverage
    missing_scopes = assertion_scopes - matrix_scopes
    extra_scopes = matrix_scopes - assertion_scopes
    covered_scopes = assertion_scopes & matrix_scopes
    
    coverage_percent = (len(covered_scopes) / len(assertion_scopes)) * 100
    
    print(f"COVERAGE SUMMARY:")
    print(f"  ✅ Covered: {len(covered_scopes)}/{len(assertion_scopes)} ({coverage_percent:.1f}%)")
    print(f"  ❌ Missing: {len(missing_scopes)}")
    print(f"  ➕ Extra: {len(extra_scopes)}")
    
    if missing_scopes:
        print(f"\nMISSING SCOPES ({len(missing_scopes)}):")
        for scope in sorted(missing_scopes):
            print(f"  - {scope}")
    
    if extra_scopes:
        print(f"\nEXTRA SCOPES IN MATRIX ({len(extra_scopes)}):")
        for scope in sorted(extra_scopes):
            print(f"  - {scope}")
    
    # Show scope prefix coverage
    print(f"\nSCOPE PREFIX COVERAGE:")
    for prefix, scopes in enhanced_assertions['scope_prefixes'].items():
        prefix_covered = len(set(scopes) & matrix_scopes)
        prefix_total = len(scopes)
        prefix_percent = (prefix_covered / prefix_total) * 100 if prefix_total > 0 else 0
        print(f"  {prefix}: {prefix_covered}/{prefix_total} ({prefix_percent:.1f}%)")
    
    # Show Azure mapping coverage
    print(f"\nAZURE MAPPING COVERAGE:")
    azure_mappings = enhanced_assertions['azure_scope_mappings']
    mapped_scopes = set(azure_mappings.keys())
    mapped_coverage = len(mapped_scopes & matrix_scopes)
    mapping_percent = (mapped_coverage / len(mapped_scopes)) * 100 if len(mapped_scopes) > 0 else 0
    print(f"  Mapped scopes in matrix: {mapped_coverage}/{len(mapped_scopes)} ({mapping_percent:.1f}%)")
    
    return {
        'assertion_scopes': assertion_scopes,
        'matrix_scopes': matrix_scopes,
        'missing_scopes': missing_scopes,
        'extra_scopes': extra_scopes,
        'coverage_percent': coverage_percent
    }

if __name__ == "__main__":
    validate_enhanced_scope_coverage()
