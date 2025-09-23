#!/usr/bin/env python3
import json
import re
from pathlib import Path

def extract_function_names_from_cis():
    """Extract all function names from CIS Azure Foundations file"""
    
    cis_path = "/Users/apple/Desktop/compliance_Database/Final_compliance_azure/CIS_MICROSOFT_AZURE_FOUNDATIONS_BENCHMARK_V4.0.0_updated_20250825_190952.json"
    with open(cis_path, 'r') as f:
        cis_data = json.load(f)
    
    function_names = set()
    control_mappings = []
    
    for control in cis_data:
        if "function_names" in control:
            for func_name in control["function_names"]:
                function_names.add(func_name)
                control_mappings.append({
                    "id": control.get("id", ""),
                    "title": control.get("title", ""),
                    "function_name": func_name,
                    "assessment": control.get("assessment", ""),
                    "compliance_level": control.get("compliance_level", "")
                })
    
    return function_names, control_mappings

def extract_adapters_from_matrix():
    """Extract all adapter names from Azure matrix"""
    
    matrix_path = "/Users/apple/Desktop/compliance_Database/rule-generator-engine/Step3-matrices-per-cloud-provider/azure_matrix_2025-01-09_enriched_complete_final_with_taxonomy.json"
    with open(matrix_path, 'r') as f:
        matrix = json.load(f)
    
    adapters = set()
    adapter_mappings = []
    
    for category, tiers in matrix.items():
        for tier_name, entries in tiers.items():
            for entry in entries:
                if "adapter" in entry:
                    adapter_name = entry["adapter"]
                    adapters.add(adapter_name)
                    adapter_mappings.append({
                        "category": category,
                        "tier": tier_name,
                        "adapter": adapter_name,
                        "service": entry.get("service", ""),
                        "resource": entry.get("resource", "")
                    })
    
    return adapters, adapter_mappings

def normalize_function_name(func_name):
    """Normalize function name for comparison"""
    # Remove common prefixes and normalize
    normalized = func_name.lower()
    # Remove azure_ prefix if present
    if normalized.startswith("azure_"):
        normalized = normalized[6:]
    return normalized

def find_matching_adapters(cis_function, matrix_adapters):
    """Find matching adapters in matrix for a CIS function"""
    normalized_cis = normalize_function_name(cis_function)
    matches = []
    
    for adapter in matrix_adapters:
        normalized_adapter = normalize_function_name(adapter)
        
        # Direct match
        if normalized_cis == normalized_adapter:
            matches.append(adapter)
        # Partial match - check if key components match
        elif any(word in normalized_adapter for word in normalized_cis.split("_")):
            matches.append(adapter)
    
    return matches

def compare_cis_with_matrix():
    """Compare CIS function names with Azure matrix adapters"""
    
    print("=== CIS AZURE FOUNDATIONS vs AZURE MATRIX COVERAGE ANALYSIS ===\n")
    
    # Extract data
    cis_functions, cis_mappings = extract_function_names_from_cis()
    matrix_adapters, matrix_mappings = extract_adapters_from_matrix()
    
    print(f"CIS Azure Foundations Function Names: {len(cis_functions)}")
    print(f"Azure Matrix Adapters: {len(matrix_adapters)}\n")
    
    # Find matches
    matched_functions = set()
    unmatched_functions = []
    function_to_adapter_mapping = {}
    
    for cis_func in cis_functions:
        matches = find_matching_adapters(cis_func, matrix_adapters)
        if matches:
            matched_functions.add(cis_func)
            function_to_adapter_mapping[cis_func] = matches
        else:
            unmatched_functions.append(cis_func)
    
    coverage_percent = (len(matched_functions) / len(cis_functions)) * 100
    
    print(f"COVERAGE SUMMARY:")
    print(f"  ✅ Matched: {len(matched_functions)}/{len(cis_functions)} ({coverage_percent:.1f}%)")
    print(f"  ❌ Unmatched: {len(unmatched_functions)}")
    
    if unmatched_functions:
        print(f"\nUNMATCHED CIS FUNCTIONS ({len(unmatched_functions)}):")
        for func in sorted(unmatched_functions):
            # Find the control info
            control_info = next((c for c in cis_mappings if c["function_name"] == func), None)
            if control_info:
                print(f"  - {func} (Control: {control_info['id']} - {control_info['title'][:60]}...)")
            else:
                print(f"  - {func}")
    
    print(f"\nMATCHED FUNCTIONS WITH MATRIX ADAPTERS:")
    for func in sorted(matched_functions):
        matches = function_to_adapter_mapping[func]
        print(f"  ✅ {func}")
        for match in matches[:3]:  # Show first 3 matches
            print(f"     → {match}")
        if len(matches) > 3:
            print(f"     → ... and {len(matches) - 3} more")
    
    # Show some examples of close matches for unmatched functions
    if unmatched_functions:
        print(f"\nPOTENTIAL MATCHES FOR UNMATCHED FUNCTIONS:")
        for func in sorted(unmatched_functions)[:10]:  # Show first 10
            potential_matches = []
            normalized_cis = normalize_function_name(func)
            
            for adapter in matrix_adapters:
                normalized_adapter = normalize_function_name(adapter)
                # Check for word overlap
                cis_words = set(normalized_cis.split("_"))
                adapter_words = set(normalized_adapter.split("_"))
                overlap = len(cis_words & adapter_words)
                
                if overlap >= 2:  # At least 2 words in common
                    potential_matches.append((adapter, overlap))
            
            if potential_matches:
                potential_matches.sort(key=lambda x: x[1], reverse=True)
                print(f"  🔍 {func}")
                for match, score in potential_matches[:2]:
                    print(f"     → {match} (score: {score})")
    
    return {
        "cis_functions": cis_functions,
        "matrix_adapters": matrix_adapters,
        "matched_functions": matched_functions,
        "unmatched_functions": unmatched_functions,
        "coverage_percent": coverage_percent
    }

if __name__ == "__main__":
    compare_cis_with_matrix()
