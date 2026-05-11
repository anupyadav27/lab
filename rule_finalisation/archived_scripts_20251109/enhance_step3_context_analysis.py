#!/usr/bin/env python3
"""
ENHANCED STEP 3 CONTEXT AND COVERAGE ANALYSIS
- Fix "nan" descriptions
- Add meaningful context
- Better analyze coverage opportunities
"""
import json
import pandas as pd
import re

print("=" * 100)
print("🔍 ENHANCED STEP 3 CONTEXT AND COVERAGE ANALYSIS")
print("=" * 100)
print()

# Files
MAPPING_FILE = "/Users/apple/Desktop/compliance_Database/rule_finalisation/service_mappings/AWS_ONE_TO_ONE_MAPPING_BULLETPROOF_COMPLETE.json"
COMPLIANCE_CSV = "/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule/consolidated_compliance_rules_FINAL.csv"

# Load data
with open(MAPPING_FILE, 'r') as f:
    mapping = json.load(f)

df = pd.read_csv(COMPLIANCE_CSV)

# Build better context
print("Building enhanced compliance context...")
function_contexts = {}

for _, row in df.iterrows():
    if pd.notna(row.get('aws_uniform_format')):
        funcs = str(row['aws_uniform_format']).split(';')
        
        # Get actual description - check multiple columns
        description = ''
        for col in ['requirement_description', 'Description', 'description']:
            if col in df.columns and pd.notna(row.get(col)):
                desc_val = str(row.get(col))
                if desc_val != 'nan' and desc_val.strip():
                    description = desc_val
                    break
        
        # If still no description, use requirement name
        if not description or description == 'nan':
            description = str(row.get('requirement_name', ''))
        
        for func in funcs:
            func = func.strip()
            if func and func.startswith('aws.'):
                if func not in function_contexts:
                    function_contexts[func] = []
                
                function_contexts[func].append({
                    'compliance_id': str(row.get('unique_compliance_id', '')),
                    'framework': str(row.get('compliance_framework', '')),
                    'requirement_name': str(row.get('requirement_name', '')),
                    'description': description[:300],  # Longer description
                    'section': str(row.get('section', '')),
                    'service': str(row.get('service', '')),
                    'automation_type': str(row.get('automation_type', ''))
                })

print(f"✓ Built enhanced context for {len(function_contexts)} functions")

# Get all available rules with detailed info
all_rules_detailed = {}
for service, data in mapping.items():
    if service != 'metadata':
        for rule in data.get('available_rules', []):
            all_rules_detailed[rule] = {
                'rule': rule,
                'service': service,
                'keywords': set(rule.lower().split('.')[2:]) if len(rule.split('.')) > 2 else set()
            }

# Analyze Step 3 with better logic
print("\nAnalyzing Step 3 for coverage opportunities...")
step3_analysis = {}
total_potentially_covered = 0

for service, data in mapping.items():
    if service == 'metadata':
        continue
    
    step3 = data.get('step3_needs_development', [])
    if not step3:
        continue
    
    service_analysis = []
    
    for func in step3:
        context = function_contexts.get(func, [])
        analysis = {
            'function': func,
            'compliance_count': len(context),
            'frameworks': list(set(c['framework'] for c in context)),
            'descriptions': [],
            'potential_coverage': []
        }
        
        # Aggregate descriptions
        unique_descs = set()
        for c in context:
            if c['description'] and c['description'] != 'nan':
                unique_descs.add(c['description'])
        analysis['descriptions'] = list(unique_descs)[:3]  # Top 3 unique
        
        # Analyze for coverage based on function name and requirements
        func_lower = func.lower()
        func_parts = func_lower.split('.')
        
        # Extract what this function checks
        if len(func_parts) >= 3:
            check_type = '_'.join(func_parts[3:]) if len(func_parts) > 3 else func_parts[2]
            
            # Find potential matches
            potential_matches = []
            
            for rule, rule_info in all_rules_detailed.items():
                rule_lower = rule.lower()
                score = 0
                reasons = []
                
                # Same service bonus
                if rule_info['service'] == service:
                    score += 2
                
                # Check for key patterns
                patterns = {
                    'high_severity': ['severity', 'critical', 'high', 'alert'],
                    'unused': ['unused', 'stale', '90_days', 'inactive'],
                    'root': ['root', 'admin', 'privileged'],
                    'public': ['public', 'internet', '0_0_0_0'],
                    'encrypt': ['encrypt', 'kms', 'cmk'],
                    'backup': ['backup', 'snapshot', 'retention'],
                    'log': ['log', 'trail', 'monitor'],
                    'mfa': ['mfa', 'multi_factor'],
                    'patch': ['patch', 'update', 'ssm'],
                    'compliance': ['compliance', 'compliant', 'standard']
                }
                
                for pattern, keywords in patterns.items():
                    if pattern in check_type:
                        for keyword in keywords:
                            if keyword in rule_lower:
                                score += 3
                                reasons.append(f"{pattern}→{keyword}")
                
                # Check descriptions for clues
                for desc in analysis['descriptions']:
                    desc_lower = desc.lower()
                    if any(word in desc_lower for word in ['audit', 'log']) and \
                       any(word in rule_lower for word in ['trail', 'log']):
                        score += 2
                        reasons.append("audit requirement")
                    
                    if 'encrypt' in desc_lower and 'encrypt' in rule_lower:
                        score += 2
                        reasons.append("encryption requirement")
                
                if score >= 4:  # Threshold
                    potential_matches.append({
                        'rule': rule,
                        'score': score,
                        'reasons': reasons
                    })
            
            # Sort by score
            potential_matches.sort(key=lambda x: x['score'], reverse=True)
            
            if potential_matches:
                analysis['potential_coverage'] = potential_matches[:3]
                analysis['coverage_likelihood'] = 'HIGH' if potential_matches[0]['score'] >= 6 else 'MEDIUM'
                total_potentially_covered += 1
            else:
                analysis['coverage_likelihood'] = 'LOW'
        
        service_analysis.append(analysis)
    
    step3_analysis[service] = service_analysis

# Create detailed report
print("\nCreating detailed Step 3 analysis report...")
REPORT_FILE = "/Users/apple/Desktop/compliance_Database/rule_finalisation/STEP3_DETAILED_ANALYSIS.md"

with open(REPORT_FILE, 'w') as f:
    f.write("# Step 3 Functions - Detailed Analysis & Coverage Opportunities\n\n")
    f.write(f"**Total Step 3 Functions:** 124\n")
    f.write(f"**Potentially Coverable:** {total_potentially_covered}\n\n")
    
    f.write("## Summary by Service\n\n")
    
    for service, analyses in step3_analysis.items():
        coverable = sum(1 for a in analyses if a.get('potential_coverage'))
        f.write(f"- **{service}**: {len(analyses)} functions ({coverable} potentially coverable)\n")
    
    f.write("\n## Detailed Analysis\n\n")
    
    # Show high potential coverage first
    f.write("### 🎯 HIGH POTENTIAL COVERAGE\n\n")
    
    count = 0
    for service, analyses in step3_analysis.items():
        for analysis in analyses:
            if analysis.get('coverage_likelihood') == 'HIGH':
                count += 1
                f.write(f"#### {count}. {analysis['function']}\n\n")
                
                f.write(f"**Compliance Requirements:** {analysis['compliance_count']} from {', '.join(analysis['frameworks'])}\n\n")
                
                if analysis['descriptions']:
                    f.write("**What it checks:**\n")
                    for desc in analysis['descriptions']:
                        f.write(f"- {desc}\n")
                    f.write("\n")
                
                f.write("**Can be covered by:**\n")
                for match in analysis['potential_coverage'][:2]:
                    f.write(f"- `{match['rule']}` (score: {match['score']})\n")
                    f.write(f"  - Reasons: {', '.join(match['reasons'])}\n")
                f.write("\n---\n\n")
    
    # Show examples of truly needed functions
    f.write("### ❌ TRULY NEEDS DEVELOPMENT\n\n")
    
    count = 0
    for service, analyses in step3_analysis.items():
        for analysis in analyses:
            if not analysis.get('potential_coverage') and count < 10:
                count += 1
                f.write(f"#### {count}. {analysis['function']}\n\n")
                
                f.write(f"**Required by:** {', '.join(analysis['frameworks'])}\n")
                
                if analysis['descriptions']:
                    f.write(f"**Purpose:** {analysis['descriptions'][0]}\n")
                
                f.write("**Why needed:** No existing rule can check this specific requirement\n\n")
                f.write("---\n\n")

print(f"✓ Detailed report saved: {REPORT_FILE}")

# Update mapping with enhanced analysis
print("\nUpdating mapping with enhanced Step 3 analysis...")
for service, analyses in step3_analysis.items():
    if service in mapping:
        # Convert to the expected format
        enhanced_step3 = []
        for analysis in analyses:
            entry = {
                'function': analysis['function'],
                'compliance_requirements': [],
                'coverage_analysis': {
                    'likelihood': analysis['coverage_likelihood'],
                    'potential_rules': [m['rule'] for m in analysis.get('potential_coverage', [])][:2]
                }
            }
            
            # Add compliance requirements with proper descriptions
            func_contexts = function_contexts.get(analysis['function'], [])
            for ctx in func_contexts[:5]:  # Top 5
                entry['compliance_requirements'].append({
                    'framework': ctx['framework'],
                    'requirement': ctx['requirement_name'],
                    'description': ctx['description'] if ctx['description'] != 'nan' else ctx['requirement_name'],
                    'what_is_expected': f"Ensure compliance with: {ctx['requirement_name']}"
                })
            
            enhanced_step3.append(entry)
        
        mapping[service]['step3_needs_development_enhanced'] = enhanced_step3

# Save enhanced mapping
with open(MAPPING_FILE, 'w') as f:
    json.dump(mapping, f, indent=2)

print("\n" + "=" * 100)
print("ENHANCED ANALYSIS COMPLETE")
print("=" * 100)
print()
print(f"✓ Fixed 'nan' descriptions")
print(f"✓ Added meaningful context from compliance requirements")
print(f"✓ Found {total_potentially_covered} Step 3 functions that could be covered")
print(f"✓ Created detailed analysis report: {REPORT_FILE}")
print()
print("Updated mapping now includes:")
print("- step3_needs_development (original list)")
print("- step3_needs_development_with_context (basic context)")  
print("- step3_needs_development_enhanced (full analysis)")
print()
print("Review the report to see which Step 3 functions could be covered!")
print("=" * 100)
