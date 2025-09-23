#!/usr/bin/env python3
"""
GCP CIS Compliance Processor 
Processes the original CIS file with mapping results to create an updated compliance file.
"""

import json
import os
import sys
from datetime import datetime

def load_json_file(file_path):
    """Load JSON file with error handling"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ JSON decode error in {file_path}: {e}")
        return None

def process_compliance_with_mapping(cis_file, mapping_file, output_file):
    """Process CIS compliance file with mapping results"""
    print(f"🔄 Processing CIS compliance file with mapping results...")
    
    # Load the original CIS data
    cis_data = load_json_file(cis_file)
    if not cis_data:
        return False
    
    # Load the mapping results
    mapping_data = load_json_file(mapping_file)
    if not mapping_data:
        return False
    
    print(f"📊 Loaded {len(cis_data)} controls from CIS file")
    print(f"📊 Loaded {len(mapping_data)} mapping results")
    
    # Create a mapping dictionary for quick lookup
    mapping_dict = {}
    for mapping in mapping_data:
        compliance_id = mapping.get('compliance_id', '')
        mapping_dict[compliance_id] = mapping
    
    # Process each control
    updated_controls = []
    controls_updated = 0
    
    for control in cis_data:
        control_id = control.get('id', 'unknown')
        
        # Clean unwanted metadata fields (if any exist)
        fields_to_remove = ['mapping_metadata', 'coverage_assessment', 'mapping_notes', 'mapping_source']
        for field in fields_to_remove:
            if field in control:
                del control[field]
        
        # Get existing function names
        existing_functions = control.get('function_names', [])
        if isinstance(existing_functions, str):
            existing_functions = [existing_functions]
        
        # Get new functions from mapping
        new_functions = []
        if control_id in mapping_dict:
            mapping_entry = mapping_dict[control_id]
            
            # Extract function names from new_functions_needed
            new_functions_needed = mapping_entry.get('new_functions_needed', [])
            for func_obj in new_functions_needed:
                if isinstance(func_obj, dict) and 'function_name' in func_obj:
                    new_functions.append(func_obj['function_name'])
                elif isinstance(func_obj, str):
                    new_functions.append(func_obj)
            
            # Also get existing mapped functions
            existing_mapped = mapping_entry.get('existing_functions_mapped', [])
            new_functions.extend(existing_mapped)
            
            print(f"  📝 Control {control_id}: {len(existing_functions)} existing + {len(new_functions)} new functions")
        
        # Combine and deduplicate
        all_functions = list(set(existing_functions + new_functions))
        all_functions = [f for f in all_functions if f and f.strip()]
        
        if all_functions:
            control['function_names'] = all_functions
            controls_updated += 1
        
        updated_controls.append(control)
    
    # Save the updated file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if not output_file:
        base_name = os.path.splitext(os.path.basename(cis_file))[0]
        output_file = f"{base_name}_updated_{timestamp}.json"
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(updated_controls, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Successfully updated {controls_updated} controls")
        print(f"💾 Saved to: {output_file}")
        return True
        
    except Exception as e:
        print(f"❌ Error saving file: {e}")
        return False

def main():
    """Main function"""
    # Define file paths for this specific directory
    current_dir = os.getcwd()
    cis_file = "CIS_GOOGLE_KUBERNETES_ENGINE(GKE)_AUTOPILOT_BENCHMARK_V1.2.0.json"
    mapping_file = "gcp_mapping_results_20250821_055421.json"
    
    # Check if files exist
    if not os.path.exists(cis_file):
        print(f"❌ CIS file not found: {cis_file}")
        print(f"Current directory: {current_dir}")
        return
    
    if not os.path.exists(mapping_file):
        print(f"❌ Mapping file not found: {mapping_file}")
        print(f"Current directory: {current_dir}")
        return
    
    # Generate output filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"CIS_GKE_AUTOPILOT_V1_2_0_updated_{timestamp}.json"
    
    print(f"🎯 Processing GCP CIS Compliance Update")
    print(f"📁 CIS File: {cis_file}")
    print(f"📁 Mapping File: {mapping_file}")
    print(f"💾 Output File: {output_file}")
    print("=" * 60)
    
    success = process_compliance_with_mapping(cis_file, mapping_file, output_file)
    
    if success:
        print("=" * 60)
        print("🎉 Processing completed successfully!")
        print(f"📂 Updated file: {output_file}")
    else:
        print("❌ Processing failed!")

if __name__ == "__main__":
    main()
