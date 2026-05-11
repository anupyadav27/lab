"""
Create Functions by Service JSON for ALL Cloud Providers
Extract and organize functions by service for each CSP: AWS, Azure, GCP, Oracle, IBM, Alicloud, Kubernetes
"""

import csv
import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime
import re

# Input/Output paths
INPUT_CSV = Path("/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule/consolidated_compliance_rules_2025-11-08.csv")
OUTPUT_DIR = Path("/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule")

# Column mappings
CSP_COLUMNS = {
    'aws': 'aws_checks',
    'azure': 'azure_checks',
    'gcp': 'gcp_checks',
    'oracle': 'oracle_checks',
    'ibm': 'ibm_checks',
    'alicloud': 'alicloud_checks',
    'kubernetes': 'k8s_checks'
}

def extract_service_from_function(function_name, csp):
    """Extract service name from function name based on CSP naming convention"""
    
    # Skip invalid/placeholder functions
    invalid_patterns = ['no checks defined', 'no_checks_defined', 'na']
    if any(pattern in function_name.lower() for pattern in invalid_patterns):
        return None
    
    # CSP-specific parsing
    if csp == 'aws':
        # AWS: aws_service_function or service_function
        parts = function_name.split('_')
        if function_name.startswith('aws_') and len(parts) >= 2:
            return parts[1]  # aws_iam_xxx -> iam
        elif len(parts) >= 2 and not function_name.startswith('aws_'):
            return parts[0]  # iam_xxx -> iam
    
    elif csp == 'azure':
        # Azure: azure_service_function or azurerm_service_function
        if function_name.startswith('azure_'):
            parts = function_name.replace('azure_', '').split('_')
            return parts[0] if parts else 'unknown'
        elif function_name.startswith('azurerm_'):
            parts = function_name.replace('azurerm_', '').split('_')
            return parts[0] if parts else 'unknown'
    
    elif csp == 'gcp':
        # GCP: gcp_service_function
        if function_name.startswith('gcp_'):
            parts = function_name.replace('gcp_', '').split('_')
            return parts[0] if parts else 'unknown'
    
    elif csp == 'oracle':
        # Oracle: oracle_service_function or oci_service_function
        if function_name.startswith('oracle_'):
            parts = function_name.replace('oracle_', '').split('_')
            return parts[0] if parts else 'unknown'
        elif function_name.startswith('oci_'):
            parts = function_name.replace('oci_', '').split('_')
            return parts[0] if parts else 'unknown'
    
    elif csp == 'ibm':
        # IBM: ibm_service_function
        if function_name.startswith('ibm_'):
            parts = function_name.replace('ibm_', '').split('_')
            return parts[0] if parts else 'unknown'
    
    elif csp == 'alicloud':
        # Alicloud: alicloud_service_function
        if function_name.startswith('alicloud_'):
            parts = function_name.replace('alicloud_', '').split('_')
            return parts[0] if parts else 'unknown'
    
    elif csp == 'kubernetes':
        # Kubernetes: k8s_service_function or kubernetes_service_function
        if function_name.startswith('k8s_'):
            parts = function_name.replace('k8s_', '').split('_')
            return parts[0] if parts else 'unknown'
        elif function_name.startswith('kubernetes_'):
            parts = function_name.replace('kubernetes_', '').split('_')
            return parts[0] if parts else 'unknown'
    
    return 'unknown'

def process_csp_functions(csp_name, column_name):
    """Process functions for a specific cloud provider"""
    print(f"\nProcessing {csp_name.upper()}...")
    
    # Data structure: {service: {function_name: [unique_ids]}}
    functions_by_service = defaultdict(lambda: defaultdict(set))
    
    # Read CSV
    with open(INPUT_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            unique_id = row['unique_compliance_id']
            checks = row.get(column_name, '')
            
            # Skip if no checks
            if not checks or checks == 'NA':
                continue
            
            # Parse checks (semicolon-separated)
            check_list = [c.strip() for c in checks.split(';') if c.strip()]
            
            for check in check_list:
                # Skip invalid checks
                if 'no checks defined' in check.lower() or check.lower() == 'na':
                    continue
                
                # Extract service
                service = extract_service_from_function(check, csp_name)
                
                if service:
                    functions_by_service[service][check].add(unique_id)
    
    # Convert sets to sorted lists
    result = {}
    for service in sorted(functions_by_service.keys()):
        result[service] = {}
        for function in sorted(functions_by_service[service].keys()):
            result[service][function] = sorted(list(functions_by_service[service][function]))
    
    return result

def create_finalized_json(csp_name, functions_data):
    """Create finalized JSON structure with metadata"""
    
    total_functions = sum(len(funcs) for funcs in functions_data.values())
    total_mappings = sum(len(ids) for service_funcs in functions_data.values() 
                        for ids in service_funcs.values())
    
    finalized = {
        "metadata": {
            "version": "1.0",
            "cloud_provider": csp_name.upper(),
            "generated_date": datetime.now().strftime("%Y-%m-%d"),
            "description": f"{csp_name.upper()} compliance check functions organized by service category",
            "total_services": len(functions_data),
            "total_functions": total_functions,
            "total_compliance_mappings": total_mappings
        },
        "services": {}
    }
    
    # Add services with metadata
    for service, functions in functions_data.items():
        service_data = {
            "service_name": service,
            "function_count": len(functions),
            "total_compliance_mappings": sum(len(ids) for ids in functions.values()),
            "functions": {}
        }
        
        for func_name, compliance_ids in functions.items():
            service_data["functions"][func_name] = {
                "function_name": func_name,
                "compliance_count": len(compliance_ids),
                "compliance_ids": compliance_ids
            }
        
        finalized["services"][service] = service_data
    
    return finalized

# Main processing
print("=" * 80)
print("CREATING FUNCTIONS BY SERVICE FOR ALL CLOUD PROVIDERS")
print("=" * 80)

statistics = {}

for csp_name, column_name in CSP_COLUMNS.items():
    functions_data = process_csp_functions(csp_name, column_name)
    
    if functions_data:
        # Create finalized JSON
        finalized_json = create_finalized_json(csp_name, functions_data)
        
        # Save to file
        output_file = OUTPUT_DIR / f"{csp_name}_functions_by_service_2025-11-08.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(finalized_json, f, indent=2)
        
        # Collect statistics
        statistics[csp_name] = {
            'services': finalized_json['metadata']['total_services'],
            'functions': finalized_json['metadata']['total_functions'],
            'mappings': finalized_json['metadata']['total_compliance_mappings'],
            'file_size': output_file.stat().st_size / 1024  # KB
        }
        
        print(f"  ✓ {csp_name.upper()}: {statistics[csp_name]['services']} services, {statistics[csp_name]['functions']} functions")
    else:
        print(f"  ✗ {csp_name.upper()}: No functions found")

print()
print("=" * 80)
print("ALL CLOUD PROVIDERS PROCESSED")
print("=" * 80)
print()

# Summary table
print(f"{'Cloud Provider':<15} {'Services':<10} {'Functions':<12} {'Mappings':<12} {'Size (KB)':<10}")
print("-" * 80)
for csp, stats in sorted(statistics.items()):
    print(f"{csp.upper():<15} {stats['services']:<10} {stats['functions']:<12} {stats['mappings']:<12} {stats['file_size']:<10.1f}")

print()
print(f"Total files created: {len(statistics)}")
print(f"Output directory: {OUTPUT_DIR}")
print()

