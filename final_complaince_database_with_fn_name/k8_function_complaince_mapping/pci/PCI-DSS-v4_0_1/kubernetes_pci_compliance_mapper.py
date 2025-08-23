#!/usr/bin/env python3
"""
Kubernetes PCI DSS Compliance Function Mapping Tool using OpenAI

This tool maps existing security functions from kubernetes_updated_20250817_051156.json 
to PCI DSS compliance frameworks and suggests new functions where gaps exist.
"""

import json
import os
import sys
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from pathlib import Path
import logging
from datetime import datetime

# Check if openai is installed, if not prompt user to install
try:
    from openai import OpenAI
except ImportError:
    print("Error: openai library not found. Please install it with:")
    print("pip install openai")
    sys.exit(1)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('kubernetes_pci_compliance_mapping.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class PCIComplianceItem:
    """Represents a single PCI DSS compliance requirement"""
    RequirementID: str
    DefinedApproachRequirements: str
    Purpose: str
    GoodPractice: str
    Definitions: str
    Examples: str
    CustomizedApproachObjective: str
    ApplicabilityNotes: str
    FurtherInformation: str
    function_names: List[str]

@dataclass
class MappingResult:
    """Represents the result of mapping a compliance item to functions"""
    compliance_id: str
    title: str
    existing_functions_mapped: List[str]
    coverage_assessment: str  # complete|partial|none
    new_functions_needed: List[Dict[str, str]]
    mapping_notes: str

class KubernetesPCIComplianceMapper:
    """Main class for mapping PCI DSS compliance items to Kubernetes security functions"""
    
    def __init__(self, openai_api_key: str = None):
        """Initialize the compliance mapper"""
        
        # SET YOUR API KEY HERE:
        self.api_key = "YOUR_OPENAI_API_KEY_HERE"
        
        self.client = OpenAI(api_key=self.api_key)
        self.kubernetes_functions = {}
        self.all_function_names = set()
        
        # Create output directory
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)
        
    def load_kubernetes_database(self, kubernetes_file: str) -> bool:
        """Load the kubernetes function database"""
        try:
            with open(kubernetes_file, 'r') as f:
                data = json.load(f)
            
            self.kubernetes_functions = data.get('services', {})
            
            # Extract all function names for quick lookup
            for service_data in self.kubernetes_functions.values():
                for func_name in service_data.get('check_functions', []):
                    self.all_function_names.add(func_name)
            
            logger.info(f"Loaded {len(self.all_function_names)} functions from kubernetes database")
            return True
            
        except FileNotFoundError:
            logger.error(f"Kubernetes file not found: {kubernetes_file}")
            return False
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing kubernetes JSON: {e}")
            return False
    
    def load_pci_compliance_framework(self, compliance_file: str) -> List[PCIComplianceItem]:
        """Load the PCI DSS compliance framework from JSON file"""
        try:
            with open(compliance_file, 'r', encoding='utf-8') as f:
                compliance_data = json.load(f)
            
            compliance_items = []
            for item in compliance_data:
                # Extract function names if they exist
                function_names = []
                if 'function_names' in item and item['function_names']:
                    function_names = item['function_names']
                
                compliance_item = PCIComplianceItem(
                    RequirementID=item.get('RequirementID', ''),
                    DefinedApproachRequirements=item.get('DefinedApproachRequirements', ''),
                    Purpose=item.get('Purpose', ''),
                    GoodPractice=item.get('GoodPractice', ''),
                    Definitions=item.get('Definitions', ''),
                    Examples=item.get('Examples', ''),
                    CustomizedApproachObjective=item.get('CustomizedApproachObjective', ''),
                    ApplicabilityNotes=item.get('ApplicabilityNotes', ''),
                    FurtherInformation=item.get('FurtherInformation', ''),
                    function_names=function_names
                )
                compliance_items.append(compliance_item)
            
            logger.info(f"Loaded {len(compliance_items)} PCI DSS compliance items from {compliance_file}")
            return compliance_items
            
        except Exception as e:
            logger.error(f"Error loading PCI DSS compliance framework: {e}")
            return []
    
    def create_mapping_prompt(self, compliance_item: PCIComplianceItem, existing_functions: List[str]) -> str:
        """Create a prompt for mapping compliance item to functions"""
        
        prompt = f"""
Map the following PCI DSS compliance requirement to Kubernetes security functions.

PCI DSS Requirement ID: {compliance_item.RequirementID}
Defined Approach Requirements: {compliance_item.DefinedApproachRequirements}
Purpose: {compliance_item.Purpose}
Good Practice: {compliance_item.GoodPractice}
Definitions: {compliance_item.Definitions}
Examples: {compliance_item.Examples}
Customized Approach Objective: {compliance_item.CustomizedApproachObjective}
Applicability Notes: {compliance_item.ApplicabilityNotes}
Further Information: {compliance_item.FurtherInformation}

Available Kubernetes Functions ({len(existing_functions)} functions):
{', '.join(existing_functions[:50])}  # Showing first 50 for brevity

Instructions:
1. Analyze the PCI DSS requirement and identify which Kubernetes security functions could help implement or verify this control
2. ONLY suggest functions that can be implemented programmatically using Kubernetes APIs/kubectl commands
3. DO NOT suggest functions for policy, documentation, procedures, training, or manual processes
4. Focus on technical controls that can be checked via Kubernetes APIs
5. If no existing functions match, or existing function not able to cover full compliance, suggest new function names that follow Kubernetes service naming conventions
6. All function names must be in snake_case format
7. New functions must start with Kubernetes service prefixes (e.g., k8s_pod_, k8s_namespace_, k8s_service_, k8s_secret_, k8s_configmap_, k8s_rbac_)
8. DO NOT use generic terms like "nsc" - use specific Kubernetes service names

Return a JSON object with:
{{
    "existing_functions_mapped": ["list", "of", "existing", "function", "names"],
    "coverage_assessment": "complete|partial|none",
    "new_functions_needed": [
        {{
            "name": "k8s_service_specific_function_name",
            "k8s_api": "kubectl get/resource or kubernetes API call",
            "service": "k8s_service_name",
            "rationale": "Why this function is needed"
        }}
    ],
    "mapping_notes": "Explanation of the mapping and any gaps identified"
}}
"""
        return prompt
    
    def _validate_mapping_quality(self, suggested_functions: List[str]) -> bool:
        """Validate that suggested functions are appropriate for Kubernetes"""
        non_checkable_keywords = [
            'policy', 'documentation', 'procedure', 'training', 'manual', 
            'review', 'approval', 'process', 'nsc'
        ]
        
        k8s_service_prefixes = [
            'k8s_pod_', 'k8s_namespace_', 'k8s_service_', 'k8s_secret_', 
            'k8s_configmap_', 'k8s_rbac_', 'k8s_network_', 'k8s_storage_',
            'k8s_security_', 'k8s_monitoring_', 'k8s_audit_', 'k8s_compliance_'
        ]
        
        for func_name in suggested_functions:
            func_lower = func_name.lower()
            
            # Check for non-checkable keywords
            if any(keyword in func_lower for keyword in non_checkable_keywords):
                logger.warning(f"Invalid functions suggested: {suggested_functions}")
                return False
            
            # Check for Kubernetes service prefixes
            if not any(func_lower.startswith(prefix) for prefix in k8s_service_prefixes):
                logger.warning(f"Function {func_name} doesn't start with Kubernetes service prefix")
                return False
        
        return True
    
    def map_compliance_item(self, compliance_item: PCIComplianceItem, max_retries: int = 3) -> Optional[MappingResult]:
        """Map a single compliance item to functions using OpenAI"""
        
        # Get potential existing functions
        existing_functions = list(self.all_function_names)
        
        for attempt in range(max_retries):
            try:
                prompt = self.create_mapping_prompt(compliance_item, existing_functions)
                
                response = self.client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an expert in Kubernetes security and PCI DSS compliance mapping. You ONLY suggest functions that can be implemented programmatically using Kubernetes APIs/kubectl commands. You DO NOT suggest functions for policy, documentation, procedures, training, or manual processes. All function names must be in snake_case and start with Kubernetes service prefixes. DO NOT use generic terms like 'nsc' - use specific Kubernetes service names."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.3,
                    max_tokens=2000
                )
                
                content = response.choices[0].message.content.strip()
                
                # Extract JSON from response
                if '```json' in content:
                    content = content.split('```json')[1].split('```')[0]
                elif '```' in content:
                    content = content.split('```')[1]
                
                mapping_data = json.loads(content)
                
                # Validate mapping quality
                suggested_functions = mapping_data.get('new_functions_needed', [])
                suggested_names = [func.get('name', '') for func in suggested_functions]
                
                if not self._validate_mapping_quality(suggested_names):
                    logger.warning(f"Quality validation failed for {compliance_item.RequirementID}, attempt {attempt + 1}")
                    if attempt < max_retries - 1:
                        time.sleep(2)
                        continue
                    else:
                        logger.error(f"Failed to map PCI DSS requirement {compliance_item.RequirementID} after {max_retries} attempts")
                        return None
                
                return MappingResult(
                    compliance_id=compliance_item.RequirementID,
                    title=f"PCI DSS {compliance_item.RequirementID}",
                    existing_functions_mapped=mapping_data.get('existing_functions_mapped', []),
                    coverage_assessment=mapping_data.get('coverage_assessment', 'none'),
                    new_functions_needed=mapping_data.get('new_functions_needed', []),
                    mapping_notes=mapping_data.get('mapping_notes', '')
                )
                
            except Exception as e:
                logger.error(f"Error processing PCI DSS requirement {compliance_item.RequirementID}, attempt {attempt + 1}: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2)
                    continue
                else:
                    return None
        
        return None
    
    def process_pci_compliance_framework(self, compliance_items: List[PCIComplianceItem], test_mode: bool = False) -> Dict[str, Any]:
        """Process the entire PCI DSS compliance framework"""
        
        logger.info("Starting PCI DSS compliance framework processing...")
        
        if test_mode:
            compliance_items = compliance_items[:5]
            logger.info(f"TEST MODE: Processing only {len(compliance_items)} items")
        
        results = []
        new_functions_count = 0
        failed_items = []
        
        for i, item in enumerate(compliance_items):
            logger.info(f"Processing PCI DSS requirement {item.RequirementID} ({i+1}/{len(compliance_items)})")
            
            mapping_result = self.map_compliance_item(item)
            if mapping_result:
                results.append(mapping_result)
                new_functions_count += len(mapping_result.new_functions_needed)
                logger.info(f"Successfully mapped PCI DSS requirement: {item.RequirementID}")
            else:
                # Create a failed mapping result with "manual" function
                failed_result = MappingResult(
                    compliance_id=item.RequirementID,
                    title=f"PCI DSS {item.RequirementID}",
                    existing_functions_mapped=[],
                    coverage_assessment="manual",
                    new_functions_needed=[{"name": "manual", "description": "Requires manual review - not programmatically checkable"}],
                    mapping_notes="This requirement requires manual review and cannot be automated programmatically"
                )
                results.append(failed_result)
                failed_items.append(item.RequirementID)
                logger.warning(f"Failed to map PCI DSS requirement: {item.RequirementID} - marked as manual")
            
            # Rate limiting
            time.sleep(2)
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = self.output_dir / f"k8s_pci_mapping_results_{'test_' if test_mode else ''}{timestamp}.json"
        
        output_data = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "compliance_framework": "PCI DSS",
                "compliance_file": "PCI-DSS-v4_0_1 copy.json",
                "kubernetes_database_functions": len(self.all_function_names),
                "processing_stats": {
                    "total_items": len(compliance_items),
                    "processed": len(results),
                    "mapped_complete": len([r for r in results if r.coverage_assessment == "complete"]),
                    "mapped_partial": len([r for r in results if r.coverage_assessment == "partial"]),
                    "mapped_none": len([r for r in results if r.coverage_assessment == "none"]),
                    "manual_review_required": len([r for r in results if r.coverage_assessment == "manual"]),
                    "new_functions_suggested": new_functions_count,
                    "test_mode": test_mode
                }
            },
            "mapping_results": [
                {
                    "compliance_id": r.compliance_id,
                    "title": r.title,
                    "existing_functions_mapped": r.existing_functions_mapped,
                    "coverage_assessment": r.coverage_assessment,
                    "new_functions_needed": r.new_functions_needed,
                    "mapping_notes": r.mapping_notes
                }
                for r in results
            ]
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Results saved to {output_file}")
        
        # Update kubernetes functions with new functions (only non-manual ones)
        non_manual_results = [r for r in results if r.coverage_assessment != "manual"]
        if new_functions_count > 0:
            self._update_kubernetes_functions(non_manual_results)
        
        # Update PCI DSS file with generated functions
        self._update_pci_file_with_functions(results)
        
        return {
            "total_items": len(compliance_items),
            "processed": len(results),
            "mapped_complete": len([r for r in results if r.coverage_assessment == "complete"]),
            "mapped_partial": len([r for r in results if r.coverage_assessment == "partial"]),
            "mapped_none": len([r for r in results if r.coverage_assessment == "none"]),
            "manual_review_required": len([r for r in results if r.coverage_assessment == "manual"]),
            "new_functions_suggested": new_functions_count,
            "test_mode": test_mode
        }
    
    def _update_kubernetes_functions(self, results: List[MappingResult]):
        """Update kubernetes functions with new suggested functions"""
        new_functions = []
        
        for result in results:
            for new_func in result.new_functions_needed:
                new_function_data = {
                    "function_name": new_func["name"],
                    "k8s_api": new_func["k8s_api"],
                    "service": new_func["service"],
                    "rationale": new_func["rationale"],
                    "compliance_control": result.compliance_id,
                    "created_at": datetime.now().isoformat()
                }
                new_functions.append(new_function_data)
        
        if new_functions:
            # Load existing functions
            kubernetes_file = "kubernetes_updated_20250817_051156.json"
            try:
                with open(kubernetes_file, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
            except FileNotFoundError:
                existing_data = {"services": {}}
            
            # Add new functions to appropriate services
            for new_func in new_functions:
                service_name = new_func["service"]
                if service_name not in existing_data["services"]:
                    existing_data["services"][service_name] = {"check_functions": []}
                
                existing_data["services"][service_name]["check_functions"].append(new_func["function_name"])
            
            # Save updated file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            updated_file = self.output_dir / f"kubernetes_updated_pci_{timestamp}.json"
            
            with open(updated_file, 'w', encoding='utf-8') as f:
                json.dump(existing_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Updated kubernetes functions with {len(new_functions)} new functions")
            logger.info(f"Updated database saved to {updated_file}")
    
    def _update_pci_file_with_functions(self, results: List[MappingResult]):
        """Update PCI DSS file with generated functions from mapping results"""
        try:
            # Load the original PCI DSS file
            pci_file = "PCI-DSS-v4_0_1 copy.json"
            
            with open(pci_file, 'r', encoding='utf-8') as f:
                pci_data = json.load(f)
            
            # Create a mapping of requirement_id to functions
            requirement_functions_map = {}
            
            for result in results:
                requirement_id = result.compliance_id
                existing_functions = result.existing_functions_mapped
                new_functions = [func['name'] for func in result.new_functions_needed]
                
                # Combine existing and new functions
                all_functions = existing_functions + new_functions
                requirement_functions_map[requirement_id] = all_functions
            
            # Update the PCI DSS file
            updated_count = 0
            
            for requirement in pci_data:
                requirement_id = requirement.get('RequirementID')
                if requirement_id in requirement_functions_map:
                    # Update the function_names array
                    requirement['function_names'] = requirement_functions_map[requirement_id]
                    updated_count += 1
                    logger.info(f"Updated {requirement_id} with {len(requirement_functions_map[requirement_id])} functions")
            
            # Save the updated file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            updated_file = f"PCI-DSS-v4_0_1_updated_{timestamp}.json"
            
            with open(updated_file, 'w', encoding='utf-8') as f:
                json.dump(pci_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Updated {updated_count} PCI DSS requirements with functions")
            logger.info(f"Updated PCI DSS file saved as: {updated_file}")
            
            # Also save a backup of the original
            backup_file = f"PCI-DSS-v4_0_1_backup_{timestamp}.json"
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(pci_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Original PCI DSS file backed up as: {backup_file}")
            
        except Exception as e:
            logger.error(f"Error updating PCI DSS file: {e}")

def main():
    """Main function to run the Kubernetes PCI DSS compliance mapper"""
    
    print("\n=== Kubernetes PCI DSS Compliance Function Mapper ===")
    print("Kubernetes Database: kubernetes_updated_20250817_051156.json")
    print("PCI DSS Compliance Framework: PCI-DSS-v4_0_1 copy.json")
    print("Output Directory: output")
    
    # Initialize mapper
    mapper = KubernetesPCIComplianceMapper()
    
    # Load Kubernetes function database
    print("\nInitializing Kubernetes PCI DSS compliance mapper...")
    if not mapper.load_kubernetes_database("kubernetes_updated_20250817_051156.json"):
        print("❌ Failed to load Kubernetes function database")
        return
    
    # Load PCI DSS compliance framework
    compliance_items = mapper.load_pci_compliance_framework("PCI-DSS-v4_0_1 copy.json")
    if not compliance_items:
        print("❌ Failed to load PCI DSS compliance framework")
        return
    
    # Process compliance framework
    print("Starting PCI DSS compliance framework processing...")
    stats = mapper.process_pci_compliance_framework(compliance_items, test_mode=True)
    
    print("\n=== Processing Complete ===")
    print(f"Results saved to: output/")
    print("Processing statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")

if __name__ == "__main__":
    main()
