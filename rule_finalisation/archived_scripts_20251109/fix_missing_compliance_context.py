#!/usr/bin/env python3
"""
Fix missing compliance context - ensure ALL functions have their requirements from CSV
"""
import json
import pandas as pd

print("=" * 100)
print("🔧 FIXING MISSING COMPLIANCE CONTEXT")
print("=" * 100)
print()

# Files
MAPPING_FILE = "/Users/apple/Desktop/compliance_Database/rule_finalisation/service_mappings/AWS_ONE_TO_ONE_MAPPING_BULLETPROOF_COMPLETE.json"
COMPLIANCE_CSV = "/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule/consolidated_compliance_rules_FINAL.csv"

# Load data
print("Loading data...")
with open(MAPPING_FILE, 'r') as f:
    mapping = json.load(f)

df = pd.read_csv(COMPLIANCE_CSV)

# Build complete function -> requirements mapping
print("Building complete function context from CSV...")
function_requirements = {}

for _, row in df.iterrows():
    if pd.notna(row.get('aws_uniform_format')):
        funcs = str(row['aws_uniform_format']).split(';')
        
        # Get all relevant columns
        context = {
            'compliance_id': str(row.get('unique_compliance_id', '')),
            'framework': str(row.get('compliance_framework', '')),
            'framework_id': str(row.get('framework_id', '')),
            'requirement_id': str(row.get('requirement_id', '')),
            'requirement_name': str(row.get('requirement_name', '')),
            'requirement_description': str(row.get('requirement_description', '')),
            'section': str(row.get('section', '')),
            'service': str(row.get('service', '')),
            'automation_type': str(row.get('automation_type', ''))
        }
        
        # Fix description if it's 'nan'
        if context['requirement_description'] == 'nan' or not context['requirement_description']:
            # Try other columns
            for col in ['Description', 'description']:
                if col in df.columns:
                    val = str(row.get(col, ''))
                    if val and val != 'nan':
                        context['requirement_description'] = val
                        break
            
            # If still no description, use requirement name
            if context['requirement_description'] == 'nan':
                context['requirement_description'] = context['requirement_name']
        
        # Add to each function
        for func in funcs:
            func = func.strip()
            if func and func.startswith('aws.'):
                if func not in function_requirements:
                    function_requirements[func] = []
                function_requirements[func].append(context)

print(f"✓ Built requirements for {len(function_requirements)} functions")

# Now fix ALL Step 3 functions
print("\nFixing Step 3 functions with missing context...")
fixed_count = 0
missing_in_csv = []

for service, data in mapping.items():
    if service == 'metadata':
        continue
    
    step3 = data.get('step3_needs_development', [])
    if not step3:
        continue
    
    # Create properly enhanced Step 3
    enhanced_step3 = []
    
    for func in step3:
        requirements = function_requirements.get(func, [])
        
        entry = {
            'function': func,
            'compliance_requirements': []
        }
        
        if requirements:
            # Add all requirements
            for req in requirements[:10]:  # Limit to 10 for readability
                entry['compliance_requirements'].append({
                    'framework': req['framework'],
                    'requirement': req['requirement_name'],
                    'description': req['requirement_description'][:200],
                    'what_is_expected': f"Ensure: {req['requirement_name']} - {req['requirement_description'][:150]}..."
                })
            
            if len(requirements) > 10:
                entry['compliance_requirements'].append({
                    'note': f'... plus {len(requirements) - 10} more compliance requirements'
                })
            
            fixed_count += 1
        else:
            # Function not found in CSV
            missing_in_csv.append(func)
            entry['compliance_requirements'].append({
                'note': 'ORPHANED FUNCTION - Not found in compliance CSV - may need removal',
                'action_needed': 'Verify if this function is still needed'
            })
        
        # Add coverage analysis
        entry['coverage_analysis'] = {
            'likelihood': 'UNKNOWN',
            'potential_rules': []
        }
        
        enhanced_step3.append(entry)
    
    # Update mapping
    data['step3_needs_development_enhanced'] = enhanced_step3

# Save fixed mapping
print("\nSaving fixed mapping...")
with open(MAPPING_FILE, 'w') as f:
    json.dump(mapping, f, indent=2)

# Report
print("\n" + "=" * 100)
print("FIXING COMPLETE")
print("=" * 100)
print()
print(f"✓ Fixed {fixed_count} Step 3 functions with proper compliance context")

if missing_in_csv:
    print(f"\n⚠️  Found {len(missing_in_csv)} ORPHANED functions not in CSV:")
    for func in missing_in_csv[:10]:
        print(f"  - {func}")
    if len(missing_in_csv) > 10:
        print(f"  ... and {len(missing_in_csv) - 10} more")
    print("\nThese may be:")
    print("  - Old functions that were removed from compliance")
    print("  - Typos in function names")
    print("  - Functions that need to be removed from mapping")

# Create detailed report of orphaned functions
if missing_in_csv:
    with open("ORPHANED_FUNCTIONS_REPORT.md", 'w') as f:
        f.write("# Orphaned Functions Report\n\n")
        f.write(f"Found {len(missing_in_csv)} functions in mapping but not in compliance CSV:\n\n")
        
        # Group by service
        by_service = {}
        for func in missing_in_csv:
            service = func.split('.')[1] if '.' in func else 'unknown'
            if service not in by_service:
                by_service[service] = []
            by_service[service].append(func)
        
        for service, funcs in sorted(by_service.items()):
            f.write(f"\n## {service} ({len(funcs)} functions)\n\n")
            for func in sorted(funcs):
                f.write(f"- {func}\n")
    
    print(f"\n✓ Orphaned functions report: ORPHANED_FUNCTIONS_REPORT.md")

print("\n✓ All Step 3 functions now have proper compliance context from CSV")
print("✓ Functions not in CSV are clearly marked as ORPHANED")
print()
print("=" * 100)
