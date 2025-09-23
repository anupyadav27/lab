#!/usr/bin/env python3
"""
Update Compliance Files with Mapped Functions

This script:
1. Updates the original compliance JSON files with existing + new function names
2. Creates a separate file with new function details for Python code generation
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

def load_mapping_results(mapping_file: str) -> Dict[str, Any]:
    """Load the mapping results from the JSON file"""
    with open(mapping_file, 'r') as f:
        return json.load(f)

def update_compliance_file(compliance_file: str, mapping_results: List[Dict], output_file: str):
    """Update compliance file with mapped functions"""
    
    # Load original compliance file
    with open(compliance_file, 'r') as f:
        compliance_data = json.load(f)
    
    # Create a mapping from compliance_id to mapping result
    id_to_mapping = {item['compliance_id']: item for item in mapping_results}
    
    # Update each compliance item
    updated_count = 0
    for item in compliance_data:
        compliance_id = item.get('id')
        if compliance_id in id_to_mapping:
            mapping = id_to_mapping[compliance_id]
            
            # Collect all function names (existing + new)
            all_functions = []
            
            # Add existing mapped functions
            all_functions.extend(mapping.get('existing_functions_mapped', []))
            
            # Add new function names
            for new_func in mapping.get('new_functions_needed', []):
                all_functions.append(new_func['name'])
            
            # Update the function_names field
            if all_functions:
                item['function_names'] = all_functions
                item['mapped_coverage'] = mapping.get('coverage_assessment', 'none')
                item['mapping_notes'] = mapping.get('mapping_notes', '')
                updated_count += 1
    
    # Save updated compliance file
    with open(output_file, 'w') as f:
        json.dump(compliance_data, f, indent=2)
    
    print(f"Updated {updated_count} compliance items in {output_file}")
    return updated_count

def extract_new_functions(mapping_results: List[Dict]) -> List[Dict]:
    """Extract all new functions with their details for Python code generation"""
    
    new_functions = []
    
    for mapping in mapping_results:
        compliance_id = mapping.get('compliance_id')
        title = mapping.get('title', '')
        
        for new_func in mapping.get('new_functions_needed', []):
            function_detail = {
                'function_name': new_func['name'],
                'service': new_func['service'],
                'boto3_api': new_func['boto3_api'],
                'rationale': new_func['rationale'],
                'compliance_id': compliance_id,
                'compliance_title': title,
                'coverage_assessment': mapping.get('coverage_assessment', 'none'),
                'mapping_notes': mapping.get('mapping_notes', '')
            }
            new_functions.append(function_detail)
    
    return new_functions

def create_new_functions_file(new_functions: List[Dict], output_file: str):
    """Create a file with new function details for Python code generation"""
    
    output_data = {
        'metadata': {
            'generated_at': datetime.now().isoformat(),
            'total_new_functions': len(new_functions),
            'description': 'New security functions suggested by compliance mapper for Python code generation'
        },
        'new_functions': new_functions
    }
    
    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=2)
    
    print(f"Created new functions file: {output_file}")
    print(f"Total new functions: {len(new_functions)}")

def main():
    """Main function to update compliance files and extract new functions"""
    
    # Configuration
    MAPPING_FILE = "mapping_results_20250816_125602.json"
    COMPLIANCE_FILE = "CIS AWS COMPUTE SERVICES BENCHMARK V1.1.0.json"
    
    # Output files
    UPDATED_COMPLIANCE_FILE = f"updated_{COMPLIANCE_FILE}"
    NEW_FUNCTIONS_FILE = f"new_functions_for_codegen_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    print("=== Compliance Files Update Tool ===")
    print(f"Mapping file: {MAPPING_FILE}")
    print(f"Compliance file: {COMPLIANCE_FILE}")
    print()
    
    # Check if files exist
    if not os.path.exists(MAPPING_FILE):
        print(f"Error: {MAPPING_FILE} not found")
        return
    
    if not os.path.exists(COMPLIANCE_FILE):
        print(f"Error: {COMPLIANCE_FILE} not found")
        return
    
    try:
        # Load mapping results
        print("Loading mapping results...")
        mapping_data = load_mapping_results(MAPPING_FILE)
        mapping_results = mapping_data.get('mapping_results', [])
        
        print(f"Loaded {len(mapping_results)} mapping results")
        
        # Update compliance file
        print("\nUpdating compliance file...")
        updated_count = update_compliance_file(
            COMPLIANCE_FILE, 
            mapping_results, 
            UPDATED_COMPLIANCE_FILE
        )
        
        # Extract new functions
        print("\nExtracting new functions...")
        new_functions = extract_new_functions(mapping_results)
        
        # Create new functions file
        print("\nCreating new functions file...")
        create_new_functions_file(new_functions, NEW_FUNCTIONS_FILE)
        
        # Summary
        print("\n=== Update Complete ===")
        print(f"Updated compliance file: {UPDATED_COMPLIANCE_FILE}")
        print(f"New functions file: {NEW_FUNCTIONS_FILE}")
        print(f"Compliance items updated: {updated_count}")
        print(f"New functions extracted: {len(new_functions)}")
        
        # Show some examples of new functions
        if new_functions:
            print("\nExample new functions:")
            for i, func in enumerate(new_functions[:5]):  # Show first 5
                print(f"  {i+1}. {func['function_name']} ({func['service']})")
                print(f"     Compliance: {func['compliance_id']} - {func['compliance_title']}")
                print(f"     API: {func['boto3_api']}")
                print()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
