#!/usr/bin/env python3
#!/usr/bin/env python3
"""
Azure Compliance Function Mapping Tool using OpenAI

This tool maps existing security functions from simplified_functions.json to CIS Azure compliance frameworks 
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
        logging.FileHandler('azure_compliance_mapping.log'),
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
    functions_to_rename: List[Dict[str, str]]  # Functions to rename for clarity
    functions_to_consolidate: List[Dict[str, Any]]  # Functions to consolidate for efficiency
    coverage_assessment: str  # complete|partial|none
    new_functions_needed: List[Dict[str, str]]
    mapping_notes: str

class AzureComplianceMapper:
    """Main class for mapping Azure compliance items to security functions"""
    
    def __init__(self, openai_api_key: str = None):
        """Initialize the compliance mapper"""
        
        # 🔑 ADD YOUR OPENAI API KEY HERE:
        self.api_key = "YOUR_OPENAI_API_KEY_HERE"
        
        if not self.api_key or self.api_key == "YOUR_OPENAI_API_KEY_HERE":
            print("❌ ERROR: Please add your OpenAI API key to the script!")
            print("   Look for the line: self.api_key = 'YOUR_OPENAI_API_KEY_HERE'")
            print("   Replace it with your actual API key")
            sys.exit(1)
        
        self.client = OpenAI(api_key=self.api_key)
        self.azure_functions = {}  # Changed to dict to store function details
        self.all_function_names = set()
        
        # Create output directories
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)
        
        # Create subdirectories
        (self.output_dir / "updated_compliance").mkdir(exist_ok=True)
        (self.output_dir / "new_functions").mkdir(exist_ok=True)
        (self.output_dir / "updated_functions").mkdir(exist_ok=True)
        
    def analyze_existing_functions_for_compliance(self, compliance_item) -> List[str]:
        """Analyze existing functions to find potential matches for compliance item."""
        potential_matches = []
        
        # Keywords from compliance item
        compliance_text = f"{compliance_item.title} {compliance_item.description}".lower()
        
        # Extract key terms
        key_terms = []
        if "tls" in compliance_text or "ssl" in compliance_text:
            key_terms.extend(["tls", "ssl", "encryption", "security"])
        if "authentication" in compliance_text or "auth" in compliance_text:
            key_terms.extend(["authentication", "auth", "identity", "login"])
        if "firewall" in compliance_text:
            key_terms.extend(["firewall", "network", "security", "access"])
        if "version" in compliance_text:
            key_terms.extend(["version", "supported", "current"])
        if "https" in compliance_text:
            key_terms.extend(["https", "ssl", "tls", "encryption"])
        if "ftp" in compliance_text:
            key_terms.extend(["ftp", "ftps", "file", "transfer"])
        
        # Find functions that might match
        for func_name in self.all_function_names:
            func_lower = func_name.lower()
            
            # Check if function name contains any key terms
            if any(term in func_lower for term in key_terms):
                potential_matches.append(func_name)
            
            # Check for service-specific matches
            if "webapp" in compliance_text and "webapp" in func_lower:
                potential_matches.append(func_name)
            elif "storage" in compliance_text and "storage" in func_lower:
                potential_matches.append(func_name)
            elif "compute" in compliance_text and "compute" in func_lower:
                potential_matches.append(func_name)
        
        # Remove duplicates and return top matches
        return list(set(potential_matches))[:10]  # Limit to top 10 matches

    def load_azure_database(self, simplified_functions_file: str) -> bool:
        """Load the azure function database from simplified_functions.json"""
        try:
            with open(simplified_functions_file, 'r', encoding='utf-8') as f:
                functions_data = json.load(f)
                
            for func in functions_data:
                if 'function_name' in func and func['function_name']:
                    self.azure_functions[func['function_name']] = func
                    self.all_function_names.add(func['function_name'])
            
            logger.info(f"Loaded {len(self.all_function_names)} functions from simplified_functions.json")
            return True
            
        except FileNotFoundError:
            logger.error(f"Simplified functions file not found: {simplified_functions_file}")
            return False
        except Exception as e:
            logger.error(f"Error loading simplified functions: {e}")
            return False
    
    def load_compliance_framework(self, compliance_file: str) -> List[ComplianceItem]:
        """Load the compliance framework from JSON file"""
        try:
            with open(compliance_file, 'r', encoding='utf-8') as f:
                compliance_data = json.load(f)
            
            compliance_items = []
            for item in compliance_data:
                # Extract function names if they exist
                function_names = []
                if 'function_names' in item and item['function_names']:
                    function_names = item['function_names']
                
                compliance_item = ComplianceItem(
                    id=item.get('id', ''),
                    title=item.get('title', ''),
                    assessment=item.get('assessment', 'Automated'),
                    description=item.get('description', ''),
                    function_names=function_names,
                    rationale=item.get('rationale'),
                    audit=item.get('audit'),
                    remediation=item.get('remediation')
                )
                compliance_items.append(compliance_item)
            
            logger.info(f"Loaded {len(compliance_items)} compliance items from {compliance_file}")
            return compliance_items
            
        except Exception as e:
            logger.error(f"Error loading compliance framework: {e}")
            return []
    
    def map_compliance_item(self, compliance_item: ComplianceItem, max_retries: int = 3) -> Optional[MappingResult]:
        """Map a single compliance item using OpenAI with retry logic for quality"""
        
        # Skip manual assessments that don't have function names
        if compliance_item.assessment.lower() == "manual" and not compliance_item.function_names:
            logger.info(f"Skipping manual assessment without function names: {compliance_item.id}")
            return None
        
        # Prepare the prompt for OpenAI
        function_list = ', '.join(sorted(list(self.all_function_names)[:100]))
        
        # Analyze existing functions for potential matches
        potential_existing_functions = self.analyze_existing_functions_for_compliance(compliance_item)
        
        prompt = f"""🎯 Your task is to map compliance rules to functions using this EXACT strategy:

1. **EXISTING FUNCTION MAPPING (FIRST PRIORITY)**:
   - Check if ANY existing functions can cover this compliance requirement
   - Map existing functions that can implement the compliance check
   - Focus on semantic matching, not just exact name matches
   - If multiple existing functions can cover it, choose the BEST one

2. **FUNCTION CONSOLIDATION (SECOND PRIORITY - STRICT RULES)**:
   - For remaining compliance requirements NOT covered by existing functions:
   - **MUST consolidate into ONE function** either by:
     a) Selecting an existing function that can be extended/renamed, OR
     b) Creating ONE new consolidated function
   - **NO EXCEPTIONS**: Multiple similar functions are NOT allowed
   - Goal: Minimize total function count while maintaining coverage

3. **NAMING STANDARDS (STRICT ENFORCEMENT)**:
   - **MUST follow**: <service><resource><requirement>[_<qualifier>]
   - **Examples**:
     ✅ `keyvault_vault_firewall_enabled`
     ✅ `storage_account_public_access_blocked`
     ✅ `appservice_web_remote_debugging_disabled`
     ❌ `container_app_remote_debugging_disabled` (wrong structure)
     ❌ `app_service_function_app_remote_debugging_disabled` (redundant words)
   - **Service names**: Use short, clear names (keyvault, storage, appservice, compute)
   - **Resource names**: Use clear, specific names (vault, account, web, vm)
   - **Requirements**: Use clear, specific requirements (firewall_enabled, public_access_blocked)
   - **NO vague verbs**: check, validate, verify, inspect, audit
   - **Focus on state**: Describe desired secure state, not the action

4. **CONSOLIDATION RULES (MANDATORY)**:
   - **Similar functions MUST be consolidated**: If multiple functions check the same thing, consolidate into ONE
   - **Cross-service functions**: If a requirement applies to multiple services, create ONE generic function
   - **Examples of what to consolidate**:
     - Multiple "remote debugging" functions → ONE `remote_debugging_disabled`
     - Multiple "TLS version" functions → ONE `minimum_tls_version_12`
     - Multiple "authentication" functions → ONE `basic_auth_disabled`

5. **COVERAGE ASSESSMENT (FINAL CHECK)**:
   - After mapping existing + consolidation: do we have complete coverage?
   - "complete" = all requirements covered by existing + consolidated functions
   - "partial" = some requirements covered, gaps remain
   - "none" = no coverage possible with current approach

RESPONSE FORMAT (JSON):
{{
    "existing_functions_mapped": ["function1", "function2"],
    "functions_to_rename": [
        {{
            "old_name": "poorly_named_function",
            "new_name": "service_resource_requirement_qualifier",
            "rationale": "Why this rename improves clarity and follows naming standards"
        }}
    ],
    "functions_to_consolidate": [
        {{
            "old_functions": ["func1", "func2", "func3"],
            "new_consolidated_function": "service_resource_requirement_qualifier",
            "rationale": "Why consolidation improves efficiency and reduces duplication"
        }}
    ],
    "coverage_assessment": "complete|partial|none",
    "new_functions_needed": [
        {{
            "function_name": "service_resource_requirement_qualifier",
            "description": "One-line description of what this function checks",
            "azure_sdk_example": "client.service.resource.get()",
            "service_category": "Network|Compute|Identity|Storage|Database|Security"
        }}
    ],
    "mapping_notes": "Technical explanation of mapping decisions, consolidation benefits, and naming optimizations"
}}

MAPPING STRATEGY:
1. FIRST: Try to map existing functions that can cover this compliance
2. SECOND: If gaps remain, consolidate into ONE function (existing or new) - NO EXCEPTIONS
3. THIRD: Assess final coverage - do we need additional functions?
4. GOAL: Maximum coverage with minimum function count

NAMING ENFORCEMENT:
- **REQUIRED**: <service><resource><requirement>[_<qualifier>]
- **NO redundant words**: Don't repeat "app", "service", etc.
- **NO vague verbs**: Use specific state descriptions
- **CONSOLIDATE similar functions**: Multiple similar functions = ONE consolidated function

POTENTIAL EXISTING FUNCTIONS TO CONSIDER:
{', '.join(potential_existing_functions) if potential_existing_functions else 'None identified'}

ALL AVAILABLE EXISTING FUNCTIONS:
{function_list}

COMPLIANCE ITEM TO MAP:
ID: {compliance_item.id}
Title: {compliance_item.title}
Description: {compliance_item.description}
Current Functions: {compliance_item.function_names or 'None'}

Map this compliance item following the EXACT strategy above. REMEMBER: Consolidate similar functions into ONE, follow naming standards strictly."""
        
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.0,  # Set to 0 for maximum determinism - no over-engineering
                    max_tokens=1000
                )
                
                content = response.choices[0].message.content.strip()
                
                # Try to extract JSON from the response
                if content.startswith('```json'):
                    content = content[7:-3]  # Remove ```json and ```
                elif content.startswith('```'):
                    content = content[3:-3]  # Remove ``` and ```
                
                mapping_data = json.loads(content)
                
                # Validate the response structure
                required_fields = ['existing_functions_mapped', 'coverage_assessment', 'new_functions_needed', 'mapping_notes']
                if all(field in mapping_data for field in required_fields):
                    # Handle optional fields
                    functions_to_rename = mapping_data.get('functions_to_rename', [])
                    functions_to_consolidate = mapping_data.get('functions_to_consolidate', [])
                    
                    return MappingResult(
                        compliance_id=compliance_item.id,
                        title=compliance_item.title,
                        existing_functions_mapped=mapping_data['existing_functions_mapped'],
                        functions_to_rename=functions_to_rename,
                        functions_to_consolidate=functions_to_consolidate,
                        coverage_assessment=mapping_data['coverage_assessment'],
                        new_functions_needed=mapping_data['new_functions_needed'],
                        mapping_notes=mapping_data['mapping_notes']
                    )
                else:
                    logger.warning(f"Invalid response structure for {compliance_item.id}, attempt {attempt + 1}")
                    continue
                    
            except json.JSONDecodeError as e:
                logger.warning(f"JSON decode error for {compliance_item.id}, attempt {attempt + 1}: {e}")
                if attempt == max_retries - 1:
                    logger.error(f"Failed to parse response for {compliance_item.id} after {max_retries} attempts")
                    return None
                time.sleep(2 ** attempt)  # Exponential backoff
                continue
                
            except Exception as e:
                if "rate limit" in str(e).lower() or "429" in str(e):
                    wait_time = 60 * (attempt + 1)  # Progressive backoff
                    logger.info(f"Rate limited, waiting {wait_time} seconds...")
                    time.sleep(wait_time)
                    continue
                else:
                    logger.error(f"Unexpected error mapping {compliance_item.id}: {e}")
                    return None
        
        return None
    
    def process_compliance_framework(self, compliance_file: str, max_items: int = None) -> List[MappingResult]:
        """Process the entire compliance framework and return mapping results"""
        
        # Load compliance items
        compliance_items = self.load_compliance_framework(compliance_file)
        if not compliance_items:
            logger.error("No compliance items loaded")
            return []
        
        # Limit items if specified
        if max_items:
            compliance_items = compliance_items[:max_items]
            logger.info(f"Processing limited to {max_items} items for testing")
        
        # Process each compliance item
        mapping_results = []
        total_items = len(compliance_items)
        
        for i, item in enumerate(compliance_items, 1):
            logger.info(f"Processing item {i}/{total_items}: {item.id} - {item.title}")
            
            result = self.map_compliance_item(item)
            if result:
                mapping_results.append(result)
                logger.info(f"✅ Mapped {item.id}: {result.coverage_assessment} coverage")
            else:
                logger.warning(f"❌ Failed to map {item.id}")
            
            # Small delay to avoid rate limiting
            time.sleep(1)
        
        return mapping_results
    
    def save_mapping_results(self, results: List[MappingResult], output_file: str):
        """Save mapping results to JSON file"""
        output_data = {
            "mapping_summary": {
                "total_items": len(results),
                "timestamp": datetime.now().isoformat(),
                "coverage_breakdown": {
                    "complete": len([r for r in results if r.coverage_assessment == "complete"]),
                    "partial": len([r for r in results if r.coverage_assessment == "partial"]),
                    "none": len([r for r in results if r.coverage_assessment == "none"])
                }
            },
            "mapping_results": [vars(result) for result in results]
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Mapping results saved to {output_file}")
    
    def update_compliance_file(self, compliance_file: str, mapping_results: List[MappingResult], output_file: str):
        """Update compliance file with mapped functions and apply consolidation"""
        
        # Load original compliance file
        with open(compliance_file, 'r') as f:
            compliance_data = json.load(f)
        
        # Create a mapping from compliance_id to mapping result
        id_to_mapping = {item.compliance_id: item for item in mapping_results}
        
        # Update each compliance item
        updated_count = 0
        for item in compliance_data:
            compliance_id = item.get('id')
            if compliance_id in id_to_mapping:
                mapping = id_to_mapping[compliance_id]
                
                # Start with existing functions that are mapped
                final_functions = list(mapping.existing_functions_mapped)
                
                # Apply consolidation: remove old functions, keep consolidated ones
                if mapping.functions_to_consolidate:
                    for consolidation in mapping.functions_to_consolidate:
                        # Remove old functions from the final list
                        old_functions = consolidation['old_functions']
                        final_functions = [f for f in final_functions if f not in old_functions]
                        
                        # Add the new consolidated function
                        final_functions.append(consolidation['new_consolidated_function'])
                
                # Add new functions needed (if any)
                for new_func in mapping.new_functions_needed:
                    final_functions.append(new_func['function_name'])
                
                # Remove duplicates and update
                item['function_names'] = list(set(final_functions))
                item['mapped_coverage'] = mapping.coverage_assessment
                item['mapping_notes'] = mapping.mapping_notes
                item['last_mapped'] = datetime.now().isoformat()
                
                # Add consolidation info for transparency
                if mapping.functions_to_consolidate:
                    item['consolidation_info'] = mapping.functions_to_consolidate
                
                updated_count += 1
        
        # Save updated compliance file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(compliance_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Updated {updated_count} compliance items in {output_file}")
    
    def extract_new_functions(self, mapping_results: List[MappingResult], output_file: str):
        """Extract new functions needed for Python code generation"""
        
        new_functions = []
        for result in mapping_results:
            for new_func in result.new_functions_needed:
                new_functions.append({
                    "compliance_id": result.compliance_id,
                    "compliance_title": result.title,
                    "function_name": new_func['function_name'],
                    "description": new_func['description'],
                    "azure_sdk_example": new_func['azure_sdk_example'],
                    "service_category": new_func['service_category'],
                    "coverage_assessment": result.coverage_assessment,
                    "mapping_notes": result.mapping_notes
                })
        
        # Save new functions
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(new_functions, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Extracted {len(new_functions)} new functions to {output_file}")
    
    def update_simplified_functions(self, mapping_results: List[MappingResult], output_file: str):
        """Update simplified_functions.json with new functions"""
        
        # Load existing simplified functions
        with open('simplified_functions.json', 'r') as f:
            existing_functions = json.load(f)
        
        # Collect all new functions
        new_functions = []
        for result in mapping_results:
            for new_func in result.new_functions_needed:
                new_function_entry = {
                    "sheet": "CIS",
                    "rule_id": result.compliance_id,
                    "description": new_func['description'],
                    "function_name": new_func['function_name'],
                    "azure_sdk_example": new_func['azure_sdk_example'],
                    "service_category": new_func['service_category']
                }
                new_functions.append(new_function_entry)
        
        # Add new functions to existing ones
        updated_functions = existing_functions + new_functions
        
        # Save updated functions
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(updated_functions, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Updated simplified functions with {len(new_functions)} new functions: {output_file}")
    
    def run_mapping(self, compliance_file: str, simplified_functions_file: str, max_items: int = None):
        """Main method to run the complete mapping process"""
        
        logger.info("🚀 Starting Azure Compliance Mapping Process")
        
        # Load Azure function database
        if not self.load_azure_database(simplified_functions_file):
            logger.error("Failed to load Azure function database")
            return
        
        # Process compliance framework
        mapping_results = self.process_compliance_framework(compliance_file, max_items)
        if not mapping_results:
            logger.error("No mapping results generated")
            return
        
        # Create timestamp for output files
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save mapping results
        mapping_file = self.output_dir / f"azure_mapping_results_{timestamp}.json"
        self.save_mapping_results(mapping_results, str(mapping_file))
        
        # Update compliance file
        compliance_output = self.output_dir / "updated_compliance" / f"updated_{Path(compliance_file).name}"
        self.update_compliance_file(compliance_file, mapping_results, str(compliance_output))
        
        # Extract new functions
        new_functions_file = self.output_dir / "new_functions" / f"azure_new_functions_{timestamp}.json"
        self.extract_new_functions(mapping_results, str(new_functions_file))
        
        # Update simplified functions
        updated_functions_file = self.output_dir / "updated_functions" / f"simplified_functions_updated_{timestamp}.json"
        self.update_simplified_functions(mapping_results, str(updated_functions_file))
        
        # Print summary
        logger.info("🎉 Azure Compliance Mapping Complete!")
        logger.info(f"📊 Processed: {len(mapping_results)} items")
        
        # Count existing functions mapped
        total_existing_mapped = sum(len(result.existing_functions_mapped) for result in mapping_results)
        total_renamed = sum(len(result.functions_to_rename) for result in mapping_results)
        total_consolidated = sum(len(result.functions_to_consolidate) for result in mapping_results)
        total_new = sum(len(result.new_functions_needed) for result in mapping_results)
        
        logger.info(f"🔄 Existing functions mapped: {total_existing_mapped}")
        logger.info(f"🔄 Functions to rename: {total_renamed}")
        logger.info(f"🔗 Functions to consolidate: {total_consolidated}")
        logger.info(f"🆕 New functions suggested: {total_new}")
        logger.info(f"📁 Outputs saved to: output/")
        logger.info(f"   - Mapping results: {mapping_file}")
        logger.info(f"   - Updated compliance: {compliance_output}")
        logger.info(f"   - New functions: {new_functions_file}")
        logger.info(f"   - Updated functions: {updated_functions_file}")

def main():
    """Main function to run the compliance mapper"""
    
    # Configuration
    compliance_file = "CIS_MICROSOFT_AZURE_COMPUTE_SERVICES_BENCHMARK_V2.0.0.json"
    simplified_functions_file = "simplified_functions.json"
    
    print("🚀 Azure Compliance Function Mapper")
    print(f"�� Compliance File: {compliance_file}")
    print(f"�� Functions Database: {simplified_functions_file}")
    print()
    
    # Initialize mapper
    mapper = AzureComplianceMapper()
    
    # Run mapping (process only 10 items for testing)
    mapper.run_mapping(compliance_file, simplified_functions_file, max_items=10)

if __name__ == "__main__":
    main()