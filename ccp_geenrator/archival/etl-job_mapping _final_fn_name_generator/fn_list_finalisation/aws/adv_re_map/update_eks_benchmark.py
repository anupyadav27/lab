#!/usr/bin/env python3
"""
Update CIS EKS BENCHMARK V1.7.0 with proper function mappings
and data_status completion using our proven methodology.
"""

import json
import os
from datetime import datetime

def load_function_database():
    """Load the service function list database"""
    with open('service_function_list.json', 'r') as f:
        return json.load(f)

def get_relevant_functions(control_description, control_title):
    """Get relevant functions from the database based on control context"""
    functions_db = load_function_database()

    # Extract key terms from control
    terms = (control_title + " " + control_description).lower()

    relevant_functions = []

    # Map controls to relevant services and functions based on EKS context
    if "audit log" in terms and "control plane" in terms:
        # Control 2.1.1: Enable audit Logs
        relevant_functions = [
            "eks_control_plane_logging_all_types_enabled",
            "eks_control_plane_logs_exported_to_cloudwatch"
        ]

    elif "audit log" in terms and "collected" in terms:
        # Control 2.1.2: Ensure audit logs are collected and managed
        relevant_functions = [
            "eks_control_plane_logs_exported"
        ]

    elif "kubeconfig" in terms and "permission" in terms:
        # Control 3.1.1: kubeconfig file permissions
        relevant_functions = [
            "eks_kubeconfig_file_permission_check"
        ]

    elif "kubeconfig" in terms and "ownership" in terms:
        # Control 3.1.2: kubeconfig file ownership
        relevant_functions = [
            "eks_kubelet_kubeconfig_file_ownership_check"
        ]

    elif "kubelet" in terms and "configuration" in terms and "permission" in terms:
        # Control 3.1.3: kubelet configuration file permissions
        relevant_functions = [
            "eks_kubelet_config_file_permission_check"
        ]

    elif "kubelet" in terms and "configuration" in terms and "ownership" in terms:
        # Control 3.1.4: kubelet configuration file ownership
        relevant_functions = [
            "eks_kubelet_config_file_ownership_check"
        ]

    elif "anonymous" in terms and "auth" in terms:
        # Control 3.2.1: Anonymous Auth Not Enabled
        relevant_functions = [
            "eks_cluster_iam_authenticator_enabled"
        ]

    elif "network policy" in terms:
        # Controls related to network policies
        relevant_functions = [
            "eks_cluster_network_policy_enabled",
            "eks_namespace_network_policy_check"
        ]

    elif "pod security" in terms:
        # Controls related to pod security policies
        relevant_functions = [
            "eks_pod_security_policies_enforced",
            "eks_pod_security_policy_no_privileged_containers"
        ]

    elif "secrets" in terms and "encryption" in terms:
        # Controls related to secrets encryption
        relevant_functions = [
            "eks_cluster_secrets_encryption_check",
            "eks_cluster_kms_cmk_encryption_in_secrets_enabled"
        ]

    elif "public access" in terms or "publicly accessible" in terms:
        # Controls related to public access
        relevant_functions = [
            "eks_cluster_not_publicly_accessible",
            "eks_cluster_public_access_disabled"
        ]

    elif "private endpoint" in terms:
        # Controls related to private endpoints
        relevant_functions = [
            "eks_cluster_private_endpoint_enabled",
            "eks_cluster_control_plane_endpoint_private_access"
        ]

    elif "vulnerability" in terms and "scan" in terms:
        # Controls related to vulnerability scanning
        relevant_functions = [
            "eks_image_vulnerability_scanning_check"
        ]

    elif "rbac" in terms or "role" in terms:
        # Controls related to RBAC and access control
        relevant_functions = [
            "eks_rbac_users_managed_with_iam_authenticator",
            "eks_cluster_limit_bind_permission"
        ]

    elif "namespace" in terms and "isolation" in terms:
        # Controls related to namespace isolation
        relevant_functions = [
            "eks_namespace_isolation_check",
            "eks_default_namespace_usage_check"
        ]

    # Filter to only include functions that actually exist in the database
    available_functions = []
    for func in relevant_functions:
        for service_name, service_data in functions_db.get('services', {}).items():
            if func in service_data.get('programmable', []):
                available_functions.append(func)
                break

    return available_functions if available_functions else ["manual_check_required"]

def get_manual_effort(control_description, control_title):
    """Get specific manual effort steps based on control context"""
    terms = (control_title + " " + control_description).lower()
    
    if "console" in terms or "gui" in terms:
        return "Review AWS EKS Console for compliance status"
    elif "kubectl" in terms or "kubernetes" in terms:
        return "Run kubectl commands to verify cluster configuration and policies"
    elif "ssh" in terms or "worker node" in terms:
        return "SSH to worker nodes to check file permissions and ownership"
    elif "pod" in terms and "privileged" in terms:
        return "Deploy privileged pods to check host file system configurations"
    elif "audit" in terms and "policy" in terms:
        return "Review and configure Kubernetes audit policies and log forwarding"
    elif "network policy" in terms:
        return "Verify network policies are properly configured and enforced"
    elif "rbac" in terms:
        return "Review RBAC configurations and IAM authenticator settings"
    elif "secrets" in terms:
        return "Verify KMS encryption for Kubernetes secrets"
    elif "vulnerability" in terms:
        return "Check vulnerability scanning results and remediation status"
    else:
        return "Manual review required - check EKS cluster configuration and documentation"

def get_new_function_suggestion(control_description, control_title):
    """Get specific new function suggestions based on control context"""
    terms = (control_title + " " + control_description).lower()
    
    if "audit log" in terms and "management" in terms:
        return "eks_audit_log_management_check - Verify audit log collection, storage, and monitoring across all Kubernetes components"
    elif "kubelet" in terms and "file" in terms:
        return "eks_kubelet_file_security_check - Comprehensive check for kubelet configuration file permissions and ownership"
    elif "anonymous" in terms:
        return "eks_anonymous_auth_disabled_check - Verify anonymous authentication is disabled across all kubelet instances"
    elif "network policy" in terms and "enforcement" in terms:
        return "eks_network_policy_enforcement_check - Verify network policies are properly enforced and monitored"
    elif "pod security" in terms and "standards" in terms:
        return "eks_pod_security_standards_check - Verify pod security standards compliance across all namespaces"
    else:
        return "new_function_needed - Specific EKS function required for this compliance control"

def update_control(control):
    """Update a single control with proper function mappings"""
    # Remove assessment field
    if "assessment" in control:
        del control["assessment"]

    # Get relevant functions from database
    relevant_functions = get_relevant_functions(
        control.get("description", ""),
        control.get("title", "")
    )

    # Update function_name (singular)
    if relevant_functions == ["manual_check_required"]:
        control["function_name"] = "manual_check_required"
        control["manual_effort"] = get_manual_effort(
            control.get("description", ""),
            control.get("title", "")
        )
        control["coverage"] = 0  # 0% automated coverage
    elif relevant_functions == ["new_function_required"]:
        control["function_name"] = "new_function_required"
        control["new_function_suggestion"] = get_new_function_suggestion(
            control.get("description", ""),
            control.get("title", "")
        )
        control["coverage"] = 0  # 0% automated coverage
    else:
        control["function_name"] = relevant_functions[0]  # Use first function
        control["coverage"] = 80  # 80% automated coverage

    # Add data_status
    control["data_status"] = "complete"

    return control

def main():
    """Main function to update the EKS benchmark file"""
    input_file = "/Users/apple/Desktop/compliance_Database/final_complaince_database_with_fn_name/aws_function_complaince_mapping/CIS_AMAZON_ELASTIC_KUBERNETES_SERVICE_(EKS)_BENCHMARK_V1.7.0_PDF/CIS_EKS_BENCHMARK_V1.7.0_PDF_updated_20250825_184041.json"

    # Load the EKS benchmark file
    with open(input_file, 'r') as f:
        controls = json.load(f)

    print(f"🔄 Updating {len(controls)} controls in CIS EKS BENCHMARK V1.7.0...")

    # Update each control
    updated_controls = []
    for i, control in enumerate(controls, 1):
        print(f"Processing control {i}/{len(controls)}: {control.get('id', 'Unknown')}")
        updated_control = update_control(control)
        updated_controls.append(updated_control)

    # Generate output filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = input_file.replace('.json', f'_updated_{timestamp}.json')

    # Save updated controls
    with open(output_file, 'w') as f:
        json.dump(updated_controls, f, indent=2)

    print(f"✅ Successfully updated {len(controls)} controls!")
    print(f"📁 Output saved to: {output_file}")

    # Show sample of updated controls
    print("\n📋 Sample Updated Controls:")
    for i, control in enumerate(updated_controls[:3], 1):
        print(f"\n{i}. ID: {control['id']}")
        print(f"   Title: {control['title']}")
        print(f"   Function: {control['function_name']}")
        print(f"   Coverage: {control['coverage']}%")
        if 'manual_effort' in control:
            print(f"   Manual Effort: {control['manual_effort']}")
        if 'new_function_suggestion' in control:
            print(f"   New Function Suggestion: {control['new_function_suggestion']}")
        print(f"   Data Status: {control['data_status']}")

if __name__ == "__main__":
    main()
