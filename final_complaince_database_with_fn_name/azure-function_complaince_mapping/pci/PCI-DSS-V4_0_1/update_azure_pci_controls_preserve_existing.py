#!/usr/bin/env python3
"""
Update Azure PCI DSS Controls with Mapping Results - Preserve Existing Functions

This script updates the original Azure PCI DSS controls file with the final mapping results
while PRESERVING all existing functions and ADDING new functions for enhanced coverage.
"""

import json
import os
from datetime import datetime
from pathlib import Path

def load_original_azure_pci_controls(file_path):
    """Load the original Azure PCI DSS controls file"""
    
    print(f"📖 Loading original Azure PCI DSS controls from: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            controls = json.load(f)
        print(f"✅ Loaded {len(controls)} Azure PCI DSS controls")
        return controls
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ JSON decode error: {e}")
        return None

def load_mapping_results(file_path):
    """Load the mapping results file"""
    
    print(f"📖 Loading mapping results from: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            mapping_data = json.load(f)
        print(f"✅ Loaded mapping results with {len(mapping_data.get('mapping_results', []))} mappings")
        return mapping_data
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ JSON decode error: {e}")
        return None

def merge_function_lists(existing_functions, mapping_result):
    """Merge existing functions with new functions from mapping results"""
    
    # Start with existing functions
    merged_functions = existing_functions.copy() if existing_functions else []
    
    # Add existing functions from mapping results
    existing_mapped = mapping_result.get('existing_functions_mapped', [])
    for func in existing_mapped:
        if func not in merged_functions:
            merged_functions.append(func)
    
    # Add new functions from mapping results
    new_functions = mapping_result.get('new_functions_needed', [])
    for func in new_functions:
        function_name = func.get('name', '')
        if function_name and function_name not in merged_functions:
            merged_functions.append(function_name)
    
    return merged_functions

def update_azure_pci_controls_preserve_existing(original_controls, mapping_data):
    """Update original Azure PCI DSS controls while preserving existing functions"""
    
    print("🔄 Updating Azure PCI DSS controls while preserving existing functions...")
    
    # Create a mapping lookup for quick access
    mapping_lookup = {}
    for mapping in mapping_data.get('mapping_results', []):
        control_id = mapping.get('compliance_id', '')
        mapping_lookup[control_id] = mapping
    
    updated_controls = []
    updated_count = 0
    total_existing_functions = 0
    total_new_functions = 0
    
    for control in original_controls:
        control_id = control.get('RequirementID', '')
        existing_functions = control.get('function_names', [])
        
        # Count existing functions
        total_existing_functions += len(existing_functions)
        
        # Check if we have mapping results for this control
        if control_id in mapping_lookup:
            mapping_result = mapping_lookup[control_id]
            
            # Merge existing functions with new ones
            merged_functions = merge_function_lists(existing_functions, mapping_result)
            
            # Count new functions added
            new_functions_added = len(merged_functions) - len(existing_functions)
            total_new_functions += new_functions_added
            
            # Update the control with merged function list
            updated_control = control.copy()
            updated_control['function_names'] = merged_functions
            
            updated_controls.append(updated_control)
            updated_count += 1
            
            # Print progress for controls with changes
            if new_functions_added > 0:
                print(f"  ✅ Updated {control_id}: {len(existing_functions)} existing + {new_functions_added} new = {len(merged_functions)} total")
        else:
            # Keep original control without changes
            updated_controls.append(control)
    
    print(f"✅ Updated {updated_count} controls with mapping results")
    print(f"📊 Function Summary:")
    print(f"  - Existing functions preserved: {total_existing_functions}")
    print(f"  - New functions added: {total_new_functions}")
    print(f"  - Total functions after update: {total_existing_functions + total_new_functions}")
    
    return updated_controls

def create_summary_report(original_controls, updated_controls, mapping_data):
    """Create a summary report of the update process"""
    
    print("📊 Creating summary report...")
    
    # Calculate statistics
    total_controls = len(original_controls)
    controls_with_functions = sum(1 for c in updated_controls if c.get('function_names'))
    controls_without_functions = total_controls - controls_with_functions
    
    # Count total functions
    total_functions = sum(len(c.get('function_names', [])) for c in updated_controls)
    
    # Count original functions
    original_functions = sum(len(c.get('function_names', [])) for c in original_controls)
    
    # Coverage statistics from mapping data
    mapping_stats = mapping_data.get('processing_stats', {})
    
    summary = {
        "update_metadata": {
            "generated_at": datetime.now().isoformat(),
            "original_file": "PCI-DSS-v4_0_1 copy.json",
            "mapping_file": "pci_mapping_results_20250823_212026.json",
            "update_type": "function_mapping_integration_preserve_existing"
        },
        "control_statistics": {
            "total_controls": total_controls,
            "controls_with_functions": controls_with_functions,
            "controls_without_functions": controls_without_functions,
            "coverage_percentage": round((controls_with_functions / total_controls) * 100, 2)
        },
        "function_statistics": {
            "original_functions": original_functions,
            "total_functions_after_update": total_functions,
            "new_functions_added": total_functions - original_functions,
            "improvement_percentage": round(((total_functions - original_functions) / original_functions) * 100, 2) if original_functions > 0 else 0
        },
        "mapping_statistics": {
            "total_items_processed": mapping_stats.get('total_items', 0),
            "mapped_complete": mapping_stats.get('mapped_complete', 0),
            "mapped_partial": mapping_stats.get('mapped_partial', 0),
            "mapped_none": mapping_stats.get('mapped_none', 0),
            "new_functions_suggested": mapping_stats.get('new_functions_suggested', 0)
        }
    }
    
    return summary

def save_updated_controls(updated_controls, output_path):
    """Save the updated controls to a new file"""
    
    print(f"💾 Saving updated Azure PCI DSS controls to: {output_path}")
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(updated_controls, f, indent=2, ensure_ascii=False)
        print(f"✅ Successfully saved updated controls")
        return True
    except Exception as e:
        print(f"❌ Error saving file: {e}")
        return False

def save_summary_report(summary, output_path):
    """Save the summary report"""
    
    print(f"💾 Saving summary report to: {output_path}")
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        print(f"✅ Successfully saved summary report")
        return True
    except Exception as e:
        print(f"❌ Error saving summary: {e}")
        return False

def main():
    """Main function"""
    
    print("🔄 Update Azure PCI DSS Controls - Preserve Existing Functions")
    print("=" * 70)
    
    # File paths
    original_file = "PCI-DSS-v4_0_1 copy.json"
    mapping_file = "output/pci_mapping_results_20250823_212026.json"
    
    # Load original controls
    original_controls = load_original_azure_pci_controls(original_file)
    if not original_controls:
        return
    
    # Load mapping results
    mapping_data = load_mapping_results(mapping_file)
    if not mapping_data:
        return
    
    # Update controls while preserving existing functions
    updated_controls = update_azure_pci_controls_preserve_existing(original_controls, mapping_data)
    
    # Create summary report
    summary = create_summary_report(original_controls, updated_controls, mapping_data)
    
    # Generate output filenames with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    updated_file = f"azure_pci_dss_controls_updated_preserve_{timestamp}.json"
    summary_file = f"azure_pci_dss_controls_update_summary_preserve_{timestamp}.json"
    
    # Save updated controls
    if save_updated_controls(updated_controls, updated_file):
        print(f"📁 Updated controls saved to: {updated_file}")
    
    # Save summary report
    if save_summary_report(summary, summary_file):
        print(f"📁 Summary report saved to: {summary_file}")
    
    # Print final summary
    print(f"\n🎯 Update Complete!")
    print(f"📊 Summary:")
    print(f"  - Total Controls: {summary['control_statistics']['total_controls']}")
    print(f"  - Controls with Functions: {summary['control_statistics']['controls_with_functions']}")
    print(f"  - Coverage: {summary['control_statistics']['coverage_percentage']}%")
    print(f"  - Original Functions: {summary['function_statistics']['original_functions']}")
    print(f"  - New Functions Added: {summary['function_statistics']['new_functions_added']}")
    print(f"  - Total Functions After Update: {summary['function_statistics']['total_functions_after_update']}")
    print(f"  - Improvement: {summary['function_statistics']['improvement_percentage']}%")
    
    print(f"\n📁 Files created:")
    print(f"  - {updated_file}")
    print(f"  - {summary_file}")

if __name__ == "__main__":
    main()
