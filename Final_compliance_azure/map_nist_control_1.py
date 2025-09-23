#!/usr/bin/env python3
"""
Map first NIST control AC-1-a with Azure functions - One control at a time for maximum quality
"""

import json

def map_nist_control_1():
    """Map NIST control AC-1-a: Policy and Procedures"""
    
    # Load the NIST compliance file
    with open('nist_subsection_controls_20250829_214518.json', 'r') as f:
        data = json.load(f)
    
    # Load the Azure function database
    with open('azure_final_sdk_service_function_grouped_enhanced.json', 'r') as f:
        functions_db = json.load(f)
    
    print(f"🔧 MAPPING NIST CONTROL AC-1-a")
    print(f"=" * 50)
    
    # Extract all available functions
    all_functions = []
    for service, categories in functions_db.items():
        if isinstance(categories, dict):
            for category, functions in categories.items():
                if isinstance(functions, list):
                    all_functions.extend(functions)
    
    # Find the first control (AC-1-a)
    control = None
    for c in data['subsection_controls']:
        if c.get('Id') == 'AC-1-a':
            control = c
            break
    
    if not control:
        print("❌ Control AC-1-a not found!")
        return
    
    print(f"Control: {control.get('Id')} - {control.get('control_title')}")
    print(f"Description: {control.get('control', {}).get('description', '')}")
    
    # Analyze the control requirements
    requirements = control.get('control', {}).get('requirements', [])
    print(f"\\nRequirements:")
    for i, req in enumerate(requirements, 1):
        print(f"  {i}. {req}")
    
    # Determine if this can be automated
    control_description = control.get('control', {}).get('description', '').lower()
    control_title = control.get('control_title', '').lower()
    
    # Policy and procedures are typically manual
    if any(keyword in control_description for keyword in ['policy', 'procedure', 'document', 'disseminate', 'develop']):
        # This is a policy/procedure control - should be manual
        control['function_names'] = []
        control['manual_required'] = True
        control['compliance_level'] = 'manual_only'
        control['mapping_reasoning'] = "Control AC-1-a requires manual verification - Azure functions cannot check policy development, documentation, or dissemination processes"
        control['assessment'] = "Manual verification required: Policy and procedure development requires organizational review and documentation"
        
        print(f"\\n❌ MANUAL CONTROL")
        print(f"Reasoning: Policy and procedure development cannot be automated")
        print(f"Assessment: Manual verification required")
        
    else:
        # Look for appropriate Azure functions
        appropriate_functions = []
        
        # Search for policy-related functions
        policy_functions = [f for f in all_functions if 'policy' in f.lower()]
        if policy_functions:
            appropriate_functions.extend(policy_functions[:1])  # Take first one
        
        if appropriate_functions:
            control['function_names'] = [appropriate_functions[0]]
            control['manual_required'] = False
            control['compliance_level'] = 'fully_automated'
            control['mapping_reasoning'] = f"Control AC-1-a can be verified via Azure API using {appropriate_functions[0]}"
            control['assessment'] = f"Automated via: {appropriate_functions[0]}"
            
            print(f"\\n✅ AUTOMATED CONTROL")
            print(f"Function: {appropriate_functions[0]}")
            print(f"Assessment: Automated via Azure API")
        else:
            control['function_names'] = []
            control['manual_required'] = True
            control['compliance_level'] = 'manual_only'
            control['mapping_reasoning'] = "Control AC-1-a requires manual verification - no suitable Azure functions available"
            control['assessment'] = "Manual verification required: No automated verification possible"
            
            print(f"\\n❌ MANUAL CONTROL")
            print(f"Reasoning: No suitable Azure functions available")
            print(f"Assessment: Manual verification required")
    
    # Save the updated file
    with open('nist_subsection_controls_20250829_214518.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"\\n✅ CONTROL AC-1-a MAPPED!")
    print(f"📊 Result: {'AUTOMATED' if not control.get('manual_required', True) else 'MANUAL'}")
    print(f"✅ File updated: nist_subsection_controls_20250829_214518.json")

if __name__ == "__main__":
    map_nist_control_1()
