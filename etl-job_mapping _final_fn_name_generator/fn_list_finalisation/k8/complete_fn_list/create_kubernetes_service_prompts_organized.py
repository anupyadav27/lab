#!/usr/bin/env python3
"""
Create Organized Kubernetes Service Prompts

This script creates service prompts organized by service folders:
kubernetes_service_prompts/
├── apiserver/
│   ├── apiserver_service_prompt.md
│   └── apiserver_functions.json
├── core/
│   ├── core_service_prompt.md
│   └── core_functions.json
└── ...
"""

import json
import os
from pathlib import Path

def create_service_folder_structure(base_dir):
    """Create the base directory structure"""
    
    print("📁 Creating Kubernetes service folder structure...")
    
    # Create base directory
    base_path = Path(base_dir)
    base_path.mkdir(exist_ok=True)
    print(f"✅ Created base directory: {base_dir}")
    
    return base_path

def generate_kubernetes_service_prompt_content(service_name, service_data):
    """Generate the content for a Kubernetes service prompt"""
    
    check_functions = service_data.get('check_functions', [])
    check_count = len(check_functions)
    
    # Create the prompt content
    prompt_content = f"""# Kubernetes {service_name.upper()} Service Compliance Prompt

## Service Information
- **Service Name**: {service_name.upper()}
- **Total Functions**: {check_count}
- **Service Type**: Kubernetes Component

## Function List
The following {check_count} functions are available for Kubernetes {service_name.upper()} compliance checks:

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
- **CIS Kubernetes Benchmark**
- **PCI Secure Software Standard v1.2.1**

## Usage Instructions
1. Use the function names above to create compliance checks
2. Each function should be implemented as a separate compliance rule
3. Follow the naming convention: `{service_name}_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Kubernetes API

## Example Implementation
```python
def {service_name}_example_function_check():
    \"\"\"
    Example compliance check for Kubernetes {service_name.upper()} service
    \"\"\"
    try:
        # Implementation using Kubernetes API
        # from kubernetes import client, config
        # config.load_kube_config()
        # v1 = client.CoreV1Api()
        
        # Check specific {service_name} configuration
        # result = v1.read_namespaced_config_map(...)
        
        pass
    except Exception as e:
        logger.error(f"Error in {service_name} check: {{e}}")
        return False
```

## Kubernetes API Integration
- **Service**: {service_name.upper()}
- **API Group**: Core API or Custom Resource Definitions
- **Authentication**: Service Account, kubeconfig, or token-based
- **Namespace**: Cluster-wide or namespace-specific

## Service-Specific Notes
"""
    
    # Add service-specific notes based on service name
    if service_name == "apiserver":
        prompt_content += """- **API Server**: Core Kubernetes API server component
- **Configuration**: Check API server flags and configuration files
- **Security**: TLS configuration, authentication, authorization
- **Audit**: Audit logging configuration and policies
- **Admission Control**: Admission controller plugins and policies
"""
    elif service_name == "core":
        prompt_content += """- **Core Components**: Essential Kubernetes core functionality
- **Pods**: Pod security policies and configurations
- **Namespaces**: Namespace isolation and security
- **Services**: Service networking and security
- **ConfigMaps/Secrets**: Configuration and secret management
"""
    elif service_name == "controllermanager":
        prompt_content += """- **Controller Manager**: Kubernetes controller components
- **Controllers**: Various controller configurations
- **Leader Election**: High availability configuration
- **Service Accounts**: Service account management
- **Node Management**: Node lifecycle management
"""
    elif service_name == "etcd":
        prompt_content += """- **etcd**: Kubernetes data store
- **TLS Configuration**: etcd TLS settings
- **Authentication**: etcd authentication mechanisms
- **Backup**: etcd backup and recovery procedures
- **Encryption**: etcd encryption at rest
"""
    elif service_name == "kubelet":
        prompt_content += """- **Kubelet**: Node agent component
- **Authentication**: Kubelet authentication configuration
- **Authorization**: Kubelet authorization settings
- **TLS**: Kubelet TLS configuration
- **Pod Security**: Pod security context enforcement
"""
    elif service_name == "rbac":
        prompt_content += """- **RBAC**: Role-Based Access Control
- **Roles**: Cluster and namespace roles
- **RoleBindings**: Role binding configurations
- **Service Accounts**: Service account permissions
- **Privilege Escalation**: Privilege escalation prevention
"""
    elif service_name == "scheduler":
        prompt_content += """- **Scheduler**: Kubernetes scheduler component
- **Scheduling Policies**: Pod scheduling policies
- **Resource Management**: Resource allocation and limits
- **Node Affinity**: Node affinity and anti-affinity rules
- **Pod Priority**: Pod priority and preemption
"""
    elif service_name == "kube-proxy":
        prompt_content += """- **Kube-proxy**: Network proxy component
- **Network Policies**: Network policy enforcement
- **Service Networking**: Service networking configuration
- **Load Balancing**: Load balancer configuration
- **Security**: Network security settings
"""
    elif service_name == "flanneld":
        prompt_content += """- **Flannel**: Container networking interface
- **Network Configuration**: CNI configuration
- **Security**: Network security policies
- **Performance**: Network performance optimization
- **Monitoring**: Network monitoring and logging
"""
    else:
        prompt_content += f"""- **{service_name.upper()}**: Kubernetes {service_name} component
- **Configuration**: {service_name} specific configurations
- **Security**: {service_name} security settings
- **Monitoring**: {service_name} monitoring and logging
- **Compliance**: {service_name} compliance requirements
"""
    
    prompt_content += f"""

## Implementation Guidelines
- All functions are based on Kubernetes {service_name.upper()} API
- Ensure proper RBAC permissions are configured
- Consider cluster-wide vs namespace-specific checks
- Implement appropriate retry logic for API calls
- Use Kubernetes client libraries for API interactions
- Follow Kubernetes security best practices
- Consider multi-cluster environments
"""
    
    return prompt_content

def create_kubernetes_service_folder_and_files(base_path, service_name, service_data):
    """Create folder and files for a specific Kubernetes service"""
    
    print(f"📝 Creating files for {service_name} service...")
    
    # Create service folder
    service_folder = base_path / service_name
    service_folder.mkdir(exist_ok=True)
    
    # Generate prompt content
    prompt_content = generate_kubernetes_service_prompt_content(service_name, service_data)
    
    # Create prompt file
    prompt_file = service_folder / f"{service_name}_service_prompt.md"
    with open(prompt_file, 'w', encoding='utf-8') as f:
        f.write(prompt_content)
    
    # Create functions JSON file
    functions_file = service_folder / f"{service_name}_functions.json"
    with open(functions_file, 'w', encoding='utf-8') as f:
        json.dump({
            'service_name': service_name,
            'check_count': len(service_data.get('check_functions', [])),
            'check_functions': service_data.get('check_functions', []),
            'service_type': 'kubernetes_component'
        }, f, indent=2, ensure_ascii=False)
    
    print(f"  ✅ Created {prompt_file}")
    print(f"  ✅ Created {functions_file}")
    
    return service_folder

def get_kubernetes_service_type(service_name):
    """Determine Kubernetes service type based on service name"""
    
    service_type_mapping = {
        # Core Components
        'apiserver': 'core_component',
        'core': 'core_component',
        'controllermanager': 'core_component',
        'scheduler': 'core_component',
        
        # Data Store
        'etcd': 'data_store',
        
        # Node Components
        'kubelet': 'node_component',
        'kube-proxy': 'node_component',
        
        # Security
        'rbac': 'security',
        
        # Networking
        'flanneld': 'networking',
        
        # Add more mappings as needed
    }
    
    return service_type_mapping.get(service_name, 'other')

def create_kubernetes_service_summary(base_path, services):
    """Create a summary file for all Kubernetes services"""
    
    print("📊 Creating Kubernetes service summary...")
    
    summary_content = """# Kubernetes Services Summary

This directory contains organized service prompts for Kubernetes compliance checks.

## Available Services

"""
    
    # Group services by type
    service_types = {}
    for service_name, service_data in services.items():
        service_type = get_kubernetes_service_type(service_name)
        
        if service_type not in service_types:
            service_types[service_type] = []
        
        service_types[service_type].append({
            'name': service_name,
            'check_count': len(service_data.get('check_functions', []))
        })
    
    # Add services by type
    for service_type, services_list in service_types.items():
        summary_content += f"### {service_type.upper().replace('_', ' ')} Services\n\n"
        
        for service in services_list:
            summary_content += f"- **{service['name']}** ({service['check_count']} functions)\n"
            summary_content += f"  - Folder: `{service['name']}/`\n\n"
    
    # Add total statistics
    total_services = len(services)
    total_functions = sum(len(service.get('check_functions', [])) for service in services.values())
    
    summary_content += f"""## Statistics
- **Total Services**: {total_services}
- **Total Functions**: {total_functions}
- **Service Types**: {len(service_types)}

## Directory Structure
```
kubernetes_service_prompts/
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
- **Core Component**: API Server, Controller Manager, Scheduler, Core
- **Data Store**: etcd
- **Node Component**: Kubelet, Kube-proxy
- **Security**: RBAC
- **Networking**: Flannel, CNI components
- **Other**: Miscellaneous components

## Kubernetes Compliance Standards
- **CIS Kubernetes Benchmark**
- **PCI Secure Software Standard v1.2.1**
- **NIST Cybersecurity Framework**
- **ISO 27001**
- **SOC 2**
- **GDPR**
- **HIPAA** (where applicable)
"""
    
    # Create summary file
    summary_file = base_path / "README.md"
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(summary_content)
    
    print(f"✅ Created {summary_file}")

def create_kubernetes_services_summary_json(base_path, services):
    """Create a JSON summary of all Kubernetes services"""
    
    print("📊 Creating Kubernetes services summary JSON...")
    
    summary_data = {
        'metadata': {
            'description': 'Kubernetes Services Summary for Compliance Checks',
            'total_services': len(services),
            'total_functions': sum(len(service.get('check_functions', [])) for service in services.values()),
            'organization': 'service_based_folders',
            'created_at': '2024-08-25',
            'compliance_frameworks': [
                'CIS Kubernetes Benchmark',
                'PCI Secure Software Standard v1.2.1',
                'NIST Cybersecurity Framework',
                'ISO 27001',
                'SOC 2',
                'GDPR',
                'HIPAA'
            ]
        },
        'services': {}
    }
    
    for service_name, service_data in services.items():
        service_type = get_kubernetes_service_type(service_name)
        
        summary_data['services'][service_name] = {
            'check_count': len(service_data.get('check_functions', [])),
            'service_type': service_type,
            'folder_path': f"{service_name}/",
            'files': [
                f"{service_name}_service_prompt.md",
                f"{service_name}_functions.json"
            ]
        }
    
    # Create summary JSON file
    summary_json_file = base_path / "kubernetes_services_summary.json"
    with open(summary_json_file, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Created {summary_json_file}")

def main():
    """Main function"""
    
    print("📁 Create Organized Kubernetes Service Prompts")
    print("=" * 60)
    
    # Load the Kubernetes service data
    try:
        with open('kubernetes_updated_pci_secure_software_20250824_021125.json', 'r') as f:
            k8s_data = json.load(f)
        print(f"✅ Loaded Kubernetes data: {len(k8s_data['services'])} services")
    except FileNotFoundError:
        print("❌ Kubernetes service data file not found")
        return
    
    services = k8s_data['services']
    
    # Create base directory structure
    base_dir = "kubernetes_service_prompts"
    base_path = create_service_folder_structure(base_dir)
    
    # Create folders and files for each service
    created_folders = []
    for service_name, service_data in services.items():
        service_folder = create_kubernetes_service_folder_and_files(base_path, service_name, service_data)
        created_folders.append(service_folder)
    
    # Create summary files
    create_kubernetes_service_summary(base_path, services)
    create_kubernetes_services_summary_json(base_path, services)
    
    print(f"\n🎯 Organized Kubernetes Service Prompts Complete!")
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
