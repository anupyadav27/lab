#!/usr/bin/env python3
"""
EKS Three-Tier Audit Mapper
Implements minimum essential function mapping with three-tier audit approach:
1. Program Only (80% coverage) - Fully automated
2. Hybrid (60% coverage) - Program + manual verification  
3. Manual Only (0% coverage) - Fully manual
"""
import json
import os
from datetime import datetime

def load_function_database():
    """Load the service function list database"""
    db_path = "/Users/apple/Desktop/compliance_Database/etl-job_mapping _final_fn_name_generator/fn_list_finalisation/aws/adv_re_map/service_function_list.json"
    with open(db_path, 'r') as f:
        return json.load(f)

def get_audit_type(control_description, control_title):
    """Determine audit type based on control content"""
    terms = (control_title + " " + control_description).lower()
    
    # Controls that can be fully automated via API calls
    if any(keyword in terms for keyword in [
        "audit log", "secrets encryption", "public access", "private endpoint", 
        "vulnerability scan", "rbac", "namespace isolation", "cluster logging",
        "control plane logging", "cloudwatch", "kms encryption"
    ]):
        return "program_only"
    
    # Controls that need hybrid approach (program + manual verification)
    elif any(keyword in terms for keyword in [
        "kubeconfig", "kubelet", "network policy", "pod security", "file permission",
        "file ownership", "worker node configuration", "node security"
    ]):
        return "hybrid"
    
    # Controls that can only be manual (require SSH, file system access, etc.)
    elif any(keyword in terms for keyword in [
        "authorization mode", "ssh", "command line argument", "process argument",
        "systemd service", "service file", "host file system", "privileged pod"
    ]):
        return "manual_only"
    
    # Default to hybrid for complex controls
    else:
        return "hybrid"

def get_minimum_essential_functions(control_description, control_title):
    """Get minimum essential programmable functions for the control"""
    functions_db = load_function_database()
    terms = (control_title + " " + control_description).lower()
    relevant_functions = []

    # Map controls to minimum essential functions
    if "audit log" in terms and "control plane" in terms:
        relevant_functions = ["eks_control_plane_logging_all_types_enabled"]
    elif "audit log" in terms and "collected" in terms:
        relevant_functions = ["eks_control_plane_logs_exported"]
    elif "kubeconfig" in terms and "permission" in terms:
        relevant_functions = ["eks_kubeconfig_file_permission_check"]
    elif "kubeconfig" in terms and "ownership" in terms:
        relevant_functions = ["eks_kubelet_kubeconfig_file_ownership_check"]
    elif "kubelet" in terms and "configuration" in terms and "permission" in terms:
        relevant_functions = ["eks_kubelet_config_file_permission_check"]
    elif "kubelet" in terms and "configuration" in terms and "ownership" in terms:
        relevant_functions = ["eks_kubelet_config_file_ownership_check"]
    elif "anonymous" in terms and "auth" in terms:
        relevant_functions = ["eks_cluster_iam_authenticator_enabled"]
    elif "network policy" in terms:
        relevant_functions = ["eks_cluster_network_policy_enabled"]
    elif "pod security" in terms:
        relevant_functions = ["eks_pod_security_policies_enforced"]
    elif "secrets" in terms and "encryption" in terms:
        relevant_functions = ["eks_cluster_secrets_encryption_check"]
    elif "public access" in terms or "publicly accessible" in terms:
        relevant_functions = ["eks_cluster_not_publicly_accessible"]
    elif "private endpoint" in terms:
        relevant_functions = ["eks_cluster_private_endpoint_enabled"]
    elif "vulnerability" in terms and "scan" in terms:
        relevant_functions = ["eks_image_vulnerability_scanning_check"]
    elif "rbac" in terms or "role" in terms:
        relevant_functions = ["eks_rbac_users_managed_with_iam_authenticator"]
    elif "namespace" in terms and "isolation" in terms:
        relevant_functions = ["eks_namespace_isolation_check"]

    # Check if functions exist in database
    available_functions = []
    for func in relevant_functions:
        for service_name, service_data in functions_db.get('services', {}).items():
            if func in service_data.get('programmable', []):
                available_functions.append(func)
                break
    
    return available_functions if available_functions else []

def get_manual_effort(control_description, control_title, audit_type):
    """Get specific manual effort steps based on audit type"""
    terms = (control_title + " " + control_description).lower()
    
    if audit_type == "manual_only":
        if "authorization mode" in terms:
            return "SSH to worker nodes and check kubelet configuration files for --authorization-mode argument"
        elif "worker node" in terms or "ssh" in terms:
            return "SSH to worker nodes to check file permissions and ownership"
        elif "file permission" in terms or "file ownership" in terms:
            return "Verify file permissions and ownership on worker nodes via SSH"
        elif "command line argument" in terms or "process argument" in terms:
            return "Check kubelet process arguments and service configuration files"
        else:
            return "Manual review required - check EKS cluster configuration and documentation"
    
    elif audit_type == "hybrid":
        if "kubeconfig" in terms:
            return "Verify kubeconfig file settings in addition to programmatic checks"
        elif "kubelet" in terms:
            return "Verify kubelet configuration files on worker nodes via SSH"
        elif "network policy" in terms:
            return "Verify network policies are properly configured and enforced in cluster"
        elif "pod security" in terms:
            return "Verify pod security policies are active and enforced"
        else:
            return "Additional manual verification required alongside programmatic checks"
    
    else:
        return "No manual effort required - fully automated"

def get_new_function_suggestion(control_description, control_title):
    """Get specific new function suggestions for controls that need automation"""
    terms = (control_title + " " + control_description).lower()
    
    if "authorization mode" in terms:
        return "eks_kubelet_authorization_mode_check - Verify kubelet authorization mode via API or configuration inspection"
    elif "worker node" in terms and "ssh" in terms:
        return "eks_worker_node_security_check - Comprehensive worker node security validation via privileged pods"
    elif "file permission" in terms:
        return "eks_file_security_validation - Automated file permission and ownership checking via privileged containers"
    else:
        return "new_function_needed - Specific EKS function required for this compliance control"

def map_control(control):
    """Map a single control using the three-tier approach"""
    print(f"\n=== Processing Control {control.get('id', 'Unknown')} ===")
    
    # Remove old fields
    if "assessment" in control:
        del control["assessment"]
    if "function_names" in control:
        del control["function_names"]
    
    # Determine audit type
    audit_type = get_audit_type(
        control.get("description", ""),
        control.get("title", "")
    )
    print(f"  Audit type: {audit_type}")
    
    if audit_type == "manual_only":
        print("  Processing as MANUAL_ONLY")
        control["function_name"] = "manual_check_required"
        control["manual_effort"] = get_manual_effort(
            control.get("description", ""),
            control.get("title", ""),
            audit_type
        )
        control["coverage"] = 0
        control["audit_approach"] = "manual_only"
        
    elif audit_type == "hybrid":
        print("  Processing as HYBRID")
        essential_functions = get_minimum_essential_functions(
            control.get("description", ""),
            control.get("title", "")
        )
        print(f"  Essential functions found: {essential_functions}")
        
        if essential_functions:
            # Programmatic function found, add manual verification
            control["function_name"] = essential_functions[0]
            control["manual_effort"] = get_manual_effort(
                control.get("description", ""),
                control.get("title", ""),
                audit_type
            )
            control["coverage"] = 60  # Program + manual verification
            control["audit_approach"] = "hybrid"
        else:
            # No programmatic function found, but hybrid approach needed
            control["function_name"] = "new_function_required"
            control["new_function_suggestion"] = get_new_function_suggestion(
                control.get("description", ""),
                control.get("title", "")
            )
            control["manual_effort"] = get_manual_effort(
                control.get("description", ""),
                control.get("title", ""),
                audit_type
            )
            control["coverage"] = 0
            control["audit_approach"] = "hybrid_no_function"
    
    else:  # program_only
        print("  Processing as PROGRAM_ONLY")
        essential_functions = get_minimum_essential_functions(
            control.get("description", ""),
            control.get("title", "")
        )
        print(f"  Essential functions found: {essential_functions}")
        
        if essential_functions:
            control["function_name"] = essential_functions[0]
            control["coverage"] = 80  # Fully automated
            control["audit_approach"] = "program_only"
        else:
            # No programmatic function found, but should be automated
            control["function_name"] = "new_function_required"
            control["new_function_suggestion"] = get_new_function_suggestion(
                control.get("description", ""),
                control.get("title", "")
            )
            control["coverage"] = 0
            control["audit_approach"] = "program_only_no_function"
    
    control["data_status"] = "complete"
    print(f"  Final mapping: {control['function_name']} | Coverage: {control['coverage']}% | Approach: {control['audit_approach']}")
    print("=== End Processing ===\n")
    
    return control

def main():
    """Main function to map EKS controls using three-tier approach"""
    input_file = "CIS_EKS_BENCHMARK_V1.7.0_PDF_updated_20250825_184041.json"
    
    print("🚀 Starting EKS Three-Tier Audit Mapping...")
    print(f"📁 Input file: {input_file}")
    
    # Load controls
    with open(input_file, 'r') as f:
        controls = json.load(f)
    
    print(f"📊 Processing {len(controls)} controls...")
    
    # Map each control
    mapped_controls = []
    for i, control in enumerate(controls, 1):
        print(f"Processing control {i}/{len(controls)}: {control.get('id', 'Unknown')}")
        mapped_control = map_control(control)
        mapped_controls.append(mapped_control)
    
    # Generate output filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"EKS_Three_Tier_Mapped_{timestamp}.json"
    
    # Save results
    with open(output_file, 'w') as f:
        json.dump(mapped_controls, f, indent=2)
    
    print(f"\n✅ Successfully mapped {len(controls)} controls!")
    print(f"📁 Output saved to: {output_file}")
    
    # Summary statistics
    program_only = sum(1 for c in mapped_controls if c.get('audit_approach') == 'program_only')
    hybrid = sum(1 for c in mapped_controls if c.get('audit_approach') == 'hybrid')
    manual_only = sum(1 for c in mapped_controls if c.get('audit_approach') == 'manual_only')
    new_function_needed = sum(1 for c in mapped_controls if c.get('function_name') == 'new_function_required')
    
    print(f"\n📋 Mapping Summary:")
    print(f"   Program Only: {program_only} controls")
    print(f"   Hybrid: {hybrid} controls") 
    print(f"   Manual Only: {manual_only} controls")
    print(f"   New Functions Needed: {new_function_needed} controls")
    
    # Sample outputs
    print(f"\n📋 Sample Mapped Controls:")
    for i, control in enumerate(mapped_controls[:3], 1):
        print(f"\n{i}. ID: {control['id']}")
        print(f"   Title: {control['title']}")
        print(f"   Function: {control['function_name']}")
        print(f"   Coverage: {control['coverage']}%")
        print(f"   Approach: {control['audit_approach']}")
        if 'manual_effort' in control:
            print(f"   Manual Effort: {control['manual_effort']}")
        if 'new_function_suggestion' in control:
            print(f"   New Function Suggestion: {control['new_function_suggestion']}")

if __name__ == "__main__":
    main()
