#!/usr/bin/env python3
"""
Merge K8s Functions into Consolidated Compliance Rules CSV
Updates the k8s_checks column for non-CIS compliance frameworks
"""

import csv
import json
import logging
import re
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Framework mapping
FRAMEWORKS = {
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


def normalize_id(text):
    """Normalize ID for matching."""
    # Remove common separators and lowercase
    return re.sub(r'[_\-\.\s]', '', text.lower())


def load_k8s_functions_from_framework(framework_name, k8s_agent_dir):
    """Load K8s functions for a specific framework."""
    k8s_functions = {}
    
    # Find the most recent output directory
    base_path = Path(k8s_agent_dir)
    output_dirs = list(base_path.glob(f"output_{framework_name}_*"))
    
    if not output_dirs:
        logging.warning(f"No output directory found for {framework_name}")
        return k8s_functions
    
    latest_dir = max(output_dirs, key=lambda p: p.stat().st_mtime)
    step2_dir = latest_dir / "step2"
    
    if not step2_dir.exists():
        logging.warning(f"Step2 directory not found for {framework_name}")
        return k8s_functions
    
    logging.info(f"Loading K8s functions for {framework_name} from {step2_dir}")
    
    # Load all Step 2 JSON files
    for json_file in step2_dir.glob("*.json"):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            control_id = data.get('control_id', '')
            if data.get('k8s_applicable') and data.get('validated_functions'):
                k8s_functions[control_id] = '; '.join(data['validated_functions'])
        
        except Exception as e:
            logging.error(f"Error loading {json_file}: {e}")
    
    logging.info(f"  Loaded {len(k8s_functions)} controls with K8s functions")
    return k8s_functions


def update_consolidated_csv(consolidated_csv_path, k8s_agent_dir, output_csv_path):
    """Update consolidated CSV with K8s functions."""
    
    logging.info("="*80)
    logging.info("MERGING K8S FUNCTIONS TO CONSOLIDATED CSV")
    logging.info("="*80)
    
    # Load K8s functions for all frameworks
    all_k8s_functions = {}
    for framework_name in FRAMEWORKS.keys():
        k8s_funcs = load_k8s_functions_from_framework(framework_name, k8s_agent_dir)
        all_k8s_functions[framework_name] = k8s_funcs
    
    # Read consolidated CSV
    logging.info(f"\nReading consolidated CSV: {consolidated_csv_path}")
    with open(consolidated_csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames)
        rows = list(reader)
    
    logging.info(f"Loaded {len(rows)} rows")
    
    # Process each row
    updated_count = 0
    skipped_cis_count = 0
    skipped_already_has_k8s_count = 0
    no_match_count = 0
    
    for row in rows:
        unique_id = row['unique_compliance_id']
        current_k8s = row.get('k8s_checks', '').strip()
        
        # Skip CIS compliance (already has K8s data)
        if '_cis_k8s_' in unique_id.lower() or unique_id.startswith('cis_'):
            skipped_cis_count += 1
            continue
        
        # Skip if already has K8s checks
        if current_k8s:
            skipped_already_has_k8s_count += 1
            continue
        
        # Try to match with generated K8s functions
        matched = False
        for framework_name, framework_prefix in FRAMEWORKS.items():
            if unique_id.startswith(framework_prefix):
                k8s_funcs = all_k8s_functions.get(framework_name, {})
                
                # Try to match by control ID
                for control_id, functions in k8s_funcs.items():
                    # Normalize both for comparison
                    normalized_control = normalize_id(control_id)
                    normalized_unique = normalize_id(unique_id)
                    
                    # Check if control ID appears in unique_compliance_id
                    if normalized_control in normalized_unique:
                        row['k8s_checks'] = functions
                        updated_count += 1
                        matched = True
                        logging.debug(f"Matched: {control_id} → {unique_id}")
                        break
                
                if not matched:
                    no_match_count += 1
                    logging.debug(f"No match found for: {unique_id}")
                
                break
    
    # Write updated CSV
    logging.info(f"\nWriting updated CSV to: {output_csv_path}")
    with open(output_csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    
    # Summary
    logging.info("\n" + "="*80)
    logging.info("MERGE COMPLETE")
    logging.info("="*80)
    logging.info(f"  Total rows in consolidated CSV: {len(rows)}")
    logging.info(f"  Updated with K8s functions: {updated_count}")
    logging.info(f"  Skipped (CIS K8s): {skipped_cis_count}")
    logging.info(f"  Skipped (already has K8s): {skipped_already_has_k8s_count}")
    logging.info(f"  No match found: {no_match_count}")
    logging.info(f"  Output file: {output_csv_path}")
    logging.info("="*80)
    
    return updated_count


def main():
    k8s_agent_dir = "/Users/apple/Desktop/compliance_Database/compliance_agent/k8s_function_agent"
    consolidated_csv = "/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule/consolidated_compliance_rules_FINAL.csv"
    output_csv = "/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule/consolidated_compliance_rules_FINAL_WITH_K8S.csv"
    
    update_consolidated_csv(consolidated_csv, k8s_agent_dir, output_csv)
    
    print("\n✅ Merge complete!")
    print(f"\nReview the output file:")
    print(f"  {output_csv}")
    print(f"\nIf satisfied, replace the original:")
    print(f"  cp {output_csv} {consolidated_csv}.backup")
    print(f"  mv {output_csv} {consolidated_csv}")


if __name__ == "__main__":
    main()

