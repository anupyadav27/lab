#!/usr/bin/env python3
"""
Update NIST Controls with Mapping Results

This script updates the original NIST controls file with the final mapping results
that include both existing functions and newly added functions for full coverage.
"""

import json
import os
from datetime import datetime
from pathlib import Path

def load_original_nist_controls(file_path):
    """Load the original NIST controls file"""
    
    print(f"📖 Loading original NIST controls from: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            controls = json.load(f)
        print(f"✅ Loaded {len(controls)} NIST controls")
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

def create_function_list_from_mapping(mapping_result):
    """Create a comprehensive function list from mapping results"""
    
    function_list = []
    
    # Add existing functions
    existing_functions = mapping_result.get('existing_functions_mapped', [])
    for func in existing_functions:
        function_list.append({
            "name": func,
            "type": "existing",
            "source": "prowler_database"
        })
    
    # Add new functions
    new_functions = mapping_result.get('new_functions_needed', [])
    for func in new_functions:
        function_list.append({
            "name": func.get('name', ''),
            "type": "new",
            "source": "ai_suggested",
            "boto3_api": func.get('boto3_api', ''),
            "service": func.get('service', ''),
            "rationale": func.get('rationale', '')
        })
    
    return function_list

def update_nist_controls_with_mapping(original_controls, mapping_data):
    """Update original NIST controls with mapping results"""
    
    print("🔄 Updating NIST controls with mapping results...")
    
    # Create a mapping lookup for quick access
    mapping_lookup = {}
    for mapping in mapping_data.get('mapping_results', []):
        control_id = mapping.get('compliance_id', '')
        mapping_lookup[control_id] = mapping
    
    updated_controls = []
    updated_count = 0
    
    for control in original_controls:
        control_id = control.get('control_id', '')
        
        # Check if we have mapping results for this control
        if control_id in mapping_lookup:
            mapping_result = mapping_lookup[control_id]
            
            # Create comprehensive function list
            function_list = create_function_list_from_mapping(mapping_result)
            
            # Update the control with function list and mapping metadata
            updated_control = control.copy()
            updated_control['function_names'] = function_list
            updated_control['mapping_metadata'] = {
                'coverage_assessment': mapping_result.get('coverage_assessment', 'none'),
                'mapping_notes': mapping_result.get('mapping_notes', ''),
                'total_functions': len(function_list),
                'existing_functions': len([f for f in function_list if f['type'] == 'existing']),
                'new_functions': len([f for f in function_list if f['type'] == 'new']),
                'last_updated': datetime.now().isoformat()
            }
            
            updated_controls.append(updated_control)
            updated_count += 1
            
            # Print progress for controls with functions
            if function_list:
                print(f"  ✅ Updated {control_id}: {len(function_list)} functions ({len([f for f in function_list if f['type'] == 'existing'])} existing, {len([f for f in function_list if f['type'] == 'new'])} new)")
        else:
            # Keep original control without changes
            updated_controls.append(control)
    
    print(f"✅ Updated {updated_count} controls with mapping results")
    return updated_controls

def create_summary_report(original_controls, updated_controls, mapping_data):
    """Create a summary report of the update process"""
    
    print("📊 Creating summary report...")
    
    # Calculate statistics
    total_controls = len(original_controls)
    controls_with_functions = sum(1 for c in updated_controls if c.get('function_names'))
    controls_without_functions = total_controls - controls_with_functions
    
    total_functions = 0
    total_existing_functions = 0
    total_new_functions = 0
    
    for control in updated_controls:
        if control.get('function_names'):
            for func in control['function_names']:
                total_functions += 1
                if func.get('type') == 'existing':
                    total_existing_functions += 1
                elif func.get('type') == 'new':
                    total_new_functions += 1
    
    # Coverage statistics from mapping data
    mapping_stats = mapping_data.get('processing_stats', {})
    
    summary = {
        "update_metadata": {
            "generated_at": datetime.now().isoformat(),
            "original_file": "nist_controls.json 14-28-15-654.json",
            "mapping_file": "nist_mapping_results_20250823_115049.json",
            "update_type": "function_mapping_integration"
        },
        "control_statistics": {
            "total_controls": total_controls,
            "controls_with_functions": controls_with_functions,
            "controls_without_functions": controls_without_functions,
            "coverage_percentage": round((controls_with_functions / total_controls) * 100, 2)
        },
        "function_statistics": {
            "total_functions": total_functions,
            "existing_functions": total_existing_functions,
            "new_functions": total_new_functions,
            "function_distribution": {
                "existing_percentage": round((total_existing_functions / total_functions) * 100, 2) if total_functions > 0 else 0,
                "new_percentage": round((total_new_functions / total_functions) * 100, 2) if total_functions > 0 else 0
            }
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
    
    print(f"💾 Saving updated NIST controls to: {output_path}")
    
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
    
    print("🔄 Update NIST Controls with Mapping Results")
    print("=" * 60)
    
    # File paths
    original_file = "nist_controls.json 14-28-15-654.json"
    mapping_file = "output/nist_mapping_results_20250823_115049.json"
    
    # Load original controls
    original_controls = load_original_nist_controls(original_file)
    if not original_controls:
        return
    
    # Load mapping results
    mapping_data = load_mapping_results(mapping_file)
    if not mapping_data:
        return
    
    # Update controls with mapping results
    updated_controls = update_nist_controls_with_mapping(original_controls, mapping_data)
    
    # Create summary report
    summary = create_summary_report(original_controls, updated_controls, mapping_data)
    
    # Generate output filenames with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    updated_file = f"nist_controls_updated_{timestamp}.json"
    summary_file = f"nist_controls_update_summary_{timestamp}.json"
    
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
    print(f"  - Total Functions: {summary['function_statistics']['total_functions']}")
    print(f"  - Existing Functions: {summary['function_statistics']['existing_functions']}")
    print(f"  - New Functions: {summary['function_statistics']['new_functions']}")
    
    print(f"\n📁 Files created:")
    print(f"  - {updated_file}")
    print(f"  - {summary_file}")

if __name__ == "__main__":
    main()
