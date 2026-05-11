#!/usr/bin/env python3
"""
Update Consolidated Compliance Rules CSV with K8s Functions
Merges K8s functions generated for non-CIS frameworks into the consolidated CSV
"""

import csv
import json
import logging
from pathlib import Path
from datetime import datetime
from collections import defaultdict

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Mapping between framework names and their prefixes in consolidated CSV
FRAMEWORK_MAPPING = {
    'GDPR': 'gdpr_multi_cloud',
    'HIPAA': 'hipaa_multi_cloud',
    'NIST_800_171': 'nist_800_171_r2_multi_cloud',
    'NIST_800_53': 'nist_800_53_rev5_multi_cloud',
    'SOC2': 'soc2_multi_cloud',
    'ISO27001': 'iso27001_2022_multi_cloud',
    'PCI_DSS': 'pci_dss_v4_multi_cloud',
    'FedRAMP': 'fedramp_moderate_multi_cloud',
    'CISA_CE': 'cisa_ce_multi_cloud',
    'RBI_BANK': 'rbi_bank_multi_cloud',
    'RBI_NBFC': 'rbi_nbfc_multi_cloud',
    'CANADA_PBMM': 'canada_pbmm_moderate_multi_cloud'
}

# Mapping of requirement IDs between frameworks
REQUIREMENT_ID_MAPPING = {
    'GDPR': {
        'article_25': 'Article_25',
        'article_30': 'Article_30',
        'article_32': 'Article_32'
    },
    'HIPAA': {
        '164_308_a_1_ii_a': '164_308_a_1_ii_a',
        '164_308_a_1_ii_b': '164_308_a_1_ii_b',
        '164_308_a_1_ii_d': '164_308_a_1_ii_d',
        '164_308_a_3_i': '164_308_a_3_i',
        '164_308_a_3_ii_a': '164_308_a_3_ii_a',
        '164_308_a_3_ii_b': '164_308_a_3_ii_b',
        '164_308_a_3_ii_c': '164_308_a_3_ii_c',
        '164_308_a_4_i': '164_308_a_4_i',
        '164_308_a_4_ii_a': '164_308_a_4_ii_a',
        '164_308_a_4_ii_b': '164_308_a_4_ii_b',
        '164_308_a_4_ii_c': '164_308_a_4_ii_c',
        '164_308_a_5_ii_b': '164_308_a_5_ii_b',
        '164_308_a_5_ii_c': '164_308_a_5_ii_c',
        '164_308_a_5_ii_d': '164_308_a_5_ii_d',
        '164_308_a_6_i': '164_308_a_6_i',
        '164_308_a_6_ii': '164_308_a_6_ii',
        '164_308_a_7_i': '164_308_a_7_i',
        '164_308_a_7_ii_a': '164_308_a_7_ii_a',
        '164_308_a_7_ii_b': '164_308_a_7_ii_b',
        '164_308_a_7_ii_c': '164_308_a_7_ii_c',
        '164_308_a_8': '164_308_a_8',
        '164_312_a_1': '164_312_a_1',
        '164_312_a_2_i': '164_312_a_2_i',
        '164_312_a_2_ii': '164_312_a_2_ii',
        '164_312_a_2_iv': '164_312_a_2_iv',
        '164_312_b': '164_312_b',
        '164_312_c_1': '164_312_c_1',
        '164_312_c_2': '164_312_c_2',
        '164_312_d': '164_312_d',
        '164_312_e_1': '164_312_e_1',
        '164_312_e_2_i': '164_312_e_2_i',
        '164_312_e_2_ii': '164_312_e_2_ii'
    },
    'NIST_800_171': {
        '3_1_1': '3_1_1',
        '3_1_12': '3_1_12',
        '3_1_13': '3_1_13',
        '3_1_14': '3_1_14',
        '3_1_2': '3_1_2',
        '3_1_20': '3_1_20',
        '3_1_3': '3_1_3',
        '3_1_4': '3_1_4',
        '3_1_5': '3_1_5',
        '3_1_6': '3_1_6',
        '3_1_7': '3_1_7',
        '3_3_1': '3_3_1',
        '3_3_2': '3_3_2',
        '3_3_3': '3_3_3',
        '3_3_4': '3_3_4',
        '3_3_5': '3_3_5',
        '3_3_8': '3_3_8',
        '3_4_1': '3_4_1',
        '3_4_2': '3_4_2',
        '3_4_6': '3_4_6',
        '3_4_7': '3_4_7',
        '3_4_9': '3_4_9',
        '3_5_10': '3_5_10',
        '3_5_2': '3_5_2',
        '3_5_3': '3_5_3',
        '3_5_5': '3_5_5',
        '3_5_6': '3_5_6',
        '3_5_7': '3_5_7',
        '3_5_8': '3_5_8',
        '3_6_1': '3_6_1',
        '3_6_2': '3_6_2',
        '3_11_2': '3_11_2',
        '3_11_3': '3_11_3',
        '3_12_4': '3_12_4',
        '3_13_1': '3_13_1',
        '3_13_11': '3_13_11',
        '3_13_15': '3_13_15',
        '3_13_16': '3_13_16',
        '3_13_2': '3_13_2',
        '3_13_3': '3_13_3',
        '3_13_4': '3_13_4',
        '3_13_5': '3_13_5',
        '3_13_6': '3_13_6',
        '3_13_8': '3_13_8',
        '3_14_1': '3_14_1',
        '3_14_2': '3_14_2',
        '3_14_3': '3_14_3',
        '3_14_4': '3_14_4',
        '3_14_6': '3_14_6',
        '3_14_7': '3_14_7'
    }
}


def load_k8s_functions_from_step2(step2_dir):
    """Load K8s functions from Step 2 JSON files."""
    k8s_functions = {}
    
    step2_path = Path(step2_dir)
    for json_file in step2_path.glob("*.json"):
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        control_id = data.get('control_id', '')
        if data.get('k8s_applicable') and data.get('validated_functions'):
            k8s_functions[control_id] = '; '.join(data['validated_functions'])
    
    return k8s_functions


def find_k8s_function_dirs(base_dir):
    """Find all framework output directories with K8s functions."""
    base_path = Path(base_dir)
    framework_k8s_data = {}
    
    for framework_name in FRAMEWORK_MAPPING.keys():
        # Find the most recent output directory for this framework
        output_dirs = list(base_path.glob(f"output_{framework_name}_*"))
        if output_dirs:
            latest_dir = max(output_dirs, key=lambda p: p.stat().st_mtime)
            step2_dir = latest_dir / "step2"
            
            if step2_dir.exists():
                logging.info(f"Loading K8s functions for {framework_name} from {step2_dir}")
                k8s_funcs = load_k8s_functions_from_step2(step2_dir)
                framework_k8s_data[framework_name] = k8s_funcs
                logging.info(f"  Found {len(k8s_funcs)} controls with K8s functions")
    
    return framework_k8s_data


def update_consolidated_csv(consolidated_csv_path, k8s_function_agent_dir, output_csv_path):
    """Update the consolidated CSV with K8s functions."""
    
    logging.info(f"Reading consolidated CSV: {consolidated_csv_path}")
    
    # Load all K8s functions
    framework_k8s_data = find_k8s_function_dirs(k8s_function_agent_dir)
    
    # Read consolidated CSV
    with open(consolidated_csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)
    
    logging.info(f"Loaded {len(rows)} rows from consolidated CSV")
    
    # Find k8s_checks column index
    k8s_checks_col = 'k8s_checks'
    if k8s_checks_col not in fieldnames:
        logging.error(f"Column '{k8s_checks_col}' not found in CSV")
        return
    
    # Update rows
    updated_count = 0
    skipped_count = 0
    
    for row in rows:
        unique_id = row['unique_compliance_id']
        
        # Check if this is a non-CIS multi-cloud row that needs K8s functions
        for framework_name, framework_prefix in FRAMEWORK_MAPPING.items():
            if unique_id.startswith(framework_prefix):
                # Extract the requirement ID from the unique_compliance_id
                # Format: framework_prefix_RequirementID_description_####
                
                # Current k8s_checks value
                current_k8s = row.get(k8s_checks_col, '').strip()
                
                # Skip if already has K8s checks (CIS or already populated)
                if current_k8s:
                    skipped_count += 1
                    continue
                
                # Find matching K8s functions from our generated data
                if framework_name in framework_k8s_data:
                    # Try to match control ID
                    # The unique_id format varies, so we need to extract the control ID
                    k8s_funcs = framework_k8s_data[framework_name]
                    
                    # Try different patterns to match
                    matched = False
                    for control_id, functions in k8s_funcs.items():
                        # Check if control_id is in the unique_id
                        control_id_clean = control_id.replace('_', '').replace('-', '').lower()
                        unique_id_clean = unique_id.replace('_', '').replace('-', '').lower()
                        
                        if control_id_clean in unique_id_clean or control_id.lower() in unique_id.lower():
                            row[k8s_checks_col] = functions
                            updated_count += 1
                            matched = True
                            break
                    
                    if not matched:
                        logging.debug(f"No K8s functions found for {unique_id}")
                
                break  # Found the framework, no need to check others
    
    # Write updated CSV
    logging.info(f"Writing updated CSV to: {output_csv_path}")
    with open(output_csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    
    logging.info(f"\n{'='*80}")
    logging.info(f"UPDATE COMPLETE")
    logging.info(f"  Total rows: {len(rows)}")
    logging.info(f"  Updated with K8s functions: {updated_count}")
    logging.info(f"  Skipped (already has K8s): {skipped_count}")
    logging.info(f"  Output: {output_csv_path}")
    logging.info(f"{'='*80}\n")


def main():
    k8s_agent_dir = "/Users/apple/Desktop/compliance_Database/compliance_agent/k8s_function_agent"
    consolidated_csv = "/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule/consolidated_compliance_rules_FINAL.csv"
    output_csv = "/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule/consolidated_compliance_rules_FINAL_WITH_K8S.csv"
    
    update_consolidated_csv(consolidated_csv, k8s_agent_dir, output_csv)
    
    logging.info("Done! Review the output file and if satisfied, you can replace the original.")
    logging.info(f"To replace: mv {output_csv} {consolidated_csv}")


if __name__ == "__main__":
    main()

