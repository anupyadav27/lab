#!/usr/bin/env python3
"""
Map fifth NIST control AC-2-b with Azure functions - One control at a time for maximum quality
"""

import json

def map_nist_control_5():
    """Map NIST control AC-2-b: Account Management"""
    
    # Load the NIST compliance file
    with open('nist_subsection_controls_20250829_214518.json', 'r') as f:
        data = json.load(f)
    
    # Load the Azure function database
    with open('azure_final_sdk_service_function_grouped_enhanced.json', 'r') as f:
        functions_db = json.load(f)
    
    print(f"🔧 MAPPING NIST CONTROL AC-2-b")
    print(f"=" * 50)
    
    # Extract all available functions
    all_functions = []
    for service, categories in functions_db.items():
        if isinstance(categories, dict):
            for category, functions in categories.items():
                if isinstance(functions, list):
                    all_functions.extend(functions)
    
    # Find the fifth control (AC-2-b)
    control = None
    for c in data['subsection_controls']:
        if c.get('Id') == 'AC-2-b':
            control = c
            break
    
    if not control:
        print("❌ Control AC-2-b not found!")
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
    
    # This control is about assigning account managers - this is organizational
    if any(keyword in control_description for keyword in ['assign', 'account', 'managers', 'responsibility']):
        # Look for role assignment functions
        appropriate_functions = []
        
        # Search for role assignment functions
        role_functions = [f for f in all_functions if 'role' in f.lower() or 'rbac' in f.lower() or 'assignment' in f.lower()]
        if role_functions:
            # Look for more specific role management functions
            specific_functions = [f for f in role_functions if any(keyword in f.lower() for keyword in ['management', 'assignment', 'rbac'])]
            if specific_functions:
                appropriate_functions.extend(specific_functions[:1])
            else:
                appropriate_functions.extend(role_functions[:1])
        
        if appropriate_functions:
            control['function_names'] = [appropriate_functions[0]]
            control['manual_required'] = False
            control['compliance_level'] = 'fully_automated'
            control['mapping_reasoning'] = f"Control AC-2-b can be verified via Azure API to check role assignments and account manager configurations using {appropriate_functions[0]}"
            control['assessment'] = f"Automated via: {appropriate_functions[0]}"
            
            print(f"\\n✅ AUTOMATED CONTROL")
            print(f"Function: {appropriate_functions[0]}")
            print(f"Assessment: Automated via Azure API")
        else:
            # Fallback to manual if no suitable functions
            control['function_names'] = []
            control['manual_required'] = True
            control['compliance_level'] = 'manual_only'
            control['mapping_reasoning'] = "Control AC-2-b requires manual verification - account manager assignments require organizational review"
            control['assessment'] = "Manual verification required: Account manager assignments require organizational policy review"
            
            print(f"\\n❌ MANUAL CONTROL")
            print(f"Reasoning: Account manager assignments require organizational review")
            print(f"Assessment: Manual verification required")
        
    else:
        # Default to manual for other cases
        control['function_names'] = []
        control['manual_required'] = True
        control['compliance_level'] = 'manual_only'
        control['mapping_reasoning'] = "Control AC-2-b requires manual verification - no suitable Azure functions available"
        control['assessment'] = "Manual verification required: No automated verification possible"
        
        print(f"\\n❌ MANUAL CONTROL")
        print(f"Reasoning: No suitable Azure functions available")
        print(f"Assessment: Manual verification required")
    
    # Save the updated file
    with open('nist_subsection_controls_20250829_214518.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"\\n✅ CONTROL AC-2-b MAPPED!")
    print(f"📊 Result: {'AUTOMATED' if not control.get('manual_required', True) else 'MANUAL'}")
    print(f"✅ File updated: nist_subsection_controls_20250829_214518.json")

if __name__ == "__main__":
    map_nist_control_5()
