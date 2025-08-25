#!/usr/bin/env python3
"""
Create Organized Azure Service Prompts

This script creates service prompts organized by service folders:
azure_service_prompts/
├── active_directory/
│   ├── active_directory_service_prompt.md
│   └── active_directory_functions.json
├── identity/
│   ├── identity_service_prompt.md
│   └── identity_functions.json
└── ...
"""

import json
import os
from pathlib import Path

def create_service_folder_structure(base_dir):
    """Create the base directory structure"""
    
    print("📁 Creating Azure service folder structure...")
    
    # Create base directory
    base_path = Path(base_dir)
    base_path.mkdir(exist_ok=True)
    print(f"✅ Created base directory: {base_dir}")
    
    return base_path

def generate_azure_service_prompt_content(service_name, service_data):
    """Generate the content for an Azure service prompt"""
    
    display_name = service_data.get('display_name', f'Azure {service_name.upper()} Service')
    check_functions = service_data.get('check_functions', [])
    check_count = service_data.get('check_count', len(check_functions))
    original_categories = service_data.get('original_categories', [])
    categorization_methods = service_data.get('categorization_methods', [])
    
    # Create the prompt content
    prompt_content = f"""# Azure {display_name} Service Compliance Prompt

## Service Information
- **Service Name**: {service_name.upper()}
- **Display Name**: {display_name}
- **Total Functions**: {check_count}
- **Original Categories**: {', '.join(original_categories) if original_categories else 'N/A'}
- **Categorization Methods**: {', '.join(categorization_methods) if categorization_methods else 'N/A'}

## Function List
The following {check_count} functions are available for {display_name} compliance checks:

"""
    
    # Add functions in a numbered list
    for i, func in enumerate(check_functions, 1):
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
- **Azure Security Benchmark**

## Usage Instructions
1. Use the function names above to create compliance checks
2. Each function should be implemented as a separate compliance rule
3. Follow the naming convention: `{service_name}_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def {service_name}_example_function_check():
    \"\"\"
    Example compliance check for {display_name} service
    \"\"\"
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.{service_name} import {service_name.title()}ManagementClient
        
        # credential = DefaultAzureCredential()
        # client = {service_name.title()}ManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in {service_name} check: {{e}}")
        return False
```

## Azure SDK Integration
- **Service**: {display_name}
- **SDK Namespace**: azure.mgmt.{service_name}
- **Client Class**: {service_name.title()}ManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure {display_name} API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
"""
    
    return prompt_content

def create_azure_service_folder_and_files(base_path, service_name, service_data):
    """Create folder and files for a specific Azure service"""
    
    print(f"📝 Creating files for {service_name} service...")
    
    # Create service folder
    service_folder = base_path / service_name
    service_folder.mkdir(exist_ok=True)
    
    # Generate prompt content
    prompt_content = generate_azure_service_prompt_content(service_name, service_data)
    
    # Create prompt file
    prompt_file = service_folder / f"{service_name}_service_prompt.md"
    with open(prompt_file, 'w', encoding='utf-8') as f:
        f.write(prompt_content)
    
    # Create functions JSON file
    functions_file = service_folder / f"{service_name}_functions.json"
    with open(functions_file, 'w', encoding='utf-8') as f:
        json.dump({
            'service_name': service_name,
            'display_name': service_data.get('display_name', f'Azure {service_name.upper()} Service'),
            'check_count': service_data.get('check_count', 0),
            'check_functions': service_data.get('check_functions', []),
            'original_categories': service_data.get('original_categories', []),
            'categorization_methods': service_data.get('categorization_methods', []),
            'original_name': service_data.get('original_name', service_name)
        }, f, indent=2, ensure_ascii=False)
    
    print(f"  ✅ Created {prompt_file}")
    print(f"  ✅ Created {functions_file}")
    
    return service_folder

def get_azure_service_type(service_name, original_categories):
    """Determine Azure service type based on service name and categories"""
    
    # Map service names to types
    service_type_mapping = {
        # Identity and Access Management
        'active_directory': 'identity',
        'identity': 'identity',
        'rbac': 'identity',
        'authorization': 'identity',
        
        # Compute
        'compute': 'compute',
        'virtual_machines': 'compute',
        'container_instances': 'compute',
        'aks': 'compute',
        'functions': 'compute',
        'functionapp': 'compute',
        'app_service': 'compute',
        'cloud_services': 'compute',
        
        # Storage
        'storage': 'storage',
        'blob': 'storage',
        'file': 'storage',
        'queue': 'storage',
        'table': 'storage',
        
        # Networking
        'network': 'networking',
        'vnet': 'networking',
        'load_balancer': 'networking',
        'application_gateway': 'networking',
        'firewall': 'networking',
        'dns': 'networking',
        
        # Security
        'security': 'security',
        'securitycenter': 'security',
        'defender': 'security',
        'keyvault': 'security',
        'sentinel': 'security',
        
        # Database
        'sql': 'database',
        'cosmos': 'database',
        'redis': 'database',
        'postgresql': 'database',
        'mysql': 'database',
        
        # Monitoring
        'monitoring': 'monitoring',
        'log_analytics': 'monitoring',
        'application_insights': 'monitoring',
        'event_hubs': 'monitoring',
        'eventgrid': 'monitoring',
        
        # Management
        'management': 'management',
        'resource_manager': 'management',
        'policy': 'management',
        'subscription': 'management',
        
        # AI/ML
        'machine_learning': 'ai_ml',
        'cognitive_services': 'ai_ml',
        'openai': 'ai_ml',
        
        # Data
        'data_factory': 'data',
        'synapse': 'data',
        'purview': 'data',
        'backup': 'data',
        'recovery_services': 'data'
    }
    
    # Check service name mapping first
    if service_name in service_type_mapping:
        return service_type_mapping[service_name]
    
    # Check original categories
    if original_categories:
        category_lower = original_categories[0].lower()
        if 'identity' in category_lower or 'access' in category_lower:
            return 'identity'
        elif 'compute' in category_lower or 'virtual' in category_lower:
            return 'compute'
        elif 'storage' in category_lower:
            return 'storage'
        elif 'network' in category_lower:
            return 'networking'
        elif 'security' in category_lower:
            return 'security'
        elif 'database' in category_lower or 'sql' in category_lower:
            return 'database'
        elif 'monitor' in category_lower or 'log' in category_lower:
            return 'monitoring'
        elif 'management' in category_lower or 'resource' in category_lower:
            return 'management'
        elif 'ai' in category_lower or 'ml' in category_lower or 'cognitive' in category_lower:
            return 'ai_ml'
        elif 'data' in category_lower or 'analytics' in category_lower:
            return 'data'
    
    return 'other'

def create_azure_service_summary(base_path, services):
    """Create a summary file for all Azure services"""
    
    print("📊 Creating Azure service summary...")
    
    summary_content = """# Azure Services Summary

This directory contains organized service prompts for Azure compliance checks.

## Available Services

"""
    
    # Group services by type
    service_types = {}
    for service_name, service_data in services.items():
        original_categories = service_data.get('original_categories', [])
        service_type = get_azure_service_type(service_name, original_categories)
        
        if service_type not in service_types:
            service_types[service_type] = []
        
        service_types[service_type].append({
            'name': service_name,
            'display_name': service_data.get('display_name', f'Azure {service_name.upper()} Service'),
            'check_count': service_data.get('check_count', 0),
            'original_categories': original_categories
        })
    
    # Add services by type
    for service_type, services_list in service_types.items():
        summary_content += f"### {service_type.upper().replace('_', ' ')} Services\n\n"
        
        for service in services_list:
            summary_content += f"- **{service['name']}** ({service['check_count']} functions)\n"
            summary_content += f"  - Display Name: {service['display_name']}\n"
            summary_content += f"  - Categories: {', '.join(service['original_categories']) if service['original_categories'] else 'N/A'}\n"
            summary_content += f"  - Folder: `{service['name']}/`\n\n"
    
    # Add total statistics
    total_services = len(services)
    total_functions = sum(service.get('check_count', 0) for service in services.values())
    
    summary_content += f"""## Statistics
- **Total Services**: {total_services}
- **Total Functions**: {total_functions}
- **Service Types**: {len(service_types)}

## Directory Structure
```
azure_service_prompts/
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
- **Identity**: Active Directory, Identity Management, RBAC
- **Compute**: Virtual Machines, Containers, Functions, App Service
- **Storage**: Blob Storage, File Storage, Queue Storage
- **Networking**: Virtual Network, Load Balancer, Firewall, DNS
- **Security**: Security Center, Key Vault, Sentinel, Defender
- **Database**: SQL Database, Cosmos DB, Redis Cache
- **Monitoring**: Log Analytics, Application Insights, Event Hubs
- **Management**: Resource Manager, Policy, Subscriptions
- **AI/ML**: Machine Learning, Cognitive Services, OpenAI
- **Data**: Data Factory, Synapse, Purview, Backup
- **Other**: Miscellaneous services
"""
    
    # Create summary file
    summary_file = base_path / "README.md"
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(summary_content)
    
    print(f"✅ Created {summary_file}")

def create_azure_services_summary_json(base_path, services):
    """Create a JSON summary of all Azure services"""
    
    print("📊 Creating Azure services summary JSON...")
    
    summary_data = {
        'metadata': {
            'description': 'Azure Services Summary for Compliance Checks',
            'total_services': len(services),
            'total_functions': sum(service.get('check_count', 0) for service in services.values()),
            'organization': 'service_based_folders',
            'created_at': '2024-08-25'
        },
        'services': {}
    }
    
    for service_name, service_data in services.items():
        original_categories = service_data.get('original_categories', [])
        service_type = get_azure_service_type(service_name, original_categories)
        
        summary_data['services'][service_name] = {
            'display_name': service_data.get('display_name', f'Azure {service_name.upper()} Service'),
            'check_count': service_data.get('check_count', 0),
            'original_categories': original_categories,
            'categorization_methods': service_data.get('categorization_methods', []),
            'service_type': service_type,
            'folder_path': f"{service_name}/",
            'files': [
                f"{service_name}_service_prompt.md",
                f"{service_name}_functions.json"
            ]
        }
    
    # Create summary JSON file
    summary_json_file = base_path / "azure_services_summary.json"
    with open(summary_json_file, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Created {summary_json_file}")

def main():
    """Main function"""
    
    print("📁 Create Organized Azure Service Prompts")
    print("=" * 60)
    
    # Load the Azure service data
    try:
        with open('azure_final_100_percent_coverage_complete.json', 'r') as f:
            azure_data = json.load(f)
        print(f"✅ Loaded Azure data: {len(azure_data['services'])} services")
    except FileNotFoundError:
        print("❌ Azure service data file not found")
        return
    
    services = azure_data['services']
    
    # Create base directory structure
    base_dir = "azure_service_prompts_organized"
    base_path = create_service_folder_structure(base_dir)
    
    # Create folders and files for each service
    created_folders = []
    for service_name, service_data in services.items():
        service_folder = create_azure_service_folder_and_files(base_path, service_name, service_data)
        created_folders.append(service_folder)
    
    # Create summary files
    create_azure_service_summary(base_path, services)
    create_azure_services_summary_json(base_path, services)
    
    print(f"\n🎯 Organized Azure Service Prompts Complete!")
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
