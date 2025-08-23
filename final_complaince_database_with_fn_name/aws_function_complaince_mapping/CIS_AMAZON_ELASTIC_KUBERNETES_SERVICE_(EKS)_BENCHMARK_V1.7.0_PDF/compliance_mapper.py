#!/usr/bin/env python3
"""
Compliance Function Mapping Tool using OpenAI

This tool maps existing security functions from prowler.json to compliance frameworks
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
        logging.FileHandler('compliance_mapping.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class ComplianceItem:
    """Represents a single compliance requirement"""
    id: str
    title: str
    assessment: str
    description: str
    function_names: List[str]
    rationale: Optional[str] = None
    audit: Optional[str] = None
    remediation: Optional[str] = None

@dataclass
class MappingResult:
    """Represents the result of mapping a compliance item to functions"""
    compliance_id: str
    title: str
    existing_functions_mapped: List[str]
    coverage_assessment: str  # complete|partial|none
    new_functions_needed: List[Dict[str, str]]
    mapping_notes: str

class ComplianceMapper:
    """Main class for mapping compliance items to security functions"""
    
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
            with open(prowler_file, 'r') as f:
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
    
    def load_compliance_framework(self, compliance_file: str) -> List[ComplianceItem]:
        """Load compliance framework from JSON file"""
        try:
            with open(compliance_file, 'r') as f:
                data = json.load(f)
            
            compliance_items = []
            for item in data:
                compliance_item = ComplianceItem(
                    id=item.get('id', ''),
                    title=item.get('title', ''),
                    assessment=item.get('assessment', ''),
                    description=item.get('description', ''),
                    function_names=item.get('function_names', []),
                    rationale=item.get('rationale'),
                    audit=item.get('audit'),
                    remediation=item.get('remediation')
                )
                compliance_items.append(compliance_item)
            
            logger.info(f"Loaded {len(compliance_items)} compliance items")
            return compliance_items
            
        except FileNotFoundError:
            logger.error(f"Compliance file not found: {compliance_file}")
            return []
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing compliance JSON: {e}")
            return []
    
    def create_mapping_prompt(self, compliance_item: ComplianceItem, batch_context: str = "") -> str:
        """Create the AI prompt for mapping a compliance item"""
        
        # Get available function names as context - limit to avoid token overflow
        available_functions = list(self.all_function_names)
        # Limit function list to stay within token limits
        functions_text = "\n".join([f"- {func}" for func in sorted(available_functions)[:300]])
        
        prompt = f"""
You are a cloud security expert working with a CSMP tool. You have access to an existing function database with 563 AWS security check functions in snake_case format.

## Task:
Map the following compliance item to existing functions and suggest new ones where gaps exist.

## Compliance Item:
- **ID**: {compliance_item.id}
- **Title**: {compliance_item.title}
- **Assessment**: {compliance_item.assessment}
- **Description**: {compliance_item.description}

## Available Functions Database (563 functions):
{functions_text}

## Instructions:
1. **Search for Matches**: Find existing functions that could satisfy this compliance requirement (semantic matching, not just exact names)
   - ONLY map functions that genuinely relate to the compliance requirement
   - Be conservative - prefer unmapped over incorrectly mapped
2. **Assess Coverage**: Determine if existing functions provide complete, partial, or no coverage
   - "complete" = all requirements covered by existing functions
   - "partial" = some requirements covered, gaps remain
   - "none" = no existing functions address this requirement
3. **Suggest New Functions**: If gaps exist and assessment is "Automated", suggest new function names following the pattern: service_resource_check_description
4. **Quality Requirements**:
   - Function names MUST be in snake_case format
   - Functions MUST be implementable with real boto3 APIs (describe_*, get_*, list_*)
   - Service field MUST match AWS service names (ec2, s3, iam, etc.)
   - Be specific and conservative in suggestions

## Output Format (JSON only):
{{
  "compliance_id": "{compliance_item.id}",
  "title": "{compliance_item.title}",
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
    
    def map_compliance_item(self, compliance_item: ComplianceItem, max_retries: int = 3) -> Optional[MappingResult]:
        """Map a single compliance item using OpenAI with retry logic for quality"""
        
        # Skip manual assessments that don't have function names
        if compliance_item.assessment.lower() == "manual" and not compliance_item.function_names:
            logger.info(f"Skipping manual assessment without function names: {compliance_item.id}")
            return None
        
        for attempt in range(max_retries):
            try:
                prompt = self.create_mapping_prompt(compliance_item)
                
                # Add rate limiting to prevent 429 errors
                time.sleep(2)  # 2 second delay between requests
                
                response = self.client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are a cloud security expert specializing in AWS compliance and security functions. Always respond with valid JSON only. Be conservative and accurate in your mappings."},
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
                            logger.warning(f"Missing required field '{field}' in response for {compliance_item.id}, attempt {attempt + 1}")
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
                            
                            logger.info(f"Successfully mapped compliance item: {compliance_item.id}")
                            return mapping_result
                        else:
                            logger.warning(f"Quality validation failed for {compliance_item.id}, attempt {attempt + 1}")
                            continue
                    
                except json.JSONDecodeError as e:
                    logger.warning(f"Failed to parse JSON response for {compliance_item.id}, attempt {attempt + 1}: {e}")
                    if attempt == max_retries - 1:
                        logger.error(f"Response was: {response_text}")
                    continue
                    
            except Exception as e:
                logger.warning(f"Error processing compliance item {compliance_item.id}, attempt {attempt + 1}: {e}")
                if attempt == max_retries - 1:
                    logger.error(f"Final attempt failed for {compliance_item.id}")
                continue
        
        logger.error(f"Failed to map compliance item {compliance_item.id} after {max_retries} attempts")
        return None
    
    def _validate_mapping_quality(self, result_data: Dict[str, Any], compliance_item: ComplianceItem) -> bool:
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
        
        return True
    
    def process_compliance_framework(self, compliance_file: str, output_file: str, batch_size: int = 5) -> Dict[str, Any]:
        """Process entire compliance framework in batches"""
        
        compliance_items = self.load_compliance_framework(compliance_file)
        if not compliance_items:
            return {"error": "Failed to load compliance framework"}
        
        results = []
        new_functions_to_add = []
        processing_stats = {
            "total_items": len(compliance_items),
            "processed": 0,
            "skipped_manual": 0,
            "mapped_complete": 0,
            "mapped_partial": 0,
            "mapped_none": 0,
            "new_functions_suggested": 0
        }
        
        # Process in batches
        for i in range(0, len(compliance_items), batch_size):
            batch = compliance_items[i:i + batch_size]
            logger.info(f"Processing batch {i//batch_size + 1}/{(len(compliance_items)-1)//batch_size + 1}")
            
            for item in batch:
                result = self.map_compliance_item(item)
                
                if result is None:
                    processing_stats["skipped_manual"] += 1
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
        output_data = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "compliance_framework": compliance_file,
                "prowler_database_functions": len(self.all_function_names),
                "processing_stats": processing_stats
            },
            "mapping_results": [self._mapping_result_to_dict(r) for r in results],
            "new_functions_suggested": new_functions_to_add
        }
        
        with open(output_file, 'w') as f:
            json.dump(output_data, f, indent=2)
        
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
    
    def update_prowler_database(self, new_functions: List[Dict[str, str]], updated_prowler_file: str):
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
        if os.path.exists(updated_prowler_file):
            with open(updated_prowler_file, 'r') as f:
                current_data = json.load(f)
        else:
            # Start with original prowler data
            with open('prowler.json', 'r') as f:
                current_data = json.load(f)
        
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
        
        # Save updated database
        with open(updated_prowler_file, 'w') as f:
            json.dump(current_data, f, indent=2)
        
        logger.info(f"Updated prowler database with {total_added} new functions")
        logger.info(f"Updated database saved to {updated_prowler_file}")


def main():
    """Main function to run the compliance mapper"""
    
    # Configuration
    PROWLER_FILE = "prowler.json"
    COMPLIANCE_FILE = "CIS_AMAZON_ELASTIC_KUBERNETES_SERVICE_(EKS)_BENCHMARK_V1.7.0_PDF.json"
    OUTPUT_FILE = f"mapping_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    UPDATED_PROWLER_FILE = f"prowler_updated_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    print("=== AWS Compliance Function Mapper ===")
    print(f"Prowler Database: {PROWLER_FILE}")
    print(f"Compliance Framework: {COMPLIANCE_FILE}")
    print(f"Output File: {OUTPUT_FILE}")
    print()
    
    # Check if files exist
    if not os.path.exists(PROWLER_FILE):
        print(f"Error: {PROWLER_FILE} not found in current directory")
        return
    
    if not os.path.exists(COMPLIANCE_FILE):
        print(f"Error: {COMPLIANCE_FILE} not found in current directory")
        return
    
    # API key will be handled by the ComplianceMapper class
    print("Initializing compliance mapper...")
    
    try:
        # Initialize mapper
        mapper = ComplianceMapper()
        
        # Load prowler database
        if not mapper.load_prowler_database(PROWLER_FILE):
            print("Failed to load prowler database")
            return
        
        print(f"Loaded {len(mapper.all_function_names)} functions from prowler database")
        
        # Process compliance framework
        print("Starting compliance framework processing...")
        results = mapper.process_compliance_framework(COMPLIANCE_FILE, OUTPUT_FILE)
        
        if "error" in results:
            print(f"Error: {results['error']}")
            return
        
        # Update prowler database with new functions
        if results.get('new_functions_suggested'):
            print(f"Updating prowler database with {len(results['new_functions_suggested'])} new functions...")
            mapper.update_prowler_database(results['new_functions_suggested'], UPDATED_PROWLER_FILE)
        
        print("\n=== Processing Complete ===")
        print(f"Results saved to: {OUTPUT_FILE}")
        print(f"Updated prowler database: {UPDATED_PROWLER_FILE}")
        print(f"Processing statistics:")
        stats = results['metadata']['processing_stats']
        for key, value in stats.items():
            print(f"  {key}: {value}")
            
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
