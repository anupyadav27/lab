#!/usr/bin/env python3
"""
PCI Secure Software Standard Compliance Function Mapping Tool using OpenAI

This tool maps existing security functions from prowler.json to PCI Secure Software Standard compliance framework
and suggests new functions where gaps exist.
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
        logging.FileHandler('pci_secure_software_mapping.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class PCISecureSoftwareRequirement:
    """Represents a single PCI Secure Software Standard requirement"""
    control_objective_id: str
    control_objective_description: str
    requirement_id: str
    requirement_description: str
    function_names: List[str] = None

@dataclass
class MappingResult:
    """Represents the result of mapping a compliance item to functions"""
    compliance_id: str
    title: str
    existing_functions_mapped: List[str]
    coverage_assessment: str  # complete|partial|none
    new_functions_needed: List[Dict[str, str]]
    mapping_notes: str

class PCISecureSoftwareMapper:
    """Main class for mapping PCI Secure Software Standard compliance items to security functions"""
    
    def __init__(self, openai_api_key: str = None):
        """Initialize the compliance mapper"""
        
        # SET YOUR API KEY HERE:
        self.api_key = "YOUR_OPENAI_API_KEY_HERE"
        
        self.client = OpenAI(api_key=self.api_key)
        self.prowler_functions = {}
        self.all_function_names = set()
        
    def load_prowler_database(self, prowler_file: str) -> bool:
        """Load the prowler function database"""
        try:
            with open(prowler_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.prowler_functions = data.get('services', {})
            
            # Extract all function names for quick lookup
            for service_data in self.prowler_functions.values():
                for func_name in service_data.get('check_functions', []):
                    self.all_function_names.add(func_name)
            
            logger.info(f"Loaded {len(self.all_function_names)} functions from prowler database")
            return True
            
        except FileNotFoundError:
            logger.error(f"Prowler file not found: {prowler_file}")
            return False
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing prowler JSON: {e}")
            return False
    
    def load_pci_secure_software_framework(self, compliance_file: str) -> List[PCISecureSoftwareRequirement]:
        """Load PCI Secure Software Standard compliance framework from JSON file"""
        try:
            with open(compliance_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            compliance_items = []
            control_objectives = data.get('control_objectives', [])
            
            for objective in control_objectives:
                objective_id = objective.get('id', '')
                objective_description = objective.get('description', '')
                requirements = objective.get('requirements', [])
                
                for requirement in requirements:
                    requirement_id = requirement.get('id', '')
                    requirement_description = requirement.get('description', '')
                    
                    compliance_item = PCISecureSoftwareRequirement(
                        control_objective_id=objective_id,
                        control_objective_description=objective_description,
                        requirement_id=requirement_id,
                        requirement_description=requirement_description,
                        function_names=requirement.get('function_names', [])
                    )
                    compliance_items.append(compliance_item)
            
            logger.info(f"Loaded {len(compliance_items)} PCI Secure Software Standard requirements")
            return compliance_items
            
        except FileNotFoundError:
            logger.error(f"Compliance file not found: {compliance_file}")
            return []
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing compliance JSON: {e}")
            return []
    
    def create_mapping_prompt(self, compliance_item: PCISecureSoftwareRequirement, batch_context: str = "") -> str:
        """Create the AI prompt for mapping a PCI Secure Software Standard requirement"""
        
        # Get available function names as context - limit to avoid token overflow
        available_functions = list(self.all_function_names)
        # Limit function list to stay within token limits
        functions_text = "\n".join([f"- {func}" for func in sorted(available_functions)[:300]])
        
        prompt = f"""
You are a cloud security expert working with a CSMP tool. You have access to an existing function database with {len(self.all_function_names)} AWS security check functions in snake_case format.

## Task:
Map the following PCI Secure Software Standard requirement to existing functions and suggest new ones where gaps exist.

## PCI Secure Software Standard Requirement:
- **Control Objective ID**: {compliance_item.control_objective_id}
- **Control Objective Description**: {compliance_item.control_objective_description}
- **Requirement ID**: {compliance_item.requirement_id}
- **Requirement Description**: {compliance_item.requirement_description}

## Available Functions Database ({len(self.all_function_names)} functions):
{functions_text}

## Instructions:
1. **Search for Matches**: Find existing functions that could satisfy this PCI Secure Software Standard requirement (semantic matching, not just exact names)
   - ONLY map functions that genuinely relate to the compliance requirement
   - Be conservative - prefer unmapped over incorrectly mapped
2. **Assess Coverage**: Determine if existing functions provide complete, partial, or no coverage
   - "complete" = all requirements covered by existing functions
   - "partial" = some requirements covered, gaps remain
   - "none" = no existing functions address this requirement
3. **Suggest New Functions**: If gaps exist, suggest ONLY functions that can be implemented programmatically
   - Functions MUST be checkable via boto3 APIs (describe_*, get_*, list_*, etc.)
   - Functions MUST check actual AWS resource configurations, not policies or documentation
   - Functions MUST start with AWS service prefixes (ec2_, s3_, iam_, vpc_, rds_, lambda_, cloudfront_, waf_, etc.)
   - Examples of checkable functions: s3_bucket_encryption_enabled, iam_user_mfa_enabled, ec2_instance_public_ip_disabled, vpc_network_acl_restrict_public_access, cloudfront_distribution_https_enabled
   - Examples of NON-checkable (DO NOT SUGGEST): policy_documentation_check, procedure_implementation_check, training_completion_check, nsc_configuration_check
4. **Quality Requirements**:
   - Function names MUST be in snake_case format
   - Functions MUST start with valid AWS service prefixes (ec2_, s3_, iam_, vpc_, rds_, lambda_, cloudfront_, waf_, apigateway_, route53_, cloudtrail_, cloudwatch_, kms_, etc.)
   - Functions MUST be implementable with real boto3 APIs (describe_*, get_*, list_*)
   - Service field MUST match AWS service names (ec2, s3, iam, etc.)
   - ONLY suggest functions that check actual AWS resource configurations
   - DO NOT suggest functions for policy documentation, procedures, training, manual processes, or generic terms like "nsc"

## Output Format (JSON only):
{{
  "compliance_id": "{compliance_item.requirement_id}",
  "title": "PCI Secure Software {compliance_item.requirement_id}",
  "existing_functions_mapped": ["function1", "function2"],
  "coverage_assessment": "complete|partial|none",
  "new_functions_needed": [
    {{
      "name": "new_function_name",
      "boto3_api": "ec2.describe_images()",
      "service": "ec2",
      "rationale": "Why this function is needed"
    }}
  ],
  "mapping_notes": "Brief explanation of mapping decisions"
}}

{batch_context}

Return ONLY the JSON response, no other text.
"""
        return prompt
    
    def map_compliance_item(self, compliance_item: PCISecureSoftwareRequirement, max_retries: int = 3) -> Optional[MappingResult]:
        """Map a single compliance item using OpenAI with retry logic for quality"""
        
        for attempt in range(max_retries):
            try:
                prompt = self.create_mapping_prompt(compliance_item)
                
                # Add rate limiting to prevent 429 errors
                time.sleep(2)  # 2 second delay between requests
                
                response = self.client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are a cloud security expert specializing in AWS compliance and PCI Secure Software Standard security controls. You ONLY suggest functions that can be implemented programmatically using boto3 APIs to check actual AWS resource configurations. Functions MUST start with AWS service prefixes (ec2_, s3_, iam_, vpc_, rds_, lambda_, cloudfront_, waf_, etc.). Do NOT suggest functions for policy documentation, procedures, training, manual processes, or generic terms like 'nsc'. Always respond with valid JSON only. Be conservative and accurate in your mappings."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.0,  # Minimum temperature for maximum consistency
                    max_tokens=1500,  # Reduced tokens to avoid context length issues
                    top_p=0.1,       # Very focused responses
                    frequency_penalty=0,
                    presence_penalty=0
                )
            
                response_text = response.choices[0].message.content.strip()
                
                # Parse JSON response
                try:
                    result_data = json.loads(response_text)
                    
                    # Validate required fields
                    required_fields = ['compliance_id', 'title', 'existing_functions_mapped', 
                                     'coverage_assessment', 'new_functions_needed', 'mapping_notes']
                    
                    for field in required_fields:
                        if field not in result_data:
                            logger.warning(f"Missing required field '{field}' in response for {compliance_item.requirement_id}, attempt {attempt + 1}")
                            break
                    else:
                        # Validate data quality
                        if self._validate_mapping_quality(result_data, compliance_item):
                            # Create MappingResult
                            mapping_result = MappingResult(
                                compliance_id=result_data['compliance_id'],
                                title=result_data['title'],
                                existing_functions_mapped=result_data['existing_functions_mapped'],
                                coverage_assessment=result_data['coverage_assessment'],
                                new_functions_needed=result_data['new_functions_needed'],
                                mapping_notes=result_data['mapping_notes']
                            )
                            
                            logger.info(f"Successfully mapped PCI Secure Software requirement: {compliance_item.requirement_id}")
                            return mapping_result
                        else:
                            logger.warning(f"Quality validation failed for {compliance_item.requirement_id}, attempt {attempt + 1}")
                            continue
                    
                except json.JSONDecodeError as e:
                    logger.warning(f"Failed to parse JSON response for {compliance_item.requirement_id}, attempt {attempt + 1}: {e}")
                    if attempt == max_retries - 1:
                        logger.error(f"Response was: {response_text}")
                    continue
                    
            except Exception as e:
                logger.warning(f"Error processing PCI Secure Software requirement {compliance_item.requirement_id}, attempt {attempt + 1}: {e}")
                if attempt == max_retries - 1:
                    logger.error(f"Final attempt failed for {compliance_item.requirement_id}")
                continue
        
        logger.error(f"Failed to map PCI Secure Software requirement {compliance_item.requirement_id} after {max_retries} attempts")
        return None
    
    def _validate_mapping_quality(self, result_data: Dict[str, Any], compliance_item: PCISecureSoftwareRequirement) -> bool:
        """Validate the quality of the mapping result"""
        
        # Check if mapped functions actually exist in our database
        mapped_functions = result_data.get('existing_functions_mapped', [])
        invalid_functions = [f for f in mapped_functions if f not in self.all_function_names]
        
        if invalid_functions:
            logger.warning(f"Invalid functions suggested: {invalid_functions}")
            return False
        
        # Validate coverage assessment values
        valid_coverage = ['complete', 'partial', 'none']
        if result_data.get('coverage_assessment') not in valid_coverage:
            logger.warning(f"Invalid coverage assessment: {result_data.get('coverage_assessment')}")
            return False
        
        # Check new functions format
        new_functions = result_data.get('new_functions_needed', [])
        for func in new_functions:
            if not isinstance(func, dict):
                return False
            required_func_fields = ['name', 'boto3_api', 'service', 'rationale']
            if not all(field in func for field in required_func_fields):
                logger.warning(f"New function missing required fields: {func}")
                return False
            
            # Validate function name format (snake_case)
            func_name = func.get('name', '')
            if not func_name.islower() or not all(c.isalnum() or c == '_' for c in func_name):
                logger.warning(f"Invalid function name format: {func_name}")
                return False
            
            # Validate that function is actually checkable (not policy/documentation) and uses AWS service names
            non_checkable_keywords = ['policy', 'documentation', 'procedure', 'training', 'manual', 'review', 'approval', 'process', 'nsc']
            aws_service_prefixes = ['ec2_', 's3_', 'iam_', 'vpc_', 'rds_', 'lambda_', 'cloudfront_', 'waf_', 'apigateway_', 'route53_', 'cloudtrail_', 'cloudwatch_', 'kms_', 'secretsmanager_', 'dynamodb_', 'sns_', 'sqs_', 'elb_', 'autoscaling_', 'backup_', 'config_', 'guardduty_', 'inspector_', 'macie_', 'securityhub_', 'shield_', 'cognito_', 'sts_', 'organizations_', 'budget_', 'costexplorer_', 'billing_', 'account_', 'acm_', 'appstream_', 'appsync_', 'athena_', 'autoscaling_', 'bedrock_', 'cloudformation_', 'codeartifact_', 'codebuild_', 'datasync_', 'directconnect_', 'directoryservice_', 'dlm_', 'dms_', 'documentdb_', 'ebs_', 'ecr_', 'ecs_', 'efs_', 'eks_', 'elasticache_', 'elasticbeanstalk_', 'elasticsearch_', 'emr_', 'fsx_', 'glacier_', 'glue_', 'kinesis_', 'lightsail_', 'mq_', 'neptune_', 'opensearch_', 'redshift_', 'sagemaker_', 'servicediscovery_', 'ses_', 'sso_', 'transfer_', 'workspaces_']
            
            func_name_lower = func_name.lower()
            
            # Check for non-checkable keywords
            if any(keyword in func_name_lower for keyword in non_checkable_keywords):
                logger.warning(f"Function appears to be non-checkable (policy/documentation): {func_name}")
                return False
            
            # Check for AWS service prefix
            if not any(func_name_lower.startswith(prefix) for prefix in aws_service_prefixes):
                logger.warning(f"Function does not use AWS service prefix: {func_name}")
                return False
        
        return True
    
    def process_pci_secure_software_framework(self, compliance_file: str, output_dir: str, batch_size: int = 5, test_mode: bool = False, test_items: int = 5) -> Dict[str, Any]:
        """Process PCI Secure Software Standard compliance framework in batches"""
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        compliance_items = self.load_pci_secure_software_framework(compliance_file)
        if not compliance_items:
            return {"error": "Failed to load PCI Secure Software Standard compliance framework"}
        
        # Limit items for test mode
        if test_mode:
            compliance_items = compliance_items[:test_items]
            logger.info(f"TEST MODE: Processing only {len(compliance_items)} items")
        
        results = []
        new_functions_to_add = []
        processing_stats = {
            "total_items": len(compliance_items),
            "processed": 0,
            "mapped_complete": 0,
            "mapped_partial": 0,
            "mapped_none": 0,
            "new_functions_suggested": 0,
            "test_mode": test_mode
        }
        
        # Process in batches
        for i in range(0, len(compliance_items), batch_size):
            batch = compliance_items[i:i + batch_size]
            logger.info(f"Processing batch {i//batch_size + 1}/{(len(compliance_items)-1)//batch_size + 1}")
            
            for item in batch:
                result = self.map_compliance_item(item)
                
                if result is None:
                    continue
                
                results.append(result)
                processing_stats["processed"] += 1
                
                # Update statistics
                if result.coverage_assessment == "complete":
                    processing_stats["mapped_complete"] += 1
                elif result.coverage_assessment == "partial":
                    processing_stats["mapped_partial"] += 1
                else:
                    processing_stats["mapped_none"] += 1
                
                # Collect new functions
                if result.new_functions_needed:
                    new_functions_to_add.extend(result.new_functions_needed)
                    processing_stats["new_functions_suggested"] += len(result.new_functions_needed)
        
        # Save results
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        mode_suffix = "_test" if test_mode else ""
        output_file = os.path.join(output_dir, f"pci_secure_software_mapping_results{mode_suffix}_{timestamp}.json")
        
        output_data = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "compliance_framework": "PCI Secure Software Standard",
                "compliance_file": compliance_file,
                "prowler_database_functions": len(self.all_function_names),
                "processing_stats": processing_stats
            },
            "mapping_results": [self._mapping_result_to_dict(r) for r in results],
            "new_functions_suggested": new_functions_to_add
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Results saved to {output_file}")
        logger.info(f"Processing complete: {processing_stats}")
        
        return output_data
    
    def _mapping_result_to_dict(self, result: MappingResult) -> Dict[str, Any]:
        """Convert MappingResult to dictionary"""
        return {
            "compliance_id": result.compliance_id,
            "title": result.title,
            "existing_functions_mapped": result.existing_functions_mapped,
            "coverage_assessment": result.coverage_assessment,
            "new_functions_needed": result.new_functions_needed,
            "mapping_notes": result.mapping_notes
        }
    
    def update_prowler_database(self, new_functions: List[Dict[str, str]], output_dir: str):
        """Update prowler database with new suggested functions"""
        
        # Group new functions by service
        functions_by_service = {}
        for func in new_functions:
            service = func.get('service', 'unknown')
            if service not in functions_by_service:
                functions_by_service[service] = []
            functions_by_service[service].append(func['name'])
        
        # Load current prowler data
        current_data = {}
        prowler_file = "prowler_updated_nist_20250822_145118.json"
        
        if os.path.exists(prowler_file):
            with open(prowler_file, 'r', encoding='utf-8') as f:
                current_data = json.load(f)
        else:
            logger.error(f"Prowler file not found: {prowler_file}")
            return
        
        # Add new functions to services
        services = current_data.get('services', {})
        total_added = 0
        
        for service, func_list in functions_by_service.items():
            if service not in services:
                services[service] = {
                    "service_name": service,
                    "check_functions": [],
                    "check_count": 0
                }
            
            # Add unique functions only
            existing_funcs = set(services[service]['check_functions'])
            new_unique_funcs = [f for f in func_list if f not in existing_funcs]
            
            services[service]['check_functions'].extend(new_unique_funcs)
            services[service]['check_count'] = len(services[service]['check_functions'])
            total_added += len(new_unique_funcs)
        
        # Update metadata
        current_data['services'] = services
        if 'scan_metadata' in current_data:
            current_data['scan_metadata']['total_check_functions'] = sum(
                s['check_count'] for s in services.values()
            )
            current_data['scan_metadata']['total_services'] = len(services)
            current_data['scan_metadata']['last_updated'] = datetime.now().isoformat()
        
        # Save updated database to output directory
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        updated_prowler_file = os.path.join(output_dir, f"prowler_updated_pci_secure_software_{timestamp}.json")
        
        with open(updated_prowler_file, 'w', encoding='utf-8') as f:
            json.dump(current_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Updated prowler database with {total_added} new functions")
        logger.info(f"Updated database saved to {updated_prowler_file}")


def main():
    """Main function to run the PCI Secure Software Standard compliance mapper"""
    
    # Configuration
    PROWLER_FILE = "prowler_updated_nist_20250822_145118.json"
    PCI_SECURE_SOFTWARE_FILE = "PCI-Secure-Software-Standard-v1_2_1.json"
    OUTPUT_DIR = "output"
    
    print("=== PCI Secure Software Standard Compliance Function Mapper ===")
    print(f"Prowler Database: {PROWLER_FILE}")
    print(f"PCI Secure Software Standard: {PCI_SECURE_SOFTWARE_FILE}")
    print(f"Output Directory: {OUTPUT_DIR}")
    print()
    
    # Check if files exist
    if not os.path.exists(PROWLER_FILE):
        print(f"Error: {PROWLER_FILE} not found in current directory")
        return
    
    if not os.path.exists(PCI_SECURE_SOFTWARE_FILE):
        print(f"Error: {PCI_SECURE_SOFTWARE_FILE} not found in current directory")
        return
    
    # API key will be handled by the PCISecureSoftwareMapper class
    print("Initializing PCI Secure Software Standard compliance mapper...")
    
    try:
        # Initialize mapper
        mapper = PCISecureSoftwareMapper()
        
        # Load prowler database
        if not mapper.load_prowler_database(PROWLER_FILE):
            print("Failed to load prowler database")
            return
        
        print(f"Loaded {len(mapper.all_function_names)} functions from prowler database")
        
        # Process PCI Secure Software Standard compliance framework
        print("Starting PCI Secure Software Standard compliance framework processing...")
        # Test mode: process only 5 items for testing
        results = mapper.process_pci_secure_software_framework(PCI_SECURE_SOFTWARE_FILE, OUTPUT_DIR, test_mode=True, test_items=5)
        
        if "error" in results:
            print(f"Error: {results['error']}")
            return
        
        # Update prowler database with new functions
        if results.get('new_functions_suggested'):
            print(f"Updating prowler database with {len(results['new_functions_suggested'])} new functions...")
            mapper.update_prowler_database(results['new_functions_suggested'], OUTPUT_DIR)
        
        print("\n=== Processing Complete ===")
        print(f"Results saved to: {OUTPUT_DIR}/")
        print(f"Processing statistics:")
        stats = results['metadata']['processing_stats']
        for key, value in stats.items():
            print(f"  {key}: {value}")
            
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
