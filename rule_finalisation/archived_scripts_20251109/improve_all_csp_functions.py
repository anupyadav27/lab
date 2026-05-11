"""
Improve ALL CSP Functions - Apply AWS learnings to Azure, GCP, Oracle, IBM, Alicloud, K8s
Phase by phase improvement for all CSPs
"""
import csv
import json
from collections import defaultdict
from pathlib import Path

INPUT_CSV = Path("/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule/consolidated_compliance_rules_FINAL.csv")
OUTPUT_DIR = Path("/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule")

# CSPs to process (AWS already done)
CSPS = ['azure', 'gcp', 'oracle', 'ibm', 'alicloud', 'k8s']

print("=" * 80)
print("ANALYZING ALL CSP FUNCTIONS")
print("=" * 80)
print()

# Extract all functions for each CSP
csp_functions = {csp: set() for csp in CSPS}
csp_function_usage = {csp: defaultdict(int) for csp in CSPS}

with open(INPUT_CSV, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        for csp in CSPS:
            col_name = f'{csp}_checks'
            checks = row.get(col_name, '')
            if checks and checks != 'NA':
                funcs = [f.strip() for f in checks.split(';') if f.strip()]
                for func in funcs:
                    csp_functions[csp].add(func)
                    csp_function_usage[csp][func] += 1

# Display summary
print("CSP Function Count:")
print(f"{'CSP':<12} {'Functions':<12} {'Status'}")
print("-" * 50)
print(f"{'AWS':<12} {524:<12} ✅ Complete")
for csp in CSPS:
    count = len(csp_functions[csp])
    print(f"{csp.upper():<12} {count:<12} 🔄 To Process")

print()
print("=" * 80)

# Analyze each CSP
for csp in CSPS:
    print()
    print(f"{'='*80}")
    print(f"{csp.upper()} ANALYSIS")
    print(f"{'='*80}")
    
    functions = csp_functions[csp]
    print(f"Total functions: {len(functions)}")
    
    if len(functions) == 0:
        print(f"⚠️  No {csp} functions found!")
        continue
    
    # Categorize by service
    by_service = defaultdict(list)
    issues = {
        'missing_prefix': [],
        'concatenated': [],
        'short_names': []
    }
    
    prefix = f"{csp}_"
    
    for func in sorted(functions):
        # Check for missing prefix
        if not func.startswith(prefix):
            issues['missing_prefix'].append(func)
            continue
        
        # Check for concatenated
        if ',' in func:
            issues['concatenated'].append(func)
            continue
        
        # Check for too short names
        if len(func.split('_')) < 3:
            issues['short_names'].append(func)
        
        # Extract service
        parts = func[len(prefix):].split('_')
        if parts:
            service = parts[0]
            by_service[service].append(func)
    
    print()
    print("Services found:", len(by_service))
    
    # Show top 10 services
    sorted_services = sorted(by_service.items(), key=lambda x: len(x[1]), reverse=True)
    print("\nTop 10 services:")
    for i, (service, funcs) in enumerate(sorted_services[:10], 1):
        print(f"  {i:2d}. {service:<20s} {len(funcs):3d} functions")
    
    # Show issues
    print()
    print("Issues found:")
    if issues['missing_prefix']:
        print(f"  ❌ Missing {csp}_ prefix: {len(issues['missing_prefix'])}")
        for f in issues['missing_prefix'][:3]:
            print(f"     • {f}")
    
    if issues['concatenated']:
        print(f"  ❌ Concatenated functions: {len(issues['concatenated'])}")
        for f in issues['concatenated'][:3]:
            print(f"     • {f}")
    
    if issues['short_names']:
        print(f"  ⚠️  Short/generic names: {len(issues['short_names'])}")
    
    # Look for potential duplicates
    print()
    print("Potential duplicate patterns:")
    
    # Encryption variations
    encryption_funcs = [f for f in functions if 'encryption' in f or 'encrypted' in f]
    if len(encryption_funcs) > 5:
        print(f"  • Encryption checks: {len(encryption_funcs)}")
        # Group by enabled/check/status_check
        enabled = [f for f in encryption_funcs if f.endswith('_enabled')]
        check = [f for f in encryption_funcs if f.endswith('_check')]
        encrypted = [f for f in encryption_funcs if f.endswith('_encrypted')]
        print(f"    - *_enabled: {len(enabled)}")
        print(f"    - *_check: {len(check)}")
        print(f"    - *_encrypted: {len(encrypted)}")
    
    # Multi-AZ/HA
    ha_funcs = [f for f in functions if 'multi' in f or '_az' in f or 'availability' in f]
    if len(ha_funcs) > 3:
        print(f"  • Multi-AZ/HA checks: {len(ha_funcs)}")
    
    # Public access
    public_funcs = [f for f in functions if 'public' in f]
    if len(public_funcs) > 5:
        print(f"  • Public access checks: {len(public_funcs)}")
    
    # Backup/retention
    backup_funcs = [f for f in functions if 'backup' in f or 'retention' in f or 'snapshot' in f]
    if len(backup_funcs) > 5:
        print(f"  • Backup/snapshot checks: {len(backup_funcs)}")
    
    # Save detailed analysis
    analysis_file = OUTPUT_DIR / f"{csp}_analysis.json"
    analysis_data = {
        'total_functions': len(functions),
        'services': {svc: len(funcs) for svc, funcs in by_service.items()},
        'issues': issues,
        'functions_by_service': {svc: funcs for svc, funcs in by_service.items()},
        'usage_count': {f: csp_function_usage[csp][f] for f in functions}
    }
    
    with open(analysis_file, 'w', encoding='utf-8') as f:
        json.dump(analysis_data, f, indent=2)
    
    print(f"\n✅ Analysis saved: {analysis_file.name}")

print()
print("=" * 80)
print("ANALYSIS COMPLETE FOR ALL CSPs")
print("=" * 80)
print()
print("Next step: Review each CSP's analysis JSON and create consolidation plan")

