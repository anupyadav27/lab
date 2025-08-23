#!/usr/bin/env python3
"""
GCP Function Database Consolidation Script

This script consolidates all updated GCP function databases from different CIS benchmarks
into a single master database, handling duplicates intelligently across all fields.

Files to be combined:
1. CIS GOOGLE KUBERNETES ENGINE (GKE) BENCHMARK V1.7.0 PDF/gcp_simplified_function_names_updated_20250822_201840.json
2. CIS_GOOGLE_CLOUD_PLATFORM_FOUNDATION_BENCHMARK_V4.0.0/gcp_simplified_function_names_updated_20250822_202829.json
3. CIS_GOOGLE_CONTAINER_OPTIMIZED_OS_BENCHMARK_V1.2.0/gcp_simplified_function_names_updated_20250822_203449.json
4. CIS_GOOGLE_KUBERNETES_ENGINE_(GKE)_AUTOPILOT_BENCHMARK_V1.0.0 PDF/gcp_simplified_function_names_updated_20250822_204345.json
5. CIS_GOOGLE_KUBERNETES_ENGINE_(GKE)_BENCHMARK_V1.8.0_PDF/gcp_simplified_function_names_updated_20250822_204345.json
6. CIS_GOOGLE_KUBERNETES_ENGINE(GKE)_AUTOPILOT_BENCHMARK_V1.2.0_PDF/gcp_simplified_function_names_updated_20250822_204345.json
7. CIS_GOOGLE_WORKSPACE_FOUNDATIONS_BENCHMARK_V1.3.0/gcp_simplified_function_names_updated_20250822_204345.json
"""

import json
import os
import sys
from datetime import datetime
from collections import defaultdict
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Define the files to be consolidated
FILES_TO_CONSOLIDATE = [
    {
        "name": "GKE Benchmark v1.7.0",
        "path": "./CIS GOOGLE KUBERNETES ENGINE (GKE) BENCHMARK V1.7.0 PDF/gcp_simplified_function_names_updated_20250822_201840.json",
        "expected_functions": 4721
    },
    {
        "name": "Foundation Benchmark v4.0.0",
        "path": "./CIS_GOOGLE_CLOUD_PLATFORM_FOUNDATION_BENCHMARK_V4.0.0/gcp_simplified_function_names_updated_20250822_202829.json",
        "expected_functions": 4672
    },
    {
        "name": "Container Optimized OS v1.2.0",
        "path": "./CIS_GOOGLE_CONTAINER_OPTIMIZED_OS_BENCHMARK_V1.2.0/gcp_simplified_function_names_updated_20250822_203449.json",
        "expected_functions": 4769
    },
    {
        "name": "GKE Autopilot v1.0.0",
        "path": "./CIS_GOOGLE_KUBERNETES_ENGINE_(GKE)_AUTOPILOT_BENCHMARK_V1.0.0 PDF/gcp_simplified_function_names_updated_20250822_204345.json",
        "expected_functions": 4690
    },
    {
        "name": "GKE Benchmark v1.8.0",
        "path": "./CIS_GOOGLE_KUBERNETES_ENGINE_(GKE)_BENCHMARK_V1.8.0_PDF/gcp_simplified_function_names_updated_20250822_204345.json",
        "expected_functions": 4712
    },
    {
        "name": "GKE Autopilot v1.2.0",
        "path": "./CIS_GOOGLE_KUBERNETES_ENGINE(GKE)_AUTOPILOT_BENCHMARK_V1.2.0_PDF/gcp_simplified_function_names_updated_20250822_204345.json",
        "expected_functions": 4691
    },
    {
        "name": "Workspace Foundations v1.3.0",
        "path": "./CIS_GOOGLE_WORKSPACE_FOUNDATIONS_BENCHMARK_V1.3.0/gcp_simplified_function_names_updated_20250822_204345.json",
        "expected_functions": 4745
    }
]

def load_json_file(file_path: str) -> list:
    """Load a JSON file and return the data"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return []
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing JSON file {file_path}: {e}")
        return []

def save_json_file(data: list, file_path: str):
    """Save data to a JSON file"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logger.info(f"Successfully saved to: {file_path}")
    except Exception as e:
        logger.error(f"Error saving file {file_path}: {e}")

def normalize_function_name(function_name: str) -> str:
    """Normalize function name for comparison"""
    if not function_name:
        return ""
    return function_name.lower().strip()

def compare_functions(func1: dict, func2: dict) -> float:
    """Compare two functions and return similarity score (0-1)"""
    score = 0.0
    total_fields = 0
    
    # Compare function_name (exact match gets highest weight)
    if func1.get('function_name') == func2.get('function_name'):
        score += 0.4
    total_fields += 0.4
    
    # Compare description (semantic similarity)
    desc1 = func1.get('description', '').lower()
    desc2 = func2.get('description', '').lower()
    if desc1 == desc2:
        score += 0.3
    elif desc1 and desc2 and (desc1 in desc2 or desc2 in desc1):
        score += 0.2
    total_fields += 0.3
    
    # Compare service_category
    if func1.get('service_category') == func2.get('service_category'):
        score += 0.2
    total_fields += 0.2
    
    # Compare gcp_sdk_example
    if func1.get('gcp_sdk_example') == func2.get('gcp_sdk_example'):
        score += 0.1
    total_fields += 0.1
    
    return score / total_fields if total_fields > 0 else 0.0

def merge_function_data(func1: dict, func2: dict, source1: str, source2: str) -> dict:
    """Merge two function entries, preferring the better one"""
    # Create a merged function
    merged = func1.copy()
    
    # Merge sheets (combine both sources)
    sheet1 = func1.get('sheet', '')
    sheet2 = func2.get('sheet', '')
    if sheet1 and sheet2 and sheet1 != sheet2:
        merged['sheet'] = f"{sheet1};{sheet2}"
    elif sheet2 and not sheet1:
        merged['sheet'] = sheet2
    
    # Merge rule_ids (combine both sources)
    rule_id1 = func1.get('rule_id', '')
    rule_id2 = func2.get('rule_id', '')
    if rule_id1 and rule_id2 and rule_id1 != rule_id2:
        merged['rule_id'] = f"{rule_id1};{rule_id2}"
    elif rule_id2 and not rule_id1:
        merged['rule_id'] = rule_id2
    
    # Prefer longer/more detailed description
    desc1 = func1.get('description', '')
    desc2 = func2.get('description', '')
    if len(desc2) > len(desc1):
        merged['description'] = desc2
    
    # Prefer higher confidence score
    conf1 = func1.get('confidence', 0)
    conf2 = func2.get('confidence', 0)
    if conf2 > conf1:
        merged['confidence'] = conf2
    
    # Prefer more detailed gcp_sdk_example
    example1 = func1.get('gcp_sdk_example', '')
    example2 = func2.get('gcp_sdk_example', '')
    if len(example2) > len(example1):
        merged['gcp_sdk_example'] = example2
    
    # Add source tracking
    merged['_sources'] = [source1, source2]
    
    return merged

def consolidate_databases() -> dict:
    """Consolidate all databases into a single master database"""
    print("🔄 GCP Function Database Consolidation")
    print("=" * 60)
    
    all_functions = []
    function_groups = defaultdict(list)
    stats = {
        'total_files_processed': 0,
        'total_functions_loaded': 0,
        'duplicates_found': 0,
        'duplicates_merged': 0,
        'unique_functions': 0,
        'file_stats': {}
    }
    
    # Load all databases
    print("📁 Loading all database files...")
    for file_info in FILES_TO_CONSOLIDATE:
        file_path = file_info["path"]
        file_name = file_info["name"]
        
        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}")
            continue
        
        print(f"📖 Loading {file_name}...")
        functions = load_json_file(file_path)
        
        if not functions:
            print(f"❌ Failed to load {file_name}")
            continue
        
        actual_count = len(functions)
        expected_count = file_info["expected_functions"]
        
        print(f"   ✅ Loaded {actual_count} functions (expected: {expected_count})")
        
        stats['total_files_processed'] += 1
        stats['total_functions_loaded'] += actual_count
        stats['file_stats'][file_name] = {
            'path': file_path,
            'functions_loaded': actual_count,
            'expected_functions': expected_count
        }
        
        # Group functions by normalized name for duplicate detection
        for func in functions:
            if func.get('function_name'):
                normalized_name = normalize_function_name(func['function_name'])
                function_groups[normalized_name].append((func, file_name))
    
    print(f"\n📊 Loaded {stats['total_functions_loaded']} functions from {stats['total_files_processed']} files")
    
    # Process function groups to handle duplicates
    print("\n🔄 Processing function groups and handling duplicates...")
    
    for normalized_name, functions in function_groups.items():
        if len(functions) == 1:
            # Single function, no duplicates
            func, source = functions[0]
            func['_sources'] = [source]
            all_functions.append(func)
            stats['unique_functions'] += 1
        else:
            # Multiple functions with same name, need to merge
            stats['duplicates_found'] += 1
            print(f"   🔄 Found {len(functions)} duplicates for: {normalized_name}")
            
            # Start with the first function
            merged_func = functions[0][0].copy()
            merged_func['_sources'] = [functions[0][1]]
            
            # Merge with all other duplicates
            for i in range(1, len(functions)):
                func, source = functions[i]
                merged_func = merge_function_data(merged_func, func, merged_func['_sources'][0], source)
                stats['duplicates_merged'] += 1
            
            all_functions.append(merged_func)
            stats['unique_functions'] += 1
    
    print(f"\n📈 Consolidation Statistics:")
    print(f"   Total functions loaded: {stats['total_functions_loaded']}")
    print(f"   Duplicate groups found: {stats['duplicates_found']}")
    print(f"   Duplicates merged: {stats['duplicates_merged']}")
    print(f"   Unique functions in final database: {stats['unique_functions']}")
    
    return {
        'functions': all_functions,
        'stats': stats
    }

def main():
    """Main function to consolidate all GCP databases"""
    print("🚀 Starting GCP Function Database Consolidation")
    print("=" * 80)
    
    # Show files to be consolidated
    print("📋 Files to be consolidated:")
    for i, file_info in enumerate(FILES_TO_CONSOLIDATE, 1):
        print(f"  {i}. {file_info['name']}")
        print(f"     Path: {file_info['path']}")
        print(f"     Expected: {file_info['expected_functions']} functions")
    
    print("\n🔄 Starting consolidation process...")
    
    # Consolidate all databases
    result = consolidate_databases()
    
    if not result['functions']:
        print("❌ No functions loaded. Consolidation failed.")
        sys.exit(1)
    
    # Generate output filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"gcp_consolidated_function_database_{timestamp}.json"
    
    # Save consolidated database
    print(f"\n💾 Saving consolidated database...")
    save_json_file(result['functions'], output_file)
    
    # Also save as a standard name
    standard_output_file = "gcp_consolidated_function_database.json"
    save_json_file(result['functions'], standard_output_file)
    
    # Print final summary
    stats = result['stats']
    print("\n" + "=" * 80)
    print("🎉 GCP Function Database Consolidation Complete!")
    print("=" * 80)
    print(f"Files processed: {stats['total_files_processed']}")
    print(f"Total functions loaded: {stats['total_functions_loaded']}")
    print(f"Duplicate groups found: {stats['duplicates_found']}")
    print(f"Duplicates merged: {stats['duplicates_merged']}")
    print(f"Unique functions in final database: {stats['unique_functions']}")
    print(f"Consolidated database: {output_file}")
    print(f"Standard database: {standard_output_file}")
    
    # Show file size
    if os.path.exists(output_file):
        file_size = os.path.getsize(output_file)
        print(f"File size: {file_size:,} bytes ({file_size/1024/1024:.2f} MB)")
    
    print("\n📊 Per-file breakdown:")
    for file_name, file_stats in stats['file_stats'].items():
        print(f"  {file_name}: {file_stats['functions_loaded']} functions")
    
    print("=" * 80)

if __name__ == "__main__":
    main()
