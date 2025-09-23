#!/usr/bin/env python3
"""
Apply Phase 2 mapping using the new rule database
"""

import csv
import json
import re
from typing import Dict, List, Any, Optional

def load_database(file_path: str) -> Dict[str, Any]:
    """Load a JSON database file"""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return {}

def find_best_rule_match(control_text: str, rules_db: List[Dict]) -> Optional[Dict]:
    """Find the best matching rule based on keywords"""
    if not rules_db:
        return None
    
    # Extract keywords from control text
    keywords = re.findall(r'\b\w+\b', control_text.lower())
    
    best_match = None
    best_score = 0
    
    for rule in rules_db:
        score = 0
        rule_text = f"{rule.get('rule_id', '')} {rule.get('description', '')} {rule.get('service', '')} {rule.get('resource_type', '')}".lower()
        
        # Score based on keyword matches
        for keyword in keywords:
            if keyword in rule_text:
                if keyword in ['api', 'server', 'pod', 'security', 'permission', 'file', 'config']:
                    score += 3  # High priority keywords
                elif keyword in ['ensure', 'set', 'restrictive', 'ownership', 'root']:
                    score += 2  # Medium priority keywords
                else:
                    score += 1  # Low priority keywords
        
        if score > best_score:
            best_score = score
            best_match = rule
    
    return best_match if best_score >= 3 else None

def find_assertion_match(control_text: str, assertions_db: List[Dict]) -> Optional[Dict]:
    """Find the best matching assertion based on keywords"""
    if not assertions_db:
        return None
    
    keywords = re.findall(r'\b\w+\b', control_text.lower())
    
    best_match = None
    best_score = 0
    
    for assertion in assertions_db:
        score = 0
        assertion_text = f"{assertion.get('assertion_id', '')} {assertion.get('description', '')}".lower()
        
        for keyword in keywords:
            if keyword in assertion_text:
                if keyword in ['security', 'permission', 'file', 'config', 'hardening']:
                    score += 3
                elif keyword in ['ensure', 'set', 'restrictive', 'ownership']:
                    score += 2
                else:
                    score += 1
        
        if score > best_score:
            best_score = score
            best_match = assertion
    
    return best_match if best_score >= 2 else None

def find_matrix_service_match(control_text: str, matrix_db: Dict) -> Optional[str]:
    """Find the best matching service in matrix database"""
    if not matrix_db:
        return None
    
    keywords = re.findall(r'\b\w+\b', control_text.lower())
    
    best_match = None
    best_score = 0
    
    for service_key in matrix_db.keys():
        score = 0
        service_text = service_key.lower()
        
        for keyword in keywords:
            if keyword in service_text:
                if keyword in ['compute', 'host', 'security', 'os', 'hardening']:
                    score += 3
                elif keyword in ['file', 'permission', 'config']:
                    score += 2
                else:
                    score += 1
        
        if score > best_score:
            best_score = score
            best_match = service_key
    
    return best_match if best_score >= 2 else None

def create_compliance_check(control: Dict, rule_match: Optional[Dict], assertion_match: Optional[Dict], matrix_service: Optional[str]) -> Dict:
    """Create compliance check based on Phase 1 analysis and database matches"""
    
    # Parse Phase 1 recommendation
    try:
        expert_rec = json.loads(control.get('provider_expert_recommendation', '{}'))
    except:
        expert_rec = {}
    
    api_feasibility = expert_rec.get('api_feasibility', 'manual_only')
    
    # Determine check type
    if api_feasibility == 'fully_automated':
        check_type = 'programmatic'
    elif api_feasibility == 'manual_only':
        check_type = 'manual'
    else:
        check_type = 'hybrid'
    
    # Create compliance check structure
    compliance_check = {
        "check_name": f"Automated {control.get('control_title', '')}",
        "check_description": f"Programmatic validation of {control.get('control_title', '').lower()}",
        "check_methods": []
    }
    
    if check_type == 'programmatic':
        # Create programmatic check
        programmatic_check = {
            "programmatic_check": {
                "automation_level": "FULLY_AUTOMATED",
                "method": expert_rec.get('recommended_method', 'Kubernetes API calls and kubectl commands'),
                "description": f"Automated validation of {control.get('control_title', '').lower()}",
                "expected_result": "Configuration meets compliance requirements",
                "api_details": {
                    "endpoints": expert_rec.get('apis_to_check', ['/api/v1/pods']),
                    "resource_field_path": "spec.containers[0].args[]",
                    "conditions_map": {
                        "conditions": [
                            {
                                "field": "spec.containers[0].args[]",
                                "operator": "contains",
                                "value": "--secure-port=6443",
                                "description": f"Check that the pod specification file contains secure configuration and validate file permissions via kubectl exec"
                            }
                        ]
                    }
                },
                "kubectl_commands": expert_rec.get('kubectl_commands', ['kubectl get pods -n kube-system']),
                "validation_criteria": f"Validate {control.get('control_title', '').lower()} using Kubernetes APIs and commands"
            }
        }
        compliance_check["check_methods"].append(programmatic_check)
    
    elif check_type == 'manual':
        # Create manual check
        manual_check = {
            "manual_check": {
                "automation_level": "MANUAL_ONLY",
                "method": expert_rec.get('recommended_method', 'Manual inspection'),
                "description": f"Manual validation of {control.get('control_title', '').lower()}",
                "expected_result": "Manual verification confirms compliance",
                "validation_criteria": expert_rec.get('validation_strategy', 'Manual inspection required'),
                "dangerous_patterns": expert_rec.get('dangerous_patterns', ['N/A'])
            }
        }
        compliance_check["check_methods"].append(manual_check)
    
    else:  # hybrid
        # Create hybrid check
        hybrid_check = {
            "hybrid_check": {
                "automation_level": "HYBRID",
                "method": expert_rec.get('recommended_method', 'Combination of API checks and manual verification'),
                "description": f"Hybrid validation of {control.get('control_title', '').lower()}",
                "expected_result": "Combined validation confirms compliance",
                "api_details": {
                    "endpoints": expert_rec.get('apis_to_check', ['/api/v1/pods']),
                    "resource_field_path": "spec.containers[0].args[]",
                    "conditions_map": {
                        "conditions": [
                            {
                                "field": "spec.containers[0].args[]",
                                "operator": "contains",
                                "value": "--secure-port=6443",
                                "description": f"Check that the pod specification file contains secure configuration"
                            }
                        ]
                    }
                },
                "kubectl_commands": expert_rec.get('kubectl_commands', ['kubectl get pods -n kube-system']),
                "manual_steps": ["Manual verification of file permissions"],
                "validation_criteria": f"Combined validation of {control.get('control_title', '').lower()}"
            }
        }
        compliance_check["check_methods"].append(hybrid_check)
    
    return compliance_check

def create_database_validation_feedback(rule_match: Optional[Dict], assertion_match: Optional[Dict], matrix_service: Optional[str]) -> Dict:
    """Create database validation feedback"""
    
    feedback = {
        "service_name_validation": {
            "found_in_database": matrix_service is not None,
            "database_value": matrix_service if matrix_service else "not_available_in_database",
            "validation_status": "validated" if matrix_service else "not_found"
        },
        "resource_type_validation": {
            "found_in_database": rule_match is not None,
            "database_value": rule_match.get('resource_type', 'not_available_in_database') if rule_match else "not_available_in_database",
            "validation_status": "validated" if rule_match else "not_found"
        },
        "assertion_id_validation": {
            "found_in_database": assertion_match is not None,
            "database_value": assertion_match.get('assertion_id', 'not_available_in_database') if assertion_match else "not_available_in_database",
            "validation_status": "validated" if assertion_match else "not_found"
        },
        "rule_id_validation": {
            "found_in_database": rule_match is not None,
            "database_value": rule_match.get('rule_id', 'not_available_in_database') if rule_match else "not_available_in_database",
            "validation_status": "validated" if rule_match else "not_found"
        }
    }
    
    return feedback

def main():
    print("=== PHASE 2 MAPPING WITH NEW RULE DATABASE ===")
    
    # Load databases
    print("Loading databases...")
    
    # Load new rules database
    rules_db = load_database('/Users/apple/Desktop/compliance_Database/rule-generator-engine/step4-rune-per-cloud-provider/k8s_rules_complete_145_2025-01-27.json')
    if 'rules' in rules_db:
        rules_list = rules_db['rules']
    else:
        rules_list = []
    
    # Load assertions database
    assertions_db = load_database('/Users/apple/Desktop/compliance_Database/rule-generator-engine/step-2-common-assercian-id/assertions_pack_k8s_2025-01-27T20-00-00.json')
    if 'assertions' in assertions_db:
        assertions_list = assertions_db['assertions']
    else:
        assertions_list = []
    
    # Load matrix database
    matrix_db = load_database('/Users/apple/Desktop/compliance_Database/simplified_combined_assertion_matrix_database.json')
    
    print(f"Loaded {len(rules_list)} rules, {len(assertions_list)} assertions, {len(matrix_db)} matrix entries")
    
    # Read Phase 1 output
    print("Reading Phase 1 output...")
    phase1_file = '/Users/apple/Desktop/compliance_Database/raw_compliance_database/cloud/kubernetes/native_kubernetes/combined_kubernetes_compliance_with_expert_recommendations_clean.csv'
    
    controls = []
    with open(phase1_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        controls = list(reader)
    
    print(f"Processing {len(controls)} controls...")
    
    # Process each control
    results = []
    for i, control in enumerate(controls):
        print(f"Processing control {i+1}/{len(controls)}: {control.get('control_title', '')[:50]}...")
        
        # Find database matches
        control_text = f"{control.get('control_title', '')} {control.get('description', '')}"
        
        rule_match = find_best_rule_match(control_text, rules_list)
        assertion_match = find_assertion_match(control_text, assertions_list)
        matrix_service = find_matrix_service_match(control_text, matrix_db)
        
        # Create compliance check
        compliance_check = create_compliance_check(control, rule_match, assertion_match, matrix_service)
        
        # Create database validation feedback
        db_validation = create_database_validation_feedback(rule_match, assertion_match, matrix_service)
        
        # Determine check type
        try:
            expert_rec = json.loads(control.get('provider_expert_recommendation', '{}'))
            api_feasibility = expert_rec.get('api_feasibility', 'manual_only')
            if api_feasibility == 'fully_automated':
                check_type = 'programmatic'
            elif api_feasibility == 'manual_only':
                check_type = 'manual'
            else:
                check_type = 'hybrid'
        except:
            check_type = 'manual'
        
        # Create result
        result = {
            'control_id': control.get('control_id', ''),
            'control_title': control.get('control_title', ''),
            'provider_expert_recommendation': control.get('provider_expert_recommendation', ''),
            'check_type': check_type,
            'compliance_checks': json.dumps([compliance_check], indent=2),
            'database_validation_feedback': json.dumps(db_validation, indent=2)
        }
        
        results.append(result)
    
    # Write Phase 2 output
    output_file = '/Users/apple/Desktop/compliance_Database/raw_compliance_database/cloud/kubernetes/native_kubernetes/combined_kubernetes_compliance_phase2_new_rules_final.csv'
    
    print(f"Writing Phase 2 output to {output_file}...")
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['control_id', 'control_title', 'provider_expert_recommendation', 'check_type', 'compliance_checks', 'database_validation_feedback']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    
    print(f"Phase 2 mapping completed! Output saved to {output_file}")
    
    # Summary
    check_types = {}
    for result in results:
        ct = result['check_type']
        check_types[ct] = check_types.get(ct, 0) + 1
    
    print(f"\n=== SUMMARY ===")
    print(f"Total controls processed: {len(results)}")
    print(f"Check type distribution:")
    for ct, count in check_types.items():
        print(f"  {ct}: {count}")

if __name__ == "__main__":
    main()

