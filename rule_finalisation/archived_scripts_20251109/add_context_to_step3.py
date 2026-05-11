#!/usr/bin/env python3
"""
ADD FULL CONTEXT TO STEP 3 FUNCTIONS
- Show which compliance requirements they match
- Show what is expected
- Then analyze if they can be covered
"""
import json
import pandas as pd

print("=" * 100)
print("🔍 ADDING FULL CONTEXT TO STEP 3 FUNCTIONS")
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

# Build complete context for all functions
print("Building complete compliance context...")
function_contexts = {}

for _, row in df.iterrows():
    if pd.notna(row.get('aws_uniform_format')):
        funcs = str(row['aws_uniform_format']).split(';')
        for func in funcs:
            func = func.strip()
            if func and func.startswith('aws.'):
                if func not in function_contexts:
                    function_contexts[func] = []
                
                # Add this compliance requirement
                function_contexts[func].append({
                    'compliance_id': str(row.get('unique_compliance_id', '')),
                    'framework': str(row.get('compliance_framework', '')),
                    'framework_id': str(row.get('framework_id', '')),
                    'requirement_id': str(row.get('requirement_id', '')),
                    'requirement_name': str(row.get('requirement_name', ''))[:100],
                    'requirement_description': str(row.get('requirement_description', ''))[:200],
                    'section': str(row.get('section', '')),
                    'service': str(row.get('service', ''))
                })

print(f"✓ Built context for {len(function_contexts)} functions")

# Now update Step 3 with full context
print("\nAdding context to Step 3 functions...")
total_step3 = 0
step3_with_context = {}

for service, data in mapping.items():
    if service == 'metadata':
        continue
    
    step3_original = data.get('step3_needs_development', [])
    if not step3_original:
        continue
    
    # Convert to list with context
    step3_enhanced = []
    
    for func in step3_original:
        context = function_contexts.get(func, [])
        
        # Create detailed entry
        func_detail = {
            'function': func,
            'compliance_requirements': []
        }
        
        # Add all compliance requirements
        for req in context:
            func_detail['compliance_requirements'].append({
                'framework': req['framework'],
                'requirement': req['requirement_name'],
                'description': req['requirement_description'],
                'what_is_expected': f"Check: {req['requirement_name']} - Ensure: {req['requirement_description']}"
            })
        
        # If no context found, note it
        if not func_detail['compliance_requirements']:
            func_detail['compliance_requirements'].append({
                'note': 'No compliance requirement found - may be orphaned function'
            })
        
        step3_enhanced.append(func_detail)
        total_step3 += 1
    
    # Replace simple list with detailed list
    data['step3_needs_development_with_context'] = step3_enhanced
    step3_with_context[service] = step3_enhanced

# Now analyze if any Step 3 can be covered
print("\nAnalyzing Step 3 for potential coverage...")
potential_coverage = {}

# Get all available rules
all_rules = set()
for service, data in mapping.items():
    if service != 'metadata':
        all_rules.update(data.get('available_rules', []))

for service, step3_funcs in step3_with_context.items():
    service_potential = []
    
    for func_detail in step3_funcs:
        func = func_detail['function']
        requirements = func_detail['compliance_requirements']
        
        # Analyze based on requirements
        potential_rules = []
        
        for req in requirements:
            if 'description' not in req:
                continue
                
            desc = req['description'].lower()
            
            # Look for patterns that suggest existing rules could cover
            if 'audit' in desc or 'log' in desc:
                matching = [r for r in all_rules if 'cloudtrail' in r or 'log' in r]
                potential_rules.extend(matching[:2])
            
            if 'encrypt' in desc:
                matching = [r for r in all_rules if 'encrypt' in r or 'kms' in r]
                potential_rules.extend(matching[:2])
            
            if 'access' in desc and ('least' in desc or 'privilege' in desc):
                matching = [r for r in all_rules if 'privilege' in r or 'policy' in r]
                potential_rules.extend(matching[:2])
            
            if 'backup' in desc or 'retention' in desc:
                matching = [r for r in all_rules if 'backup' in r or 'retention' in r]
                potential_rules.extend(matching[:2])
        
        if potential_rules:
            func_detail['potential_coverage'] = list(set(potential_rules))[:3]
            func_detail['coverage_analysis'] = "Could potentially be covered by existing rules based on requirements"
            service_potential.append(func)
    
    if service_potential:
        potential_coverage[service] = len(service_potential)

# Save updated mapping
print("\nSaving enhanced mapping...")
with open(MAPPING_FILE, 'w') as f:
    json.dump(mapping, f, indent=2)

# Create a summary report
REPORT_FILE = MAPPING_FILE.replace('.json', '_STEP3_CONTEXT_REPORT.md')
with open(REPORT_FILE, 'w') as f:
    f.write("# Step 3 Functions - Full Context Report\n\n")
    f.write(f"Total Step 3 Functions: {total_step3}\n\n")
    
    # Show examples from each service
    for service, step3_funcs in step3_with_context.items():
        f.write(f"\n## {service.upper()}\n\n")
        
        # Show first 3 functions with full context
        for func_detail in step3_funcs[:3]:
            f.write(f"### {func_detail['function']}\n\n")
            
            if func_detail['compliance_requirements']:
                for req in func_detail['compliance_requirements']:
                    if 'framework' in req:
                        f.write(f"**Framework:** {req['framework']}\n")
                        f.write(f"**Requirement:** {req['requirement']}\n")
                        f.write(f"**Description:** {req['description']}\n")
                        f.write(f"**Expected:** {req['what_is_expected']}\n\n")
            
            if 'potential_coverage' in func_detail:
                f.write("**Potential Coverage:**\n")
                for rule in func_detail['potential_coverage']:
                    f.write(f"- {rule}\n")
                f.write(f"\n{func_detail['coverage_analysis']}\n")
            
            f.write("\n---\n\n")
        
        if len(step3_funcs) > 3:
            f.write(f"*... plus {len(step3_funcs) - 3} more functions*\n\n")

print(f"\n✓ Context report saved to: {REPORT_FILE}")

# Show summary
print("\n" + "=" * 100)
print("STEP 3 CONTEXT SUMMARY")
print("=" * 100)
print(f"\n✓ Added context to {total_step3} Step 3 functions")
print(f"✓ Each function now shows:")
print("  - Which compliance frameworks require it")
print("  - What the requirement expects")
print("  - Potential existing rules that could cover it")

if potential_coverage:
    print(f"\n✓ Found potential coverage opportunities:")
    total_potential = sum(potential_coverage.values())
    for service, count in potential_coverage.items():
        print(f"  - {service}: {count} functions could potentially be covered")
    print(f"\nTotal: {total_potential} Step 3 functions might be coverable!")

print("\n✓ Updated file: " + MAPPING_FILE)
print("✓ Each Step 3 function now has 'step3_needs_development_with_context'")
print("\n" + "=" * 100)

# Show a sample
print("\nSAMPLE STEP 3 WITH CONTEXT:")
print("-" * 80)

# Find a good example
for service, step3_funcs in step3_with_context.items():
    if step3_funcs:
        example = step3_funcs[0]
        print(f"\nFunction: {example['function']}")
        if example['compliance_requirements']:
            req = example['compliance_requirements'][0]
            if 'framework' in req:
                print(f"Framework: {req['framework']}")
                print(f"Requirement: {req['requirement']}")
                print(f"What's Expected: {req['what_is_expected']}")
        
        if 'potential_coverage' in example:
            print(f"\nCould be covered by:")
            for rule in example['potential_coverage'][:2]:
                print(f"  → {rule}")
        break

print("\n" + "=" * 100)
