#!/usr/bin/env python3
import json
import re
from pathlib import Path

def extract_cis_functions():
    """Extract all function names from CIS Azure Foundations file"""
    
    cis_path = "/Users/apple/Desktop/compliance_Database/Final_compliance_azure/CIS_MICROSOFT_AZURE_FOUNDATIONS_BENCHMARK_V4.0.0_updated_20250825_190952.json"
    with open(cis_path, 'r') as f:
        cis_data = json.load(f)
    
    functions = []
    for control in cis_data:
        if "function_names" in control:
            for func_name in control["function_names"]:
                functions.append({
                    "id": control.get("id", ""),
                    "title": control.get("title", ""),
                    "function_name": func_name,
                    "assessment": control.get("assessment", ""),
                    "compliance_level": control.get("compliance_level", "")
                })
    
    return functions

def extract_matrix_adapters():
    """Extract all adapter names from Azure matrix"""
    
    matrix_path = "/Users/apple/Desktop/compliance_Database/rule-generator-engine/Step3-matrices-per-cloud-provider/azure_matrix_2025-01-09_enriched_complete_final_with_taxonomy.json"
    with open(matrix_path, 'r') as f:
        matrix = json.load(f)
    
    adapters = []
    for category, tiers in matrix.items():
        for tier_name, entries in tiers.items():
            for entry in entries:
                if "adapter" in entry:
                    adapters.append({
                        "category": category,
                        "tier": tier_name,
                        "adapter": entry["adapter"],
                        "service": entry.get("service", ""),
                        "resource": entry.get("resource", "")
                    })
    
    return adapters

def find_exact_matches(cis_functions, matrix_adapters):
    """Find exact or very close matches between CIS functions and matrix adapters"""
    
    exact_matches = []
    partial_matches = []
    no_matches = []
    
    for cis_func in cis_functions:
        cis_name = cis_func["function_name"].lower()
        
        # Remove azure_ prefix for comparison
        if cis_name.startswith("azure_"):
            cis_name = cis_name[6:]
        
        # Try to find exact match first
        exact_match = None
        partial_matches_for_func = []
        
        for adapter in matrix_adapters:
            adapter_name = adapter["adapter"].lower()
            
            # Remove azure. prefix for comparison
            if adapter_name.startswith("azure."):
                adapter_name = adapter_name[6:]
            
            # Exact match
            if cis_name == adapter_name:
                exact_match = adapter
                break
            
            # Check for partial match - same service and similar function
            cis_parts = cis_name.split("_")
            adapter_parts = adapter_name.split("_")
            
            # Check if they share significant parts
            if len(set(cis_parts) & set(adapter_parts)) >= 2:
                partial_matches_for_func.append(adapter)
        
        if exact_match:
            exact_matches.append({
                "cis_function": cis_func,
                "matrix_adapter": exact_match,
                "match_type": "exact"
            })
        elif partial_matches_for_func:
            partial_matches.append({
                "cis_function": cis_func,
                "matrix_adapters": partial_matches_for_func,
                "match_type": "partial"
            })
        else:
            no_matches.append(cis_func)
    
    return exact_matches, partial_matches, no_matches

def analyze_coverage():
    """Analyze coverage between CIS functions and Azure matrix"""
    
    print("=== PRECISE CIS AZURE FOUNDATIONS vs AZURE MATRIX COVERAGE ===\n")
    
    # Extract data
    cis_functions = extract_cis_functions()
    matrix_adapters = extract_matrix_adapters()
    
    print(f"CIS Azure Foundations Function Names: {len(cis_functions)}")
    print(f"Azure Matrix Adapters: {len(matrix_adapters)}\n")
    
    # Find matches
    exact_matches, partial_matches, no_matches = find_exact_matches(cis_functions, matrix_adapters)
    
    total_coverage = len(exact_matches) + len(partial_matches)
    coverage_percent = (total_coverage / len(cis_functions)) * 100
    
    print(f"COVERAGE SUMMARY:")
    print(f"  ✅ Exact Matches: {len(exact_matches)}")
    print(f"  🔍 Partial Matches: {len(partial_matches)}")
    print(f"  ❌ No Matches: {len(no_matches)}")
    print(f"  📊 Total Coverage: {total_coverage}/{len(cis_functions)} ({coverage_percent:.1f}%)\n")
    
    if exact_matches:
        print("EXACT MATCHES:")
        for match in exact_matches:
            cis = match["cis_function"]
            adapter = match["matrix_adapter"]
            print(f"  ✅ {cis['function_name']}")
            print(f"     CIS Control: {cis['id']} - {cis['title'][:60]}...")
            print(f"     Matrix: {adapter['adapter']} ({adapter['category']})\n")
    
    if partial_matches:
        print("PARTIAL MATCHES:")
        for match in partial_matches:
            cis = match["cis_function"]
            adapters = match["matrix_adapters"]
            print(f"  🔍 {cis['function_name']}")
            print(f"     CIS Control: {cis['id']} - {cis['title'][:60]}...")
            print(f"     Potential Matrix Matches:")
            for adapter in adapters[:3]:  # Show top 3
                print(f"       → {adapter['adapter']} ({adapter['category']})")
            if len(adapters) > 3:
                print(f"       → ... and {len(adapters) - 3} more")
            print()
    
    if no_matches:
        print("NO MATCHES FOUND:")
        for cis_func in no_matches:
            print(f"  ❌ {cis_func['function_name']}")
            print(f"     CIS Control: {cis_func['id']} - {cis_func['title'][:60]}...")
            print()
    
    # Show matrix coverage statistics
    print("MATRIX COVERAGE BY SERVICE:")
    service_coverage = {}
    for adapter in matrix_adapters:
        service = adapter["service"]
        if service not in service_coverage:
            service_coverage[service] = 0
        service_coverage[service] += 1
    
    for service, count in sorted(service_coverage.items(), key=lambda x: x[1], reverse=True):
        print(f"  {service}: {count} adapters")
    
    return {
        "cis_functions": cis_functions,
        "matrix_adapters": matrix_adapters,
        "exact_matches": exact_matches,
        "partial_matches": partial_matches,
        "no_matches": no_matches,
        "coverage_percent": coverage_percent
    }

if __name__ == "__main__":
    analyze_coverage()
