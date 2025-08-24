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
import hashlib
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
        self.api_key = os.getenv("OPENAI_API_KEY")
        
        # Model configuration with fallback
        self.model_default = "gpt-4o-mini"
        self.model_fallback = "gpt-4o"
        
        self.client = OpenAI(api_key=self.api_key)
        self.kubernetes_functions = {}
        self.all_function_names = set()
        
        # Initialize cache
        self.cache_file = "kubernetes_pci_cache.jsonl"
        self.cache = {}
        self._cache_hits = 0
        self._load_cache()
        
        # Create output directory
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)
        
    def _load_cache(self):
        """Load existing cache from file"""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.strip():
                            cache_entry = json.loads(line.strip())
                            self.cache[cache_entry['key']] = cache_entry['value']
                logger.info(f"Loaded {len(self.cache)} cached responses")
            except Exception as e:
                logger.warning(f"Failed to load cache: {e}")
    
    def _cache_key(self, payload: str) -> str:
        """Generate cache key from payload"""
        return hashlib.sha256(payload.encode('utf-8')).hexdigest()
    
    def _cache_get(self, key: str) -> Optional[Dict[str, Any]]:
        """Get cached response if exists"""
        return self.cache.get(key)
    
    def _cache_put(self, key: str, value: Dict[str, Any]):
        """Store response in cache and save to file"""
        self.cache[key] = value
        try:
            with open(self.cache_file, 'a', encoding='utf-8') as f:
                json.dump({'key': key, 'value': value}, f)
                f.write('\n')
        except Exception as e:
            logger.warning(f"Failed to save to cache file: {e}")
    
    def _truncate_text(self, text: str, max_length: int = 1000) -> str:
        """Truncate text to safe length while preserving meaning"""
        if not text or len(text) <= max_length:
            return text
        
        # Try to truncate at sentence boundary
        truncated = text[:max_length]
        last_period = truncated.rfind('.')
        last_exclamation = truncated.rfind('!')
        last_question = truncated.rfind('?')
        
        # Find the last sentence boundary
        last_boundary = max(last_period, last_exclamation, last_question)
        
        if last_boundary > max_length * 0.8:  # If we can find a good boundary
            return truncated[:last_boundary + 1] + " [truncated]"
        else:
            return truncated + " [truncated]"
        
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
                    DefinedApproachRequirements=self._truncate_text(item.get('DefinedApproachRequirements', ''), 1000),
                    Purpose=self._truncate_text(item.get('Purpose', ''), 800),
                    GoodPractice=self._truncate_text(item.get('GoodPractice', ''), 800),
                    Definitions=self._truncate_text(item.get('Definitions', ''), 600),
                    Examples=self._truncate_text(item.get('Examples', ''), 600),
                    CustomizedApproachObjective=self._truncate_text(item.get('CustomizedApproachObjective', ''), 800),
                    ApplicabilityNotes=self._truncate_text(item.get('ApplicabilityNotes', ''), 600),
                    FurtherInformation=self._truncate_text(item.get('FurtherInformation', ''), 600),
                    function_names=function_names
                )
                compliance_items.append(compliance_item)
            
            logger.info(f"Loaded {len(compliance_items)} PCI DSS compliance items from {compliance_file}")
            return compliance_items
            
        except Exception as e:
            logger.error(f"Error loading PCI DSS compliance framework: {e}")
            return []
    
    def create_batch_mapping_prompt(self, compliance_items: List[PCIComplianceItem], existing_functions: List[str]) -> str:
        """Create a prompt for mapping multiple compliance items to functions in batch"""
        
        # Create batch context
        batch_context = "## Batch Items to Process:\n"
        for i, item in enumerate(compliance_items, 1):
            batch_context += f"""
### Item {i}: {item.RequirementID}
- **Defined Approach Requirements**: {item.DefinedApproachRequirements}
- **Purpose**: {item.Purpose}
- **Good Practice**: {item.GoodPractice}
- **Definitions**: {item.Definitions}
- **Examples**: {item.Examples}
- **Customized Approach Objective**: {item.CustomizedApproachObjective}
- **Applicability Notes**: {item.ApplicabilityNotes}
- **Further Information**: {item.FurtherInformation}
"""
        
        prompt = f"""
Map the following PCI DSS compliance requirements to Kubernetes security functions. Process ALL items in the batch.

Available Kubernetes Functions ({len(existing_functions)} functions):
{', '.join(existing_functions[:50])}  # Showing first 50 for brevity

Instructions:
1. Analyze each PCI DSS requirement and identify which Kubernetes security functions could help implement or verify this control
2. ONLY suggest functions that can be implemented programmatically using Kubernetes APIs (kubectl, client-go, etc.)
3. DO NOT suggest functions for policy, documentation, procedures, training, or manual processes
4. Focus on technical controls that can be checked via Kubernetes APIs
5. If no existing functions match, or existing function not able to cover full compliance, suggest new function names that follow Kubernetes naming conventions
6. All function names must be in snake_case format
7. New functions must start with Kubernetes service prefixes (e.g., k8s_pod_, k8s_service_, k8s_rbac_, k8s_network_)
8. Assess coverage as: "complete", "partial", or "none"

Return a JSON object with:
{{
    "batch_results": [
        {{
            "compliance_id": "requirement_id",
            "title": "PCI DSS requirement_id",
            "existing_functions_mapped": ["list", "of", "existing", "function", "names"],
            "coverage_assessment": "complete|partial|none",
            "new_functions_needed": [
                {{
                    "name": "k8s_service_specific_function_name",
                    "kubernetes_api": "k8s.api.method()",
                    "service": "k8s_service_name",
                    "rationale": "Why this function is needed"
                }}
            ],
            "mapping_notes": "Explanation of the mapping and any gaps identified"
        }}
    ]
}}

{batch_context}

Return ONLY the JSON response, no other text.
"""
        return prompt
    
    def _validate_mapping_quality(self, suggested_functions: List[str]) -> bool:
        """Validate that suggested functions are appropriate for Kubernetes"""
        non_checkable_keywords = [
            'documentation', 'procedure', 'training', 'manual'
        ]
        
        k8s_service_prefixes = [
            'k8s_pod_', 'k8s_service_', 'k8s_rbac_', 'k8s_network_',
            'k8s_secret_', 'k8s_configmap_', 'k8s_namespace_', 'k8s_node_',
            'k8s_deployment_', 'k8s_statefulset_', 'k8s_daemonset_', 'k8s_job_',
            'k8s_cronjob_', 'k8s_persistentvolume_', 'k8s_storageclass_', 'k8s_ingress_'
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
    
    def map_compliance_batch(self, compliance_items: List[PCIComplianceItem], max_retries: int = 3) -> List[Optional[MappingResult]]:
        """Map multiple compliance items to functions using OpenAI with fallback model support"""
        
        # Get potential existing functions
        existing_functions = list(self.all_function_names)
        
        # Create batch payload for caching
        batch_payload = json.dumps([{
            'requirement_id': item.RequirementID,
            'defined_approach_requirements': item.DefinedApproachRequirements,
            'purpose': item.Purpose,
            'good_practice': item.GoodPractice,
            'definitions': item.Definitions,
            'examples': item.Examples,
            'customized_approach_objective': item.CustomizedApproachObjective,
            'applicability_notes': item.ApplicabilityNotes,
            'further_information': item.FurtherInformation
        } for item in compliance_items], sort_keys=True)
        
        cache_key = self._cache_key(batch_payload)
        cached_result = self._cache_get(cache_key)
        if cached_result:
            logger.info(f"Using cached result for batch of {len(compliance_items)} items")
            # Update cache hit statistics
            if hasattr(self, '_cache_hits'):
                self._cache_hits += 1
            return self._parse_batch_response(cached_result, compliance_items)
        
        for attempt in range(max_retries):
            try:
                # Try default model first
                model_to_use = self.model_default
                
                # Check if we should use fallback model based on previous attempts
                if attempt > 0 and model_to_use == self.model_default:
                    # If first attempt with default model failed, try fallback
                    model_to_use = self.model_fallback
                    logger.info(f"Attempt {attempt + 1}: Using fallback model {self.model_fallback}")
                
                prompt = self.create_batch_mapping_prompt(compliance_items, existing_functions)
                
                logger.info(f"Calling OpenAI API with model: {model_to_use}")
                response = self.client.chat.completions.create(
                    model=model_to_use,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an expert in Kubernetes security and PCI DSS compliance mapping. You ONLY suggest functions that can be implemented programmatically using Kubernetes APIs. You DO NOT suggest functions for policy, documentation, procedures, training, or manual processes. All function names must be in snake_case and start with Kubernetes service prefixes."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.3,
                    max_tokens=2000,
                    response_format={"type": "json_object"}  # Ensure JSON output
                )
                
                content = response.choices[0].message.content.strip()
                
                # Parse JSON response
                try:
                    mapping_data = json.loads(content)
                    
                    # Validate batch response structure
                    if 'batch_results' not in mapping_data:
                        logger.warning(f"Missing 'batch_results' in response, attempt {attempt + 1}")
                        continue
                    
                    batch_results = mapping_data['batch_results']
                    if len(batch_results) != len(compliance_items):
                        logger.warning(f"Batch size mismatch: expected {len(compliance_items)}, got {len(batch_results)}, attempt {attempt + 1}")
                        continue
                    
                    # Validate each result
                    valid_results = []
                    for i, result in enumerate(batch_results):
                        suggested_functions = result.get('new_functions_needed', [])
                        suggested_names = [func.get('name', '') for func in suggested_functions]
                        
                        if self._validate_mapping_quality(suggested_names):
                            valid_results.append(result)
                        else:
                            logger.warning(f"Quality validation failed for item {i} in batch, attempt {attempt + 1}")
                    
                    if len(valid_results) == len(compliance_items):
                        # Check if any items have low coverage and we're using default model
                        if model_to_use == self.model_default:
                            low_coverage_count = sum(1 for r in valid_results if r.get('coverage_assessment') == 'none')
                            if low_coverage_count > 0 and attempt == 0:
                                logger.info(f"Batch has {low_coverage_count} items with 'none' coverage, retrying with fallback model")
                                model_to_use = self.model_fallback
                                continue
                        
                        # Cache successful result
                        self._cache_put(cache_key, mapping_data)
                        
                        # Convert to MappingResult objects
                        mapping_results = self._parse_batch_response(mapping_data, compliance_items)
                        logger.info(f"Successfully mapped batch of {len(compliance_items)} PCI DSS requirements using {model_to_use}")
                        return mapping_results
                    else:
                        logger.warning(f"Only {len(valid_results)}/{len(compliance_items)} items passed validation, attempt {attempt + 1}")
                        continue
                    
                except json.JSONDecodeError as e:
                    logger.warning(f"Failed to parse JSON response for batch, attempt {attempt + 1}: {e}")
                    if attempt == max_retries - 1:
                        logger.error(f"Response was: {content}")
                    continue
                    
            except Exception as e:
                logger.warning(f"Error processing batch, attempt {attempt + 1}: {e}")
                
                # If default model fails, try fallback model
                if model_to_use == self.model_default and attempt == 0:
                    logger.info(f"Default model {self.model_default} failed, trying fallback {self.model_fallback}")
                    model_to_use = self.model_fallback
                    continue
                
                # If fallback model also fails, log the error
                if model_to_use == self.model_fallback and attempt == 1:
                    logger.warning(f"Fallback model {self.model_fallback} also failed for batch")
                
                if attempt == max_retries - 1:
                    logger.error(f"Final attempt failed for batch")
                continue
        
        logger.error(f"Failed to map batch of {len(compliance_items)} PCI DSS requirements after {max_retries} attempts")
        return [None] * len(compliance_items)
    
    def _parse_batch_response(self, mapping_data: Dict[str, Any], compliance_items: List[PCIComplianceItem]) -> List[Optional[MappingResult]]:
        """Parse batch response and convert to MappingResult objects"""
        mapping_results = []
        batch_results = mapping_data.get('batch_results', [])
        
        for i, result in enumerate(batch_results):
            if i < len(compliance_items):
                try:
                    mapping_result = MappingResult(
                        compliance_id=result['compliance_id'],
                        title=result['title'],
                        existing_functions_mapped=result['existing_functions_mapped'],
                        coverage_assessment=result['coverage_assessment'],
                        new_functions_needed=result['new_functions_needed'],
                        mapping_notes=result['mapping_notes']
                    )
                    mapping_results.append(mapping_result)
                except KeyError as e:
                    logger.error(f"Missing required field in batch result {i}: {e}")
                    mapping_results.append(None)
            else:
                mapping_results.append(None)
        
        return mapping_results
    
    def map_compliance_item(self, compliance_item: PCIComplianceItem, max_retries: int = 3) -> Optional[MappingResult]:
        """Map a single compliance item to functions using OpenAI (backward compatibility)"""
        results = self.map_compliance_batch([compliance_item], max_retries)
        return results[0] if results else None
    
    def process_pci_compliance_framework(self, compliance_items: List[PCIComplianceItem], test_mode: bool = False, batch_size: int = 5) -> Dict[str, Any]:
        """Process the entire PCI DSS compliance framework using batch processing"""
        
        logger.info("Starting PCI DSS compliance framework processing...")
        
        if test_mode:
            compliance_items = compliance_items[:5]
            logger.info(f"TEST MODE: Processing only {len(compliance_items)} items")
        
        results = []
        new_functions_count = 0
        failed_items = []
        batches_processed = 0
        cache_hits = 0
        
        # Process in batches
        for i in range(0, len(compliance_items), batch_size):
            batch = compliance_items[i:i + batch_size]
            batch_num = (i // batch_size) + 1
            total_batches = (len(compliance_items) + batch_size - 1) // batch_size
            
            logger.info(f"Processing batch {batch_num}/{total_batches} ({len(batch)} items)")
            
            # Check cache first
            batch_payload = json.dumps([{
                'requirement_id': item.RequirementID,
                'defined_approach_requirements': item.DefinedApproachRequirements,
                'purpose': item.Purpose,
                'good_practice': item.GoodPractice,
                'definitions': item.Definitions,
                'examples': item.Examples,
                'customized_approach_objective': item.CustomizedApproachObjective,
                'applicability_notes': item.ApplicabilityNotes,
                'further_information': item.FurtherInformation
            } for item in batch], sort_keys=True)
            
            cache_key = self._cache_key(batch_payload)
            if self._cache_get(cache_key):
                cache_hits += 1
            
            mapping_results = self.map_compliance_batch(batch)
            if mapping_results:
                for mapping_result in mapping_results:
                    if mapping_result:
                        results.append(mapping_result)
                        new_functions_count += len(mapping_result.new_functions_needed)
                        logger.info(f"Successfully mapped PCI DSS requirement: {mapping_result.compliance_id}")
                    else:
                        # Create a failed mapping result with "manual" function
                        failed_result = MappingResult(
                            compliance_id=batch[0].RequirementID,  # Use first item as reference
                            title=f"PCI DSS {batch[0].RequirementID}",
                            existing_functions_mapped=[],
                            coverage_assessment="manual",
                            new_functions_needed=[{"name": "manual", "description": "Requires manual review - not programmatically checkable"}],
                            mapping_notes="This requirement requires manual review and cannot be automated programmatically"
                        )
                        results.append(failed_result)
                        failed_items.append(batch[0].RequirementID)
                        logger.warning(f"Failed to map item in batch {batch_num} - marked as manual")
                
                batches_processed += 1
                logger.info(f"Successfully processed batch {batch_num}/{total_batches}")
            else:
                logger.warning(f"Failed to process batch {batch_num}/{total_batches}")
            
            # Rate limiting between batches
            if i + batch_size < len(compliance_items):
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
                    "batches_processed": batches_processed,
                    "cache_hits": cache_hits,
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
            "test_mode": test_mode,
            "batches_processed": batches_processed,
            "cache_hits": cache_hits
        }
    
    def _update_kubernetes_functions(self, results: List[MappingResult]):
        """Update kubernetes functions with new suggested functions"""
        new_functions = []
        
        for result in results:
            for new_func in result.new_functions_needed:
                new_function_data = {
                    "function_name": new_func["name"],
                    "k8s_api": new_func["kubernetes_api"], # Changed from k8s_api to kubernetes_api
                    "service": new_func["service"],
                    "rationale": new_func["rationale"],
                    "compliance_control": result.compliance_id,
                    "created_at": datetime.now().isoformat()
                }
                new_functions.append(new_function_data)
        
        if new_functions:
            # Load existing functions
            kubernetes_file = "kubernetes_updated_nist_20250824_005159.json"
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
    if not mapper.load_kubernetes_database("kubernetes_updated_nist_20250824_005159.json"):
        print("❌ Failed to load Kubernetes function database")
        return
    
    # Load PCI DSS compliance framework
    compliance_items = mapper.load_pci_compliance_framework("PCI-DSS-v4_0_1 copy.json")
    if not compliance_items:
        print("❌ Failed to load PCI DSS compliance framework")
        return
    
    # Process compliance framework
    print("Starting PCI DSS compliance framework processing...")
    stats = mapper.process_pci_compliance_framework(compliance_items, test_mode=False, batch_size=5)
    
    print("\n=== Processing Complete ===")
    print(f"Results saved to: output/")
    print("Processing statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Print batch processing summary
    if 'batches_processed' in stats:
        print(f"\n📊 BATCH PROCESSING SUMMARY:")
        print(f"  Batches processed: {stats['batches_processed']}")
        print(f"  Cache hits: {stats['cache_hits']}")
        print(f"  Test mode: {'Enabled' if stats['test_mode'] else 'Disabled'}")

if __name__ == "__main__":
    main()
