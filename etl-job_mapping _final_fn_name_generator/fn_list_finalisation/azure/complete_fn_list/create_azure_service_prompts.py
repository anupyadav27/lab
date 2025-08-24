#!/usr/bin/env python3
"""
Azure Service Prompt File Generator

This script processes Azure compliance functions and creates individual prompt files
for each service category using the Azure prompt template.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any
from collections import defaultdict

def load_azure_template() -> str:
    """Load the Azure service prompt template"""
    template_file = "promt.md"
    
    if not Path(template_file).exists():
        print(f"Error: Azure template file {template_file} not found")
        return ""
    
    with open(template_file, 'r', encoding='utf-8') as f:
        return f.read()

def load_azure_data() -> List[Dict]:
    """Load the Azure functions data"""
    azure_file = "simplified_functions_updated_pci_secure_software_20250823_230607.json"
    
    if not Path(azure_file).exists():
        print(f"Error: Azure data file {azure_file} not found")
        return []
    
    with open(azure_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"Loaded Azure data with {len(data)} functions")
    return data

def group_functions_by_service(data: List[Dict]) -> Dict[str, List[Dict]]:
    """Group functions by service category"""
    print("Grouping functions by service category...")
    
    service_groups = defaultdict(list)
    
    for item in data:
        service_category = item.get('service_category', 'Unknown')
        if service_category == 'Unknown':
            # Try to extract service from function name
            func_name = item.get('function_name', '')
            if 'active_directory' in func_name or 'azuread' in func_name:
                service_category = 'Identity'
            elif 'storage' in func_name or 'blob' in func_name:
                service_category = 'Storage'
            elif 'network' in func_name or 'vnet' in func_name:
                service_category = 'Network'
            elif 'compute' in func_name or 'vm' in func_name:
                service_category = 'Compute'
            elif 'security' in func_name or 'keyvault' in func_name:
                service_category = 'Security'
            else:
                service_category = 'Other'
        
        service_groups[service_category].append(item)
    
    print(f"Grouped into {len(service_groups)} service categories")
    return dict(service_groups)

def create_azure_service_prompt_file(service_name: str, functions: List[Dict], template: str) -> str:
    """Create a prompt file for a specific Azure service"""
    
    # Replace template placeholders
    prompt_content = template.replace("[SERVICE_NAME_HERE]", service_name)
    prompt_content = prompt_content.replace("[NUMBER_OF_FUNCTIONS]", str(len(functions)))
    
    # Create the JSON input section with Azure-specific structure
    json_input = f'''```json
{{
  "services": {{
    "{service_name}": {{
      "check_functions": [
{chr(10).join([f'        "{func.get("function_name", "")}",' for func in functions])}
      ]
    }}
  }}
}}
```'''
    
    # Replace the input data section using regex for exact pattern matching
    import re
    
    # Pattern to match the placeholder section
    pattern = r'"check_functions":\s*\["function1",\s*"function2",\s*"function3"\]'
    
    # Build the replacement string
    replacement = '"check_functions": [\n'
    for func in functions:
        replacement += f'        "{func.get("function_name", "")}",\n'
    replacement += '      ]'
    
    # Replace with actual functions
    prompt_content = re.sub(pattern, replacement, prompt_content)
    
    return prompt_content

def create_service_directory() -> Path:
    """Create the service_prompts directory if it doesn't exist"""
    service_dir = Path("service_prompts")
    service_dir.mkdir(exist_ok=True)
    return service_dir

def generate_azure_service_prompts():
    """Main function to generate Azure service prompt files"""
    
    print("🚀 Azure Service Prompt File Generator")
    print("=" * 50)
    
    # Load Azure template
    print("📋 Loading Azure template...")
    template = load_azure_template()
    if not template:
        return
    
    # Load Azure data
    print("📊 Loading Azure data...")
    azure_data = load_azure_data()
    if not azure_data:
        return
    
    # Group functions by service
    service_groups = group_functions_by_service(azure_data)
    
    # Create service directory
    service_dir = create_service_directory()
    
    # Generate prompt files for each service category
    successful_services = 0
    failed_services = 0
    
    for service_name, functions in service_groups.items():
        try:
            print(f"📝 Processing {service_name} ({len(functions)} functions)...")
            
            # Create prompt content
            prompt_content = create_azure_service_prompt_file(service_name, functions, template)
            
            # Create filename (sanitize service name)
            safe_service_name = service_name.replace("/", "_").replace(" ", "_").replace("-", "_").replace("|", "_")
            filename = f"{safe_service_name}_service_prompt.md"
            filepath = service_dir / filename
            
            # Write prompt file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(prompt_content)
            
            print(f"✅ Created: {filename}")
            successful_services += 1
            
        except Exception as e:
            print(f"❌ Failed to process {service_name}: {e}")
            failed_services += 1
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 GENERATION SUMMARY")
    print(f"✅ Successful: {successful_services} services")
    print(f"❌ Failed: {failed_services} services")
    print(f"📁 Output directory: {service_dir.absolute()}")
    
    if successful_services > 0:
        print(f"\n🎯 Next steps:")
        print(f"1. Review the generated prompt files in: {service_dir}")
        print(f"2. Each file contains the Azure prompt + service functions")
        print(f"3. Use these files with AI tools for Azure compliance categorization")
        print(f"4. Files are ready for processing - no manual editing needed!")

def main():
    """Main entry point"""
    try:
        generate_azure_service_prompts()
    except KeyboardInterrupt:
        print("\n\n⏹️  Process interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
