#!/usr/bin/env python3
"""
Create Organized GCP Service Prompts

This script creates service prompts organized by service folders:
gcp_service_prompts/
├── iam/
│   ├── iam_service_prompt.md
│   └── iam_functions.json
├── compute/
│   ├── compute_service_prompt.md
│   └── compute_functions.json
└── ...
"""

import json
import os
from pathlib import Path

def create_service_folder_structure(base_dir):
    """Create the base directory structure"""
    
    print("📁 Creating service folder structure...")
    
    # Create base directory
    base_path = Path(base_dir)
    base_path.mkdir(exist_ok=True)
    print(f"✅ Created base directory: {base_dir}")
    
    return base_path

def generate_service_prompt_content(service_name, service_data):
    """Generate the content for a service prompt"""
    
    description = service_data.get('description', f'GCP {service_name.upper()} Service')
    total_functions = service_data['total_functions']
    functions = service_data['functions']
    sdk_client = service_data.get('sdk_client', 'unknown')
    service_type = service_data.get('service_type', 'other')
    
    # Create the prompt content
    prompt_content = f"""# GCP {service_name.upper()} Service Compliance Prompt

## Service Information
- **Service Name**: {service_name.upper()}
- **Description**: {description}
- **Total Functions**: {total_functions}
- **SDK Client**: {sdk_client}
- **Service Type**: {service_type}

## Function List
The following {total_functions} functions are available for {service_name.upper()} compliance checks:

"""
    
    # Add functions in a numbered list
    for i, func in enumerate(functions, 1):
        prompt_content += f"{i}. `{func}`\n"
    
    prompt_content += f"""

## Compliance Framework Coverage
This service supports compliance checks for:
- **NIST Cybersecurity Framework**
- **PCI DSS v4.0**
- **ISO 27001**
- **SOC 2**
- **GDPR**
- **HIPAA** (where applicable)

## Usage Instructions
1. Use the function names above to create compliance checks
2. Each function should be implemented as a separate compliance rule
3. Follow the naming convention: `{service_name}_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization

## Example Implementation
```python
def {service_name}_example_function_check():
    \"\"\"
    Example compliance check for {service_name.upper()} service
    \"\"\"
    try:
        # Implementation here
        pass
    except Exception as e:
        logger.error(f"Error in {service_name} check: {{e}}")
        return False
```

## Notes
- All functions are based on GCP {service_name.upper()} API
- Ensure proper IAM permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
"""
    
    return prompt_content

def create_service_folder_and_files(base_path, service_name, service_data):
    """Create folder and files for a specific service"""
    
    print(f"📝 Creating files for {service_name} service...")
    
    # Create service folder
    service_folder = base_path / service_name
    service_folder.mkdir(exist_ok=True)
    
    # Generate prompt content
    prompt_content = generate_service_prompt_content(service_name, service_data)
    
    # Create prompt file
    prompt_file = service_folder / f"{service_name}_service_prompt.md"
    with open(prompt_file, 'w', encoding='utf-8') as f:
        f.write(prompt_content)
    
    # Create functions JSON file
    functions_file = service_folder / f"{service_name}_functions.json"
    with open(functions_file, 'w', encoding='utf-8') as f:
        json.dump({
            'service_name': service_name,
            'description': service_data.get('description', f'GCP {service_name.upper()} Service'),
            'total_functions': service_data['total_functions'],
            'functions': service_data['functions'],
            'sdk_client': service_data.get('sdk_client', 'unknown'),
            'service_type': service_data.get('service_type', 'other')
        }, f, indent=2, ensure_ascii=False)
    
    print(f"  ✅ Created {prompt_file}")
    print(f"  ✅ Created {functions_file}")
    
    return service_folder

def create_service_summary(base_path, services):
    """Create a summary file for all services"""
    
    print("📊 Creating service summary...")
    
    summary_content = """# GCP Services Summary

This directory contains organized service prompts for GCP compliance checks.

## Available Services

"""
    
    # Group services by type
    service_types = {}
    for service_name, service_data in services.items():
        service_type = service_data.get('service_type', 'other')
        if service_type not in service_types:
            service_types[service_type] = []
        service_types[service_type].append({
            'name': service_name,
            'description': service_data.get('description', f'GCP {service_name.upper()} Service'),
            'total_functions': service_data['total_functions'],
            'sdk_client': service_data.get('sdk_client', 'unknown')
        })
    
    # Add services by type
    for service_type, services_list in service_types.items():
        summary_content += f"### {service_type.upper().replace('_', ' ')} Services\n\n"
        
        for service in services_list:
            summary_content += f"- **{service['name']}** ({service['total_functions']} functions)\n"
            summary_content += f"  - Description: {service['description']}\n"
            summary_content += f"  - SDK Client: {service['sdk_client']}\n"
            summary_content += f"  - Folder: `{service['name']}/`\n\n"
    
    # Add total statistics
    total_services = len(services)
    total_functions = sum(service['total_functions'] for service in services.values())
    
    summary_content += f"""## Statistics
- **Total Services**: {total_services}
- **Total Functions**: {total_functions}
- **Service Types**: {len(service_types)}

## Directory Structure
```
gcp_service_prompts/
"""
    
    for service_name in sorted(services.keys()):
        summary_content += f"├── {service_name}/\n"
        summary_content += f"│   ├── {service_name}_service_prompt.md\n"
        summary_content += f"│   └── {service_name}_functions.json\n"
    
    summary_content += "└── README.md (this file)\n"
    
    summary_content += """

## Usage
1. Navigate to the specific service folder
2. Read the service prompt for implementation guidance
3. Use the functions JSON file for function lists
4. Implement compliance checks based on the provided templates

## Service Types
- **Compute**: Virtual machines, containers, serverless
- **Data**: Databases, analytics, data processing
- **Storage**: Object storage, file systems
- **Networking**: VPC, DNS, load balancing
- **Security**: IAM, encryption, security monitoring
- **Monitoring**: Logging, metrics, alerts
- **Management**: Resource management, billing
- **AI/ML**: Machine learning, AI services
- **Workspace**: Google Workspace services
- **Other**: Miscellaneous services
"""
    
    # Create summary file
    summary_file = base_path / "README.md"
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(summary_content)
    
    print(f"✅ Created {summary_file}")

def create_services_summary_json(base_path, services):
    """Create a JSON summary of all services"""
    
    print("📊 Creating services summary JSON...")
    
    summary_data = {
        'metadata': {
            'description': 'GCP Services Summary for Compliance Checks',
            'total_services': len(services),
            'total_functions': sum(service['total_functions'] for service in services.values()),
            'organization': 'service_based_folders',
            'created_at': '2024-08-25'
        },
        'services': {}
    }
    
    for service_name, service_data in services.items():
        summary_data['services'][service_name] = {
            'description': service_data.get('description', f'GCP {service_name.upper()} Service'),
            'total_functions': service_data['total_functions'],
            'sdk_client': service_data.get('sdk_client', 'unknown'),
            'service_type': service_data.get('service_type', 'other'),
            'folder_path': f"{service_name}/",
            'files': [
                f"{service_name}_service_prompt.md",
                f"{service_name}_functions.json"
            ]
        }
    
    # Create summary JSON file
    summary_json_file = base_path / "gcp_services_summary.json"
    with open(summary_json_file, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Created {summary_json_file}")

def main():
    """Main function"""
    
    print("📁 Create Organized GCP Service Prompts")
    print("=" * 60)
    
    # Load the complete service categorization
    try:
        with open('gcp_complete_service_categorization.json', 'r') as f:
            gcp_data = json.load(f)
        print(f"✅ Loaded GCP data: {len(gcp_data['services'])} services")
    except FileNotFoundError:
        print("❌ GCP complete service categorization file not found")
        return
    
    services = gcp_data['services']
    
    # Create base directory structure
    base_dir = "gcp_service_prompts"
    base_path = create_service_folder_structure(base_dir)
    
    # Create folders and files for each service
    created_folders = []
    for service_name, service_data in services.items():
        service_folder = create_service_folder_and_files(base_path, service_name, service_data)
        created_folders.append(service_folder)
    
    # Create summary files
    create_service_summary(base_path, services)
    create_services_summary_json(base_path, services)
    
    print(f"\n🎯 Organized GCP Service Prompts Complete!")
    print(f"✅ Created {len(created_folders)} service folders")
    print(f"✅ Created {len(created_folders) * 2} service files")
    print(f"✅ Created summary files")
    print(f"📁 Base directory: {base_dir}/")
    
    # Show some examples
    print(f"\n📝 Example folders created:")
    for i, folder in enumerate(created_folders[:5]):
        print(f"  {i+1}. {folder.name}/")
    if len(created_folders) > 5:
        print(f"  ... and {len(created_folders) - 5} more")

if __name__ == "__main__":
    main()
