#!/usr/bin/env python3
"""
Compliance Rules Consolidation Script
Consolidates all compliance framework controls into a unified CSV schema
"""

import csv
import json
import os
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# Base directory
BASE_DIR = Path("/Users/apple/Desktop/compliance_Database/compliance_agent")
OUTPUT_DIR = Path("/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule")
OUTPUT_DIR.mkdir(exist_ok=True)

# Framework mapping
FRAMEWORK_MAPPING = {
    'canada_pbmm': ('CANADA_PBMM', 'canada_pbmm_moderate', 'Moderate'),
    'cisa_ce': ('CISA_CE', 'cisa_ce_v1', 'v1.0'),
    'FedRamp': ('FedRAMP', 'fedramp_moderate', 'Moderate'),
    'gdpr': ('GDPR', 'gdpr', ''),
    'hipaa': ('HIPAA', 'hipaa', ''),
    'iso27001-2022': ('ISO27001', 'iso27001_2022', '2022'),
    'nist_800_171': ('NIST_800-171', 'nist_800_171_r2', 'R2'),
    'nist_complaince_agent': ('NIST_800-53', 'nist_800_53_rev5', 'Rev5'),
    'pci_compliance_agent': ('PCI-DSS', 'pci_dss_v4', 'v4.0'),
    'rbi_bank': ('RBI_BANK', 'rbi_bank', ''),
    'rbi_nbfc': ('RBI_NBFC', 'rbi_nbfc', ''),
    'soc2': ('SOC2', 'soc2', '')
}

CIS_CLOUD_MAPPING = {
    'aws_agent': 'AWS',
    'azure_agent': 'AZURE',
    'gcp_agent': 'GCP',
    'oracle_agent': 'ORACLE',
    'ibm_agent': 'IBM',
    'alicloud_agent': 'ALICLOUD',
    'k8s_agent': 'KUBERNETES'
}


def generate_unique_id(framework_id, technology, requirement_id, requirement_name='', row_index=0):
    """
    Generate a unique compliance ID for each control
    Format: {framework_id}_{technology}_{sanitized_requirement_id}_{sequential_number}
    """
    # Sanitize requirement_id - remove special characters, replace spaces with underscore
    sanitized_req_id = re.sub(r'[^\w\-.]', '_', str(requirement_id))
    sanitized_req_id = re.sub(r'_+', '_', sanitized_req_id)  # Replace multiple underscores with single
    sanitized_req_id = sanitized_req_id.strip('_')  # Remove leading/trailing underscores
    
    # If requirement_id is NA or empty, use sanitized requirement_name
    if not sanitized_req_id or sanitized_req_id == 'NA':
        sanitized_req_id = re.sub(r'[^\w\-.]', '_', str(requirement_name)[:50])  # Limit to 50 chars
        sanitized_req_id = re.sub(r'_+', '_', sanitized_req_id)
        sanitized_req_id = sanitized_req_id.strip('_')
    
    # Create the unique ID with sequential number (padded to 4 digits)
    unique_id = f"{framework_id}_{technology.lower()}_{sanitized_req_id}_{str(row_index).zfill(4)}"
    
    return unique_id


def clean_text(text):
    """Clean text by removing extra whitespace and line breaks"""
    if not text or text == '':
        return 'NA'
    text = str(text).replace('\n', ' ').replace('\r', ' ')
    text = ' '.join(text.split())
    result = text.strip()
    return result if result else 'NA'


def extract_section_from_title(title):
    """Extract section/domain from control title"""
    if not title:
        return 'NA'
    
    # Look for common patterns
    patterns = [
        r'^([A-Z][A-Za-z\s&]+?)[\s:]',  # "Access Control: ..."
        r'^[A-Z]+-\d+[a-z]?\s+([A-Z][A-Za-z\s&]+?)[\s:]',  # "AC-2 Access Control: ..."
    ]
    
    for pattern in patterns:
        match = re.search(pattern, title)
        if match:
            result = match.group(1).strip()
            return result if result else 'NA'
    
    # Return first part before colon if present
    if ':' in title:
        result = title.split(':')[0].strip()
        return result if result else 'NA'
    
    return 'NA'


def infer_service_from_checks(checks):
    """Infer primary service from check names"""
    if not checks or checks == '' or checks == 'NA':
        return 'NA'
    
    # Extract service prefixes
    services = set()
    for check in checks.split(';'):
        check = check.strip()
        if '_' in check:
            parts = check.split('_')
            if len(parts) >= 2:
                services.add(parts[1])  # e.g., aws_iam_xxx -> iam
    
    if len(services) == 0:
        return 'NA'
    elif len(services) == 1:
        return list(services)[0].upper()
    else:
        return 'Multiple'


def count_checks(*check_columns):
    """Count total checks across all cloud providers"""
    total = 0
    for checks in check_columns:
        if checks and checks != '' and checks != 'NA':
            total += len([c for c in checks.split(';') if c.strip()])
    return total


def process_standard_compliance_file(file_path, framework_name):
    """Process standard compliance CSV files (NIST, ISO, PCI, etc.)"""
    print(f"  Processing: {file_path.name}")
    
    framework_info = FRAMEWORK_MAPPING.get(framework_name, (framework_name.upper(), framework_name.lower(), ''))
    compliance_framework, framework_id, framework_version = framework_info
    
    results = []
    row_counter = 0
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                row_counter += 1
                # Map fields based on column names
                control_id = row.get('Control_ID') or row.get('id') or row.get('control_id') or ''
                title = row.get('Title') or row.get('title') or row.get('Requirement Name') or ''
                automation_type = row.get('Automation_Type') or row.get('automation_type') or row.get('Assessment') or 'manual'
                
                # Extract checks for each cloud provider
                aws_checks = clean_text(row.get('AWS_Checks') or row.get('aws_checks') or '')
                azure_checks = clean_text(row.get('Azure_Checks') or row.get('azure_checks') or '')
                gcp_checks = clean_text(row.get('GCP_Checks') or row.get('gcp_checks') or '')
                oracle_checks = clean_text(row.get('Oracle_Checks') or row.get('oracle_checks') or '')
                ibm_checks = clean_text(row.get('IBM_Checks') or row.get('ibm_checks') or '')
                alicloud_checks = clean_text(row.get('Alicloud_Checks') or row.get('alicloud_checks') or '')
                k8s_checks = ''
                
                # Calculate total checks
                total = count_checks(aws_checks, azure_checks, gcp_checks, oracle_checks, ibm_checks, alicloud_checks)
                
                # Generate unique ID
                unique_id = generate_unique_id(framework_id, 'MULTI_CLOUD', control_id, title, row_counter)
                
                # Build result record
                record = {
                    'unique_compliance_id': unique_id,
                    'technology': 'MULTI_CLOUD',
                    'compliance_framework': compliance_framework,
                    'framework_id': framework_id,
                    'framework_version': framework_version or 'NA',
                    'requirement_id': clean_text(control_id),
                    'requirement_name': clean_text(title),
                    'requirement_description': 'NA',
                    'section': extract_section_from_title(title),
                    'service': infer_service_from_checks(aws_checks),
                    'total_checks': total,
                    'aws_checks': aws_checks if aws_checks and aws_checks != 'NA' else 'NA',
                    'azure_checks': azure_checks if azure_checks and azure_checks != 'NA' else 'NA',
                    'gcp_checks': gcp_checks if gcp_checks and gcp_checks != 'NA' else 'NA',
                    'oracle_checks': oracle_checks if oracle_checks and oracle_checks != 'NA' else 'NA',
                    'ibm_checks': ibm_checks if ibm_checks and ibm_checks != 'NA' else 'NA',
                    'alicloud_checks': alicloud_checks if alicloud_checks and alicloud_checks != 'NA' else 'NA',
                    'k8s_checks': 'NA',
                    'automation_type': automation_type.lower() if automation_type else 'manual',
                    'confidence_score': 'NA',
                    'references': 'NA',
                    'source_file': file_path.name
                }
                
                results.append(record)
                
    except Exception as e:
        print(f"    ERROR processing {file_path.name}: {e}")
    
    return results


def process_cis_agent_file(file_path, cloud_provider):
    """Process CIS agent CSV files"""
    print(f"  Processing CIS: {file_path.name}")
    
    results = []
    aggregated = defaultdict(lambda: {
        'checks': [],
        'description': '',
        'section': '',
        'title': '',
        'source': '',
        'references': '',
        'automation_type': 'manual',
        'confidence_scores': []
    })
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                req_id = row.get('id') or row.get('unique_id') or ''
                if not req_id:
                    continue
                
                program_name = row.get('program_name') or ''
                if program_name:
                    aggregated[req_id]['checks'].append(program_name)
                
                # Store other fields (first occurrence)
                if not aggregated[req_id]['title']:
                    aggregated[req_id]['title'] = clean_text(row.get('title') or '')
                    aggregated[req_id]['description'] = clean_text(row.get('description') or '')
                    aggregated[req_id]['section'] = clean_text(row.get('section') or '')
                    aggregated[req_id]['source'] = clean_text(row.get('source') or '')
                    aggregated[req_id]['references'] = clean_text(row.get('references') or '')
                    
                    # Map automation type
                    final_approach = row.get('final_approach') or row.get('assessment') or 'manual'
                    if 'automated' in final_approach.lower() or 'automatic' in final_approach.lower():
                        aggregated[req_id]['automation_type'] = 'automated'
                    else:
                        aggregated[req_id]['automation_type'] = 'manual'
                    
                    # Confidence score
                    conf_score = row.get('final_confidence') or ''
                    if conf_score and conf_score != '':
                        try:
                            aggregated[req_id]['confidence_scores'].append(float(conf_score))
                        except:
                            pass
        
        # Convert aggregated data to records
        req_counter = 0
        for req_id, data in aggregated.items():
            req_counter += 1
            # Extract framework info from source
            source = data['source']
            framework_match = re.search(r'CIS\s+(.+?)\s+BENCHMARK\s+V([\d.]+)', source, re.IGNORECASE)
            if framework_match:
                framework_name = framework_match.group(1).strip()
                framework_version = f"v{framework_match.group(2)}"
            else:
                framework_name = cloud_provider
                framework_version = 'v1.0'
            
            # Calculate average confidence
            avg_confidence = ''
            if data['confidence_scores']:
                avg_confidence = f"{sum(data['confidence_scores']) / len(data['confidence_scores']):.2f}"
            else:
                avg_confidence = 'NA'
            
            # Build check columns based on cloud provider
            check_columns = {
                'aws_checks': 'NA',
                'azure_checks': 'NA',
                'gcp_checks': 'NA',
                'oracle_checks': 'NA',
                'ibm_checks': 'NA',
                'alicloud_checks': 'NA',
                'k8s_checks': 'NA'
            }
            
            checks_str = ';'.join(data['checks']) if data['checks'] else 'NA'
            if cloud_provider == 'AWS':
                check_columns['aws_checks'] = checks_str
            elif cloud_provider == 'AZURE':
                check_columns['azure_checks'] = checks_str
            elif cloud_provider == 'GCP':
                check_columns['gcp_checks'] = checks_str
            elif cloud_provider == 'ORACLE':
                check_columns['oracle_checks'] = checks_str
            elif cloud_provider == 'IBM':
                check_columns['ibm_checks'] = checks_str
            elif cloud_provider == 'ALICLOUD':
                check_columns['alicloud_checks'] = checks_str
            elif cloud_provider == 'KUBERNETES':
                check_columns['k8s_checks'] = checks_str
            
            # Generate unique ID
            unique_id = generate_unique_id(f"cis_{cloud_provider.lower()}", cloud_provider, req_id, data['title'], req_counter)
            
            record = {
                'unique_compliance_id': unique_id,
                'technology': cloud_provider,
                'compliance_framework': 'CIS',
                'framework_id': f"cis_{cloud_provider.lower()}",
                'framework_version': framework_version,
                'requirement_id': req_id,
                'requirement_name': data['title'] or 'NA',
                'requirement_description': data['description'] or 'NA',
                'section': data['section'] or 'NA',
                'service': infer_service_from_checks(checks_str),
                'total_checks': len(data['checks']),
                'automation_type': data['automation_type'],
                'confidence_score': avg_confidence,
                'references': data['references'] or 'NA',
                'source_file': file_path.name,
                **check_columns
            }
            
            results.append(record)
            
    except Exception as e:
        print(f"    ERROR processing {file_path.name}: {e}")
    
    return results


def main():
    """Main consolidation function"""
    print("=" * 80)
    print("COMPLIANCE RULES CONSOLIDATION")
    print("=" * 80)
    print()
    
    all_records = []
    
    # Process standard compliance frameworks
    print("Processing Standard Compliance Frameworks...")
    print("-" * 80)
    
    for framework_dir in FRAMEWORK_MAPPING.keys():
        framework_path = BASE_DIR / framework_dir
        if not framework_path.exists():
            continue
        
        # Look for controls_with_checks.csv files
        csv_files = list(framework_path.glob('*controls_with_checks.csv'))
        
        for csv_file in csv_files:
            records = process_standard_compliance_file(csv_file, framework_dir)
            all_records.extend(records)
            print(f"    Added {len(records)} records")
    
    print()
    print("Processing CIS Compliance Agent Files...")
    print("-" * 80)
    
    # Process CIS agent files
    cis_agent_dir = BASE_DIR / 'cis_compliance_agent'
    if cis_agent_dir.exists():
        for agent_dir_name, cloud_provider in CIS_CLOUD_MAPPING.items():
            agent_dir = cis_agent_dir / agent_dir_name
            if not agent_dir.exists():
                continue
            
            # Look for FINAL CSV files
            csv_files = list(agent_dir.glob('*_controls_FINAL_*.csv'))
            
            # Get the most recent file (not BACKUP)
            csv_files = [f for f in csv_files if 'BACKUP' not in f.name]
            
            if csv_files:
                # Use the first (most recent) file
                csv_file = sorted(csv_files, reverse=True)[0]
                records = process_cis_agent_file(csv_file, cloud_provider)
                all_records.extend(records)
                print(f"    Added {len(records)} records from {cloud_provider}")
    
    # Write consolidated CSV
    print()
    print("=" * 80)
    print(f"Total records collected: {len(all_records)}")
    print("=" * 80)
    print()
    
    if all_records:
        output_file = OUTPUT_DIR / f'consolidated_compliance_rules_{datetime.now().strftime("%Y-%m-%d")}.csv'
        
        fieldnames = [
            'unique_compliance_id',
            'technology',
            'compliance_framework',
            'framework_id',
            'framework_version',
            'requirement_id',
            'requirement_name',
            'requirement_description',
            'section',
            'service',
            'total_checks',
            'aws_checks',
            'azure_checks',
            'gcp_checks',
            'oracle_checks',
            'ibm_checks',
            'alicloud_checks',
            'k8s_checks',
            'automation_type',
            'confidence_score',
            'references',
            'source_file'
        ]
        
        print(f"Writing consolidated CSV to: {output_file}")
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_records)
        
        print(f"✓ Successfully created: {output_file}")
        print(f"✓ Total records: {len(all_records)}")
        
        # Generate statistics
        print()
        print("=" * 80)
        print("STATISTICS")
        print("=" * 80)
        
        frameworks = defaultdict(int)
        technologies = defaultdict(int)
        automated_count = 0
        manual_count = 0
        
        for record in all_records:
            frameworks[record['compliance_framework']] += 1
            technologies[record['technology']] += 1
            if record['automation_type'] == 'automated':
                automated_count += 1
            else:
                manual_count += 1
        
        print("\nBy Compliance Framework:")
        for framework, count in sorted(frameworks.items()):
            print(f"  {framework:20s}: {count:5d} controls")
        
        print("\nBy Technology:")
        for tech, count in sorted(technologies.items()):
            print(f"  {tech:15s}: {count:5d} controls")
        
        print(f"\nAutomation Status:")
        print(f"  Automated: {automated_count:5d} ({automated_count/len(all_records)*100:.1f}%)")
        print(f"  Manual:    {manual_count:5d} ({manual_count/len(all_records)*100:.1f}%)")
        
        print()
        print("=" * 80)
        print("CONSOLIDATION COMPLETE!")
        print("=" * 80)
    else:
        print("WARNING: No records were collected!")


if __name__ == '__main__':
    main()

