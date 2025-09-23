#!/usr/bin/env python3
import json
import re

def extract_scopes_from_assertions():
    """Extract scope allowlist from assertions pack"""
    with open('/Users/apple/Desktop/compliance_Database/rule-generator-engine/step-2-common-assercian-id/assertions_pack_final_2025-09-11T18-41-14.json', 'r') as f:
        data = json.load(f)
    return set(data['scope_allowlist'])

def extract_scopes_from_matrix():
    """Extract unique scopes from enriched matrix"""
    scopes = set()
    with open('/Users/apple/Desktop/compliance_Database/rule-generator-engine/Step3-matrices-per-cloud-provider/azure_matrix_2025-01-09_enriched_complete.json', 'r') as f:
        data = json.load(f)
    
    for assertion_key, tiers in data.items():
        for tier_name, rows in tiers.items():
            for row in rows:
                if 'resource' in row:
                    scopes.add(row['resource'])
    
    return scopes

def compare_scope_coverage():
    """Compare scope coverage between assertions and matrix"""
    assertion_scopes = extract_scopes_from_assertions()
    matrix_scopes = extract_scopes_from_matrix()
    
    print("=== SCOPE COVERAGE ANALYSIS ===\n")
    
    print(f"Assertions Pack Scopes: {len(assertion_scopes)}")
    print(f"Enriched Matrix Scopes: {len(matrix_scopes)}\n")
    
    # Scopes in assertions but missing from matrix
    missing_scopes = assertion_scopes - matrix_scopes
    print(f"MISSING SCOPES ({len(missing_scopes)}):")
    for scope in sorted(missing_scopes):
        print(f"  - {scope}")
    
    # Scopes in matrix but not in assertions (potential additions)
    extra_scopes = matrix_scopes - assertion_scopes
    print(f"\nEXTRA SCOPES IN MATRIX ({len(extra_scopes)}):")
    for scope in sorted(extra_scopes):
        print(f"  - {scope}")
    
    # Coverage percentage
    covered_scopes = assertion_scopes & matrix_scopes
    coverage_percent = (len(covered_scopes) / len(assertion_scopes)) * 100
    
    print(f"\nCOVERAGE SUMMARY:")
    print(f"  Covered: {len(covered_scopes)}/{len(assertion_scopes)} ({coverage_percent:.1f}%)")
    print(f"  Missing: {len(missing_scopes)}")
    print(f"  Extra: {len(extra_scopes)}")
    
    return {
        'assertion_scopes': assertion_scopes,
        'matrix_scopes': matrix_scopes,
        'missing_scopes': missing_scopes,
        'extra_scopes': extra_scopes,
        'coverage_percent': coverage_percent
    }

if __name__ == "__main__":
    compare_scope_coverage()
