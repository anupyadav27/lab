#!/usr/bin/env python3
"""
Update CIS AWS COMPUTE SERVICES BENCHMARK V1.1.0 with proper function mappings
and data_status completion.
"""

import json
import os
from datetime import datetime

def load_function_database():
    """Load the service function list database"""
    with open('service_function_list.json', 'r') as f:
        return json.load(f)

def get_relevant_functions(service, control_description, control_title):
    """Get relevant functions from the database based on control context"""
    functions_db = load_function_database()

    # Extract key terms from control
    terms = (control_title + " " + control_description).lower()

    relevant_functions = []

    # Map controls to relevant services and functions
    if "ami" in terms and "naming" in terms:
        # Control 2.1.1: AMI Naming Convention
        # This requires a function that can check naming patterns - not available in programmable
        relevant_functions = ["new_function_required"]

    elif "ami" in terms and "encrypt" in terms:
        # Control 2.1.2: AMI Encryption
        relevant_functions = [
            "ec2_ami_encryption_check"
        ]

    elif "ami" in terms and "approv" in terms:
        # Control 2.1.3: Approved AMIs
        # This requires approval logic - not available in programmable
        relevant_functions = ["new_function_required"]

    elif "ami" in terms and "90" in terms:
        # Control 2.1.4: AMI Age Check
        relevant_functions = [
            "ec2_ami_older_than_90_days"
        ]

    elif "ami" in terms and "public" in terms:
        # Control 2.1.5: AMI Public Access
        relevant_functions = [
            "ec2_ami_public"
        ]

    elif "ebs" in terms and "encrypt" in terms:
        # Control 2.2.1: EBS Encryption
        relevant_functions = [
            "ec2_ebs_default_encryption"
        ]

    elif "snapshot" in terms and "encrypt" in terms:
        # Control 2.2.2: EBS Snapshot Encryption
        relevant_functions = [
            "ec2_ebs_snapshots_encrypted"
        ]

    elif "instance" in terms and "security" in terms:
        # Control 2.3.x: Instance Security
        relevant_functions = [
            "ec2_instance_security_group_configuration_check"
        ]

    elif "security group" in terms:
        # Control 2.4.x: Security Groups
        relevant_functions = [
            "ec2_default_security_group_no_inbound_rules"
        ]

    elif "monitor" in terms or "logging" in terms:
        # Control 2.5.x: Monitoring & Logging
        relevant_functions = [
            "ec2_instance_detailed_monitoring_enabled"
        ]

    # Filter to only include functions that actually exist in the database
    available_functions = []
    for func in relevant_functions:
        if func == "new_function_required":
            available_functions.append(func)
        else:
            for service_name, service_data in functions_db.get('services', {}).items():
                if func in service_data.get('programmable', []):
                    available_functions.append(func)
                    break

    return available_functions if available_functions else ["manual_check_required"]

def get_manual_effort(control_description, control_title):
    """Get specific manual effort steps based on control context"""
    terms = (control_title + " " + control_description).lower()

    if "console" in terms or "gui" in terms:
        return "Review AWS Console GUI for compliance status"
    elif "policy" in terms or "organiz" in terms:
        return "Check AWS Organizations policy documents and settings"
    elif "cli" in terms or "command" in terms:
        return "Run AWS CLI commands to verify compliance"
    elif "tag" in terms:
        return "Review resource tagging in AWS Console and verify tag policies"
    elif "monitor" in terms or "logging" in terms:
        return "Check CloudWatch logs and monitoring configuration in AWS Console"
    elif "security" in terms and "group" in terms:
        return "Review Security Group rules in EC2 Console and verify access controls"
    elif "backup" in terms:
        return "Verify AWS Backup plans and retention policies in Console"
    elif "encryption" in terms:
        return "Check encryption settings in respective service consoles"
    else:
        return "Manual review required - check AWS Console and documentation"

def get_new_function_suggestion(control_description, control_title):
    """Get specific new function suggestions based on control context"""
    terms = (control_title + " " + control_description).lower()
    
    if "ami" in terms and "naming" in terms:
        return "ec2_ami_naming_convention_validation - Check AMI names against organizational naming patterns using regex or policy rules"
    elif "ami" in terms and "approv" in terms:
        return "ec2_ami_approval_status_check - Verify AMIs are in approved list/registry and meet organizational standards"
    elif "tag" in terms and "policy" in terms:
        return "ec2_tag_policy_compliance_check - Validate EC2 resource tags against organizational tag policies"
    elif "organization" in terms:
        return "aws_org_policy_compliance_check - Verify organizational policies are properly configured and enforced"
    else:
        return "new_function_needed - Specific function required for this compliance control"

def update_control(control):
    """Update a single control with proper function mappings"""
    # Remove assessment field
    if "assessment" in control:
        del control["assessment"]

    # Get relevant functions from database
    relevant_functions = get_relevant_functions(
        control.get("id", ""),
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
    """Main function to update the CIS benchmark file"""
    input_file = "/Users/apple/Desktop/compliance_Database/final_complaince_database_with_fn_name/aws_function_complaince_mapping/CIS AWS COMPUTE SERVICES BENCHMARK V1.1.0/CIS AWS COMPUTE SERVICES BENCHMARK V1.1.0_updated_20250825_183711.json"

    # Load the CIS benchmark file
    with open(input_file, 'r') as f:
        controls = json.load(f)

    print(f"🔄 Updating {len(controls)} controls in CIS AWS COMPUTE SERVICES BENCHMARK...")

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
