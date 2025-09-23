#!/usr/bin/env python3
"""
Clean up the EKS benchmark output file by removing old function_names fields
and other redundant data.
"""

import json
from datetime import datetime

def cleanup_control(control):
    """Clean up a single control by removing redundant fields"""
    # Remove old function_names field if it exists
    if "function_names" in control:
        del control["function_names"]
    
    return control

def main():
    """Main function to clean up the EKS benchmark file"""
    input_file = "/Users/apple/Desktop/compliance_Database/final_complaince_database_with_fn_name/aws_function_complaince_mapping/CIS_AMAZON_ELASTIC_KUBERNETES_SERVICE_(EKS)_BENCHMARK_V1.7.0_PDF/CIS_EKS_BENCHMARK_V1.7.0_PDF_updated_20250825_184041_updated_20250829_223332.json"
    
    # Load the EKS benchmark file
    with open(input_file, 'r') as f:
        controls = json.load(f)
    
    print(f"🧹 Cleaning up {len(controls)} controls in CIS EKS BENCHMARK V1.7.0...")
    
    # Clean up each control
    cleaned_controls = []
    for i, control in enumerate(controls, 1):
        print(f"Cleaning control {i}/{len(controls)}: {control.get('id', 'Unknown')}")
        cleaned_control = cleanup_control(control)
        cleaned_controls.append(cleaned_control)
    
    # Generate output filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = input_file.replace('.json', f'_cleaned_{timestamp}.json')
    
    # Save cleaned controls
    with open(output_file, 'w') as f:
        json.dump(cleaned_controls, f, indent=2)
    
    print(f"✅ Successfully cleaned {len(controls)} controls!")
    print(f"📁 Output saved to: {output_file}")
    
    # Show sample of cleaned controls
    print("\n📋 Sample Cleaned Controls:")
    for i, control in enumerate(cleaned_controls[:3], 1):
        print(f"\n{i}. ID: {control['id']}")
        print(f"   Title: {control['title']}")
        print(f"   Function: {control['function_name']}")
        print(f"   Coverage: {control['coverage']}%")
        if 'manual_effort' in control:
            print(f"   Manual Effort: {control['manual_effort']}")
        if 'new_function_suggestion' in control:
            print(f"   New Function Suggestion: {control['new_function_suggestion']}")
        print(f"   Data Status: {control['data_status']}")

if __name__ == "__main__":
    main()
