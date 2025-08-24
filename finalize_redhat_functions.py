#!/usr/bin/env python3
"""
Script to finalize the best function names for RedHat CIS compliance checks.
This script analyzes the suggested function names and selects the most appropriate one
based on clarity, consistency, and adherence to naming conventions.
"""

import json
import re
from typing import Dict, List, Tuple

def analyze_function_names(function_names: List[str]) -> str:
    """
    Analyze suggested function names and return the best one.
    
    Criteria for selection:
    1. Most descriptive and clear
    2. Consistent with naming patterns
    3. Avoids redundant terms
    4. Follows the pattern: <category>_<specific_check>_<condition>
    """
    
    if not function_names:
        return ""
    
    if len(function_names) == 1:
        return function_names[0]
    
    # Score each function name based on quality criteria
    scored_names = []
    
    for name in function_names:
        score = 0
        
        # Prefer names that start with 'filesystem_' for filesystem-related checks
        if name.startswith('filesystem_'):
            score += 10
        
        # Prefer names that start with 'compute_' for compute-related checks
        if name.startswith('compute_'):
            score += 8
            
        # Prefer names that start with 'linux_' for Linux-specific checks
        if name.startswith('linux_'):
            score += 6
            
        # Prefer names that start with 'os_' for OS-level checks
        if name.startswith('os_'):
            score += 5
            
        # Prefer names that start with 'system_' for system-level checks
        if name.startswith('system_'):
            score += 4
            
        # Prefer names that start with 'storage_' for storage-related checks
        if name.startswith('storage_'):
            score += 3
            
        # Prefer names that start with 'server_' for server-specific checks
        if name.startswith('server_'):
            score += 2
            
        # Penalize overly long names
        if len(name) > 50:
            score -= 5
            
        # Penalize names with redundant terms
        redundant_terms = ['enabled', 'set', 'configured', 'restriction', 'enforced', 'protected', 'secure', 'compliant', 'applied']
        for term in redundant_terms:
            if name.count(term) > 1:
                score -= 3
                
        # Penalize names with unnecessary complexity
        if any(term in name for term in ['all_regions', 'over_90d', 'min_tls_1_2', 'secure_config']):
            score -= 5
            
        # Bonus for clear, descriptive names
        if '_' in name and len(name.split('_')) >= 3:
            score += 2
            
        scored_names.append((name, score))
    
    # Sort by score (highest first) and return the best one
    scored_names.sort(key=lambda x: x[1], reverse=True)
    return scored_names[0][0]

def clean_function_name(name: str) -> str:
    """
    Clean and standardize function names.
    """
    # Remove any trailing whitespace
    name = name.strip()
    
    # Ensure consistent formatting
    name = name.lower()
    
    return name

def finalize_compliance_functions(input_file: str, output_file: str):
    """
    Process the RedHat CIS compliance JSON file and finalize function names.
    """
    
    print(f"Reading input file: {input_file}")
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading input file: {e}")
        return
    
    print(f"Processing {len(data)} compliance checks...")
    
    finalized_count = 0
    unchanged_count = 0
    
    for item in data:
        if 'function_names' in item and item['function_names']:
            original_names = item['function_names']
            
            # Analyze and select the best function name
            best_name = analyze_function_names(original_names)
            
            if best_name:
                # Clean the function name
                cleaned_name = clean_function_name(best_name)
                
                # Replace the function_names array with the single best name
                item['function_names'] = [cleaned_name]
                
                # Add a comment about the selection
                item['selected_function_reason'] = f"Selected '{cleaned_name}' from {len(original_names)} options based on clarity and consistency"
                
                finalized_count += 1
            else:
                unchanged_count += 1
        else:
            unchanged_count += 1
    
    print(f"Finalized {finalized_count} function names")
    print(f"Unchanged: {unchanged_count} items")
    
    # Write the updated data to output file
    print(f"Writing output to: {output_file}")
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print("Successfully wrote finalized compliance functions")
    except Exception as e:
        print(f"Error writing output file: {e}")

def main():
    """
    Main function to run the function finalization process.
    """
    input_file = "raw_compliance_database/linux/redhat/CIS_RED_HAT_ENTERPRISE_LINUX_6_BENCHMARK_V3.0.0_ARCHIVE (1).json"
    output_file = "raw_compliance_database/linux/redhat/CIS_RED_HAT_ENTERPRISE_LINUX_6_BENCHMARK_V3.0.0_FINALIZED.json"
    
    print("RedHat CIS Compliance Function Finalization Tool")
    print("=" * 50)
    
    finalize_compliance_functions(input_file, output_file)
    
    print("\nFunction finalization complete!")
    print(f"Original file: {input_file}")
    print(f"Finalized file: {output_file}")

if __name__ == "__main__":
    main()
