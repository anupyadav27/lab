# #!/usr/bin/env python3
# """
# GCP Compliance Function Mapping Tool using OpenAI

# This tool maps existing security functions from gcp_simplified_function_names.json to CIS GCP compliance frameworks 
# and suggests new functions where gaps exist, following the same high-quality standards as Azure and Kubernetes mappers.
# """

# import json
# import os
# import sys
# import time
# from typing import Dict, List, Any, Optional
# from dataclasses import dataclass
# from pathlib import Path
# import logging
# from datetime import datetime

# # Check if openai is installed, if not prompt user to install
# try:
#     from openai import OpenAI
# except ImportError:
#     print("Error: openai library not found. Please install it with:")
#     print("pip install openai")
#     sys.exit(1)

# # Setup logging
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(levelname)s - %(message)s',
#     handlers=[
#         logging.FileHandler('gcp_compliance_mapping.log'),
#         logging.StreamHandler()
#     ]
# )
# logger = logging.getLogger(__name__)

# @dataclass
# class ComplianceItem:
#     """Represents a single compliance requirement"""
#     id: str
#     title: str
#     assessment: str
#     description: str
#     function_names: List[str]
#     rationale: Optional[str] = None
#     audit: Optional[str] = None
#     remediation: Optional[str] = None

# @dataclass
# class MappingResult:
#     """Represents the result of mapping a compliance item to functions"""
#     compliance_id: str
#     title: str
#     existing_functions_mapped: List[str]
#     functions_to_rename: List[Dict[str, str]]  # Functions to rename for clarity
#     functions_to_consolidate: List[Dict[str, Any]]  # Functions to consolidate for efficiency
#     coverage_assessment: int  # 1-10 scale (1=no coverage, 10=complete coverage)
#     new_functions_needed: List[Dict[str, str]]
#     mapping_notes: str

# class GCPComplianceMapper:
#     """Main class for mapping GCP compliance items to security functions"""
    
#     def __init__(self, openai_api_key: str = None):
#         """Initialize the compliance mapper"""
        
#         # 🔑 ADD YOUR OPENAI API KEY HERE:
#         self.api_key = "YOUR_OPENAI_API_KEY_HERE"
        
#         if not self.api_key or self.api_key == "YOUR_OPENAI_API_KEY_HERE":
#             print("❌ ERROR: Please add your OpenAI API key to the script!")
#             print("   Look for the line: self.api_key = 'YOUR_OPENAI_API_KEY_HERE'")
#             print("   Replace it with your actual API key")
#             sys.exit(1)
        
#         self.client = OpenAI(api_key=self.api_key)
#         self.gcp_functions = {}
#         self.all_function_names = set()
        
#         # Create output directories
#         self.output_dir = Path("output")
#         self.output_dir.mkdir(exist_ok=True)
        
#         # Create subdirectories
#         (self.output_dir / "updated_compliance").mkdir(exist_ok=True)
#         (self.output_dir / "new_functions").mkdir(exist_ok=True)
#         (self.output_dir / "updated_functions").mkdir(exist_ok=True)
        
#     def load_gcp_database(self, gcp_file: str) -> bool:
#         """Load the GCP function database"""
#         try:
#             with open(gcp_file, 'r') as f:
#                 data = json.load(f)
            
#             # GCP functions are stored as a list of objects with function_name field
#             if isinstance(data, list):
#                 self.gcp_functions = {"GCP_Functions": data}
                
#                 # Extract function names from objects
#                 for item in data:
#                     if isinstance(item, dict) and 'function_name' in item:
#                         func_name = item['function_name']
#                         if isinstance(func_name, str) and func_name.strip():
#                             self.all_function_names.add(func_name.strip())
#             else:
#                 self.gcp_functions = data
                
#                 # Handle nested structure if needed
#                 for service_data in self.gcp_functions.values():
#                     if isinstance(service_data, list):
#                         for item in service_data:
#                             if isinstance(item, dict) and 'function_name' in item:
#                                 func_name = item['function_name']
#                                 if isinstance(func_name, str) and func_name.strip():
#                                     self.all_function_names.add(func_name.strip())
#                     elif isinstance(service_data, dict):
#                         for func_name in service_data.get('check_functions', []):
#                             if isinstance(func_name, str) and func_name.strip():
#                                 self.all_function_names.add(func_name.strip())
            
#             logger.info(f"Loaded {len(self.all_function_names)} functions from GCP database")
#             return True
            
#         except FileNotFoundError:
#             logger.error(f"GCP file not found: {gcp_file}")
#             return False
#         except json.JSONDecodeError as e:
#             logger.error(f"Error parsing GCP JSON: {e}")
#             return False
    
#     def load_compliance_framework(self, compliance_file: str) -> List[ComplianceItem]:
#         """Load compliance framework from JSON file"""
#         try:
#             # with open(compliance_file, 'r') as f:
#             #     data = json.load(f)
#             with open(compliance_file, "r", encoding="utf-8", errors="replace") as f:
#                  data = json.load(f)
            
#             compliance_items = []
#             for item in data:
#                 if isinstance(item, dict) and 'id' in item and 'title' in item:
#                     compliance_item = ComplianceItem(
#                         id=item.get('id', ''),
#                         title=item.get('title', ''),
#                         assessment=item.get('assessment', ''),
#                         description=item.get('description', ''),
#                         function_names=item.get('function_names', []),
#                         rationale=item.get('rationale'),
#                         audit=item.get('audit'),
#                         remediation=item.get('remediation')
#                     )
#                     compliance_items.append(compliance_item)
            
#             logger.info(f"Loaded {len(compliance_items)} compliance items")
#             return compliance_items
            
#         except FileNotFoundError:
#             logger.error(f"Compliance file not found: {compliance_file}")
#             return []
#         except json.JSONDecodeError as e:
#             logger.error(f"Error parsing compliance JSON: {e}")
#             return []
    
#     def analyze_existing_functions_for_compliance(self, compliance_item: ComplianceItem) -> List[str]:
#         """Analyze existing functions to find potential matches for compliance item"""
#         potential_matches = []
        
#         # Keywords from compliance item
#         compliance_text = f"{compliance_item.title} {compliance_item.description}".lower()
        
#         # Extract key terms based on GCP services
#         key_terms = []
        
#         # IAM and Identity Management
#         if any(term in compliance_text for term in ["iam", "identity", "authentication", "authorization", "service account", "mfa", "security key"]):
#             key_terms.extend(["iam", "identity", "authentication", "authorization", "service_account", "mfa", "security_key"])
        
#         # Compute Services
#         if any(term in compliance_text for term in ["compute", "gke", "cloud run", "app engine", "cloud functions", "vm", "instance"]):
#             key_terms.extend(["compute", "gke", "cloud_run", "app_engine", "cloud_functions", "vm", "instance"])
        
#         # Storage Services
#         if any(term in compliance_text for term in ["storage", "bigquery", "cloud sql", "spanner", "firestore", "bucket", "dataset"]):
#             key_terms.extend(["storage", "bigquery", "cloud_sql", "spanner", "firestore", "bucket", "dataset"])
        
#         # Networking
#         if any(term in compliance_text for term in ["vpc", "firewall", "subnet", "load balancer", "cloud armor", "cdn", "interconnect"]):
#             key_terms.extend(["vpc", "firewall", "subnet", "load_balancer", "cloud_armor", "cdn", "interconnect"])
        
#         # Security Services
#         if any(term in compliance_text for term in ["kms", "security center", "access context", "binary authorization", "assured workloads"]):
#             key_terms.extend(["kms", "security_center", "access_context", "binary_authorization", "assured_workloads"])
        
#         # Monitoring and Logging
#         if any(term in compliance_text for term in ["logging", "monitoring", "trace", "error reporting", "profiler", "debugger"]):
#             key_terms.extend(["logging", "monitoring", "trace", "error_reporting", "profiler", "debugger"])
        
#         # Organization and Policies
#         if any(term in compliance_text for term in ["organization", "policy", "resource manager", "billing", "quotas"]):
#             key_terms.extend(["organization", "policy", "resource_manager", "billing", "quotas"])
        
#         # Encryption and Keys
#         if any(term in compliance_text for term in ["encryption", "cmek", "kms", "key", "certificate", "tls", "ssl"]):
#             key_terms.extend(["encryption", "cmek", "kms", "key", "certificate", "tls", "ssl"])
        
#         # Search for functions that match key terms
#         for func_name in self.all_function_names:
#             func_lower = func_name.lower()
#             if any(term in func_lower for term in key_terms):
#                 potential_matches.append(func_name)
        
#         return potential_matches
    
#     def create_mapping_prompt(self, compliance_item: ComplianceItem, potential_existing_functions: List[str]) -> str:
#         """Create high-quality AI prompt for mapping compliance items"""
        
#         # Get available function names as context - limit to avoid token overflow
#         available_functions = list(self.all_function_names)
#         # Limit to 25 functions to stay well within token limits
#         functions_text = "\n".join([f"- {func}" for func in sorted(available_functions)[:25]])
        
#         prompt = f"""
# You are a GCP security expert working with a CSMP tool. You have access to an existing function database with {len(self.all_function_names)} GCP security check functions in snake_case format.

# ## TASK:
# Map the following compliance item to existing functions and suggest new ones where gaps exist, following STRICT quality standards.

# ## COMPLIANCE ITEM:
# - **ID**: {compliance_item.id}
# - **Title**: {compliance_item.title}
# - **Assessment**: {compliance_item.assessment}
# - **Description**: {compliance_item.description[:200]}{'...' if len(compliance_item.description) > 200 else ''}
# - **Rationale**: {compliance_item.rationale[:150] + '...' if compliance_item.rationale and len(compliance_item.rationale) > 150 else (compliance_item.rationale or 'Not provided')}

# ## AVAILABLE FUNCTIONS DATABASE ({len(self.all_function_names)} functions):
# **Note: Showing first 25 functions for token efficiency. Search the full database for best matches.**
# {functions_text}

# ## POTENTIAL EXISTING FUNCTIONS TO CONSIDER:
# {', '.join(potential_existing_functions) if potential_existing_functions else 'None identified'}

# ## IMPORTANT INSTRUCTIONS:
# - **ALWAYS check the functions database above FIRST** before suggesting new functions
# - **ONLY use function names that actually exist** in the database for mapping
# - **Be THOROUGH in function discovery** - look for semantic matches, not just exact name matches
# - **If no existing functions match**, then suggest new functions to fill gaps
# - **Coverage score should reflect**: existing function mapping quality + new function completeness
# - **Goal: Maximize coverage by finding ALL relevant existing functions**

# ## MAPPING STRATEGY (FOLLOW EXACTLY):

# 1. **EXISTING FUNCTION MAPPING (FIRST PRIORITY)**:
#    - **MUST check the GCP functions database first** - look for existing functions that can cover this compliance requirement
#    - Map existing functions that can implement the compliance check
#    - **Be THOROUGH** - look for semantic matches, related functions, and partial matches
#    - **Map MULTIPLE functions** if they can collectively cover the requirement
#    - Focus on semantic matching, not just exact name matches
#    - If multiple existing functions can cover it, map ALL relevant ones
#    - ONLY map functions that genuinely relate to the compliance requirement
#    - **CRITICAL**: Use the actual function names from the database, don't make up function names

# 2. **FUNCTION CONSOLIDATION (SECOND PRIORITY - STRICT RULES)**:
#    - For remaining compliance requirements NOT covered by existing functions:
#    - **MUST consolidate into ONE function** either by:
#      a) Selecting an existing function that can be extended/renamed, OR
#      b) Creating ONE new consolidated function
#    - **NO EXCEPTIONS**: Multiple similar functions are NOT allowed
#    - Goal: Minimize total function count while maintaining coverage

# 3. **NAMING STANDARDS (STRICT ENFORCEMENT)**:
#    - **MUST follow**: <service><resource><requirement>[_<qualifier>]
#    - **GCP Service Examples**:
#      ✅ `iam_user_mfa_enabled`
#      ✅ `compute_instance_public_access_blocked`
#      ✅ `storage_bucket_public_access_restricted`
#      ✅ `kms_key_rotation_enabled`
#      ❌ `gcp_compute_instance_public_access_blocked` (redundant 'gcp')
#      ❌ `compute_vm_instance_public_access_blocked` (redundant 'vm_instance')
#    - **Service names**: Use short, clear names (iam, compute, storage, kms, bigquery, gke)
#    - **Resource names**: Use clear, specific names (user, instance, bucket, key, cluster, dataset)
#    - **Requirements**: Use clear, specific requirements (mfa_enabled, public_access_blocked, encryption_enabled)
#    - **NO vague verbs**: check, validate, verify, inspect, audit
#    - **Focus on state**: Describe desired secure state, not the action

# 4. **CONSOLIDATION RULES (MANDATORY)**:
#    - **Similar functions MUST be consolidated**: If multiple functions check the same thing, consolidate into ONE
#    - **Cross-service functions**: If a requirement applies to multiple services, create ONE generic function
#    - **Examples of what to consolidate**:
#      - Multiple "MFA" functions → ONE `user_mfa_enabled`
#      - Multiple "TLS version" functions → ONE `minimum_tls_version_12`
#      - Multiple "public access" functions → ONE `public_access_restricted`

# 5. **COVERAGE ASSESSMENT (FINAL CHECK)**:
#    - After mapping existing functions AND suggesting new functions, assess overall coverage
#    - Consider THREE categories for complete coverage:
#      a) Existing functions mapped from database
#      b) Unmapped potential functions from database that could cover gaps
#      c) New functions proposed to fill remaining gaps
#    - 10 = Complete coverage (all three categories combined cover ALL requirements)
#    - 7-9 = High coverage (three categories combined cover most requirements, minor gaps)
#    - 4-6 = Medium coverage (three categories combined cover some requirements, significant gaps)
#    - 1-3 = Low coverage (three categories combined cover few requirements, major gaps)
#    - Goal: Ensure the combination of all three categories provides comprehensive compliance coverage

# ## RESPONSE FORMAT (JSON ONLY):
# {{
#     "compliance_id": "{compliance_item.id}",
#     "title": "{compliance_item.title}",
#     "existing_functions_mapped": ["function1", "function2"],
#     "functions_to_rename": [
#         {{
#             "old_name": "poorly_named_function",
#             "new_name": "service_resource_requirement_qualifier",
#             "rationale": "Why this rename improves clarity and follows naming standards"
#         }}
#     ],
#     "functions_to_consolidate": [
#         {{
#             "old_functions": ["func1", "func2", "func3"],
#             "new_consolidated_function": "service_resource_requirement_qualifier",
#             "rationale": "Why consolidation improves efficiency and reduces duplication"
#         }}
#     ],
#     "coverage_assessment": 7,
#     "new_functions_needed": [
#         {{
#             "function_name": "service_resource_requirement_qualifier",
#             "description": "One-line description of what this function checks",
#             "gcp_api_example": "gcloud service resource get --project=PROJECT_ID",
#             "service_category": "Identity|Compute|Storage|Network|Security|Monitoring|Organization"
#         }}
#     ],
#     "mapping_notes": "Technical explanation of mapping decisions, consolidation benefits, and naming optimizations"
# }}

# ## QUALITY REQUIREMENTS:
# - **Function names MUST be in snake_case format**
# - **Functions MUST be implementable with real GCP APIs (gcloud, REST API)**
# - **Service field MUST match GCP service names (iam, compute, storage, kms, etc.)**
# - **Be specific and conservative in suggestions**
# - **NO over-engineering or unnecessary complexity**

# ## MAPPING APPROACH:
# 1. FIRST: Try to map existing functions that can cover this compliance
# 2. SECOND: If gaps remain, consolidate into ONE function (existing or new) - NO EXCEPTIONS
# 3. THIRD: Assess final coverage - do we need additional functions?
# 4. GOAL: Maximum coverage with minimum function count

# Return ONLY the JSON response, no other text.
# """
#         return prompt
    
#     def map_compliance_item(self, compliance_item: ComplianceItem, max_retries: int = 3) -> Optional[MappingResult]:
#         """Map a single compliance item using OpenAI with retry logic for quality"""
        
#         # Skip manual assessments that don't have function names
#         if compliance_item.assessment.lower() == "manual" and not compliance_item.function_names:
#             logger.info(f"Skipping manual assessment without function names: {compliance_item.id}")
#             return None
        
#         for attempt in range(max_retries):
#             try:
#                 # Analyze existing functions first
#                 potential_existing_functions = self.analyze_existing_functions_for_compliance(compliance_item)
                
#                 # Create high-quality prompt
#                 prompt = self.create_mapping_prompt(compliance_item, potential_existing_functions)
                
#                 # Check prompt length to avoid token issues
#                 estimated_tokens = len(prompt.split()) * 1.3  # Rough token estimation
#                 if estimated_tokens > 6000:  # Leave room for response
#                     logger.warning(f"Prompt too long ({estimated_tokens:.0f} estimated tokens) for {compliance_item.id}, truncating...")
#                     # Truncate the prompt
#                     prompt = prompt[:4000] + "\n\n[Prompt truncated for token efficiency]"
                
#                 # Add rate limiting to prevent 429 errors
#                 time.sleep(5)  # 5 second delay between requests to avoid rate limiting
                
#                 response = self.client.chat.completions.create(
#                     model="gpt-4",
#                     messages=[
#                         {"role": "system", "content": "You are a GCP security expert specializing in compliance and security functions. Always respond with valid JSON only. Be conservative and accurate in your mappings."},
#                         {"role": "user", "content": prompt}
#                     ],
#                     temperature=0.2,  # Slightly higher temperature for better coverage discovery
#                     max_tokens=600,  # Reduced tokens to avoid context length issues
#                     top_p=0.3,       # Allow more variety in function selection
#                     frequency_penalty=0,
#                     presence_penalty=0
#                 )
                
#                 response_text = response.choices[0].message.content.strip()
                
#                 # Parse JSON response
#                 try:
#                     result_data = json.loads(response_text)
                    
#                     # Validate required fields
#                     required_fields = ['compliance_id', 'title', 'existing_functions_mapped', 
#                                      'coverage_assessment', 'new_functions_needed', 'mapping_notes']
                    
#                     for field in required_fields:
#                         if field not in result_data:
#                             logger.warning(f"Missing required field '{field}' in response for {compliance_item.id}, attempt {attempt + 1}")
#                             break
#                     else:
#                         # Validate data quality
#                         if self._validate_mapping_quality(result_data, compliance_item):
#                             # Calculate intelligent coverage score
#                             existing_functions = result_data['existing_functions_mapped']
#                             new_functions = result_data['new_functions_needed']
#                             intelligent_coverage = self._calculate_intelligent_coverage(existing_functions, new_functions, compliance_item)
                            
#                             # Create MappingResult with intelligent coverage
#                             # Check for unmapped potential functions
#                             potential_existing = self.analyze_existing_functions_for_compliance(compliance_item)
#                             unmapped_potential = [f for f in potential_existing if f not in existing_functions]
                            
#                             coverage_note = f"""Coverage Analysis:
# - Coverage Score: {intelligent_coverage}/10
# - Existing Functions Mapped: {len(existing_functions)} ({', '.join(existing_functions) if existing_functions else 'None'})
# - Unmapped Potential Functions: {len(unmapped_potential)} ({', '.join(unmapped_potential[:3]) if unmapped_potential else 'None'}{'...' if len(unmapped_potential) > 3 else ''})
# - New Functions Proposed: {len(new_functions)} ({', '.join([f['function_name'] for f in new_functions]) if new_functions else 'None'})

# Total Coverage: The combination of mapped existing functions + unmapped potential functions + new proposed functions should provide comprehensive compliance coverage."""
                            
#                             updated_mapping_notes = f"{result_data['mapping_notes']}\n\n{coverage_note}"
                            
#                             mapping_result = MappingResult(
#                                 compliance_id=result_data['compliance_id'],
#                                 title=result_data['title'],
#                                 existing_functions_mapped=result_data['existing_functions_mapped'],
#                                 functions_to_rename=result_data.get('functions_to_rename', []),
#                                 functions_to_consolidate=result_data.get('functions_to_consolidate', []),
#                                 coverage_assessment=intelligent_coverage,
#                                 new_functions_needed=result_data['new_functions_needed'],
#                                 mapping_notes=updated_mapping_notes
#                             )
                            
#                             logger.info(f"Successfully mapped compliance item: {compliance_item.id}")
#                             return mapping_result
#                         else:
#                             logger.warning(f"Quality validation failed for {compliance_item.id}, attempt {attempt + 1}")
#                             continue
                    
#                 except json.JSONDecodeError as e:
#                     logger.warning(f"Failed to parse JSON response for {compliance_item.id}, attempt {attempt + 1}: {e}")
#                     if attempt == max_retries - 1:
#                         logger.error(f"Response was: {response_text}")
#                     continue
                    
#             except Exception as e:
#                 logger.warning(f"Error processing compliance item {compliance_item.id}, attempt {attempt + 1}: {e}")
#                 if attempt == max_retries - 1:
#                     logger.error(f"Final attempt failed for {compliance_item.id}")
#                 continue
        
#         logger.error(f"Failed to map compliance item {compliance_item.id} after {max_retries} attempts")
        
#         # Create a fallback result with basic information
#         fallback_coverage = self._calculate_intelligent_coverage([], [], compliance_item)
#         fallback_result = MappingResult(
#             compliance_id=compliance_item.id,
#             title=compliance_item.title,
#             existing_functions_mapped=[],
#             functions_to_rename=[],
#             functions_to_consolidate=[],
#             coverage_assessment=fallback_coverage,
#             new_functions_needed=[],
#             mapping_notes=f"Failed to process due to API errors. Coverage score {fallback_coverage}/10 calculated based on basic analysis."
#         )
        
#         return fallback_result
    
#     def _validate_mapping_quality(self, result_data: Dict[str, Any], compliance_item: ComplianceItem) -> bool:
#         """Validate the quality of the mapping result"""
        
#         # Check if mapped functions actually exist in our database
#         mapped_functions = result_data.get('existing_functions_mapped', [])
#         invalid_functions = [f for f in mapped_functions if f not in self.all_function_names]
        
#         if invalid_functions:
#             logger.warning(f"Invalid functions suggested: {invalid_functions}")
#             return False
        
#         # Validate coverage assessment values (1-10 scale)
#         coverage_score = result_data.get('coverage_assessment')
#         if not isinstance(coverage_score, int) or coverage_score < 1 or coverage_score > 10:
#             logger.warning(f"Invalid coverage assessment: {coverage_score}. Must be integer 1-10.")
#             return False
        
#         # Check new functions format
#         new_functions = result_data.get('new_functions_needed', [])
#         for func in new_functions:
#             if not isinstance(func, dict):
#                 return False
#             required_func_fields = ['function_name', 'description', 'gcp_api_example', 'service_category']
#             if not all(field in func for field in required_func_fields):
#                 logger.warning(f"New function missing required fields: {func}")
#                 return False
            
#             # Validate function name format (snake_case)
#             func_name = func.get('function_name', '')
#             if not func_name.islower() or not all(c.isalnum() or c == '_' for c in func_name):
#                 logger.warning(f"Invalid function name format: {func_name}")
#                 return False
        
#         return True
    
#     def _calculate_intelligent_coverage(self, existing_functions: List[str], new_functions: List[Dict], compliance_item: ComplianceItem) -> int:
#         """Calculate intelligent coverage score based on comprehensive function analysis"""
        
#         # Analyze compliance requirements
#         compliance_text = f"{compliance_item.title} {compliance_item.description}".lower()
        
#         # Check if we have existing functions that could cover this (even if not mapped)
#         potential_existing_functions = self.analyze_existing_functions_for_compliance(compliance_item)
        
#         # Calculate coverage components
#         existing_mapped_score = 0
#         unmapped_potential_score = 0
#         new_functions_score = 0
        
#         # 1. Score for existing functions mapped (max 4 points)
#         if existing_functions:
#             for func in existing_functions:
#                 if func in self.all_function_names:
#                     # Check relevance to compliance requirement
#                     relevance = self._calculate_function_relevance(func, compliance_text)
#                     existing_mapped_score += relevance
#             existing_mapped_score = min(4, existing_mapped_score)
        
#         # 2. Score for unmapped potential functions (max 3 points)
#         unmapped_potential = [f for f in potential_existing_functions if f not in existing_functions]
#         if unmapped_potential:
#             # These functions exist but weren't mapped - they could fill gaps
#             unmapped_potential_score = min(3, len(unmapped_potential) * 0.8)
        
#         # 3. Score for new functions proposed (max 3 points)
#         if new_functions:
#             # Assess quality and completeness of new function suggestions
#             new_functions_score = min(3, len(new_functions) * 1.0)
        
#         # Calculate total coverage score
#         total_score = existing_mapped_score + unmapped_potential_score + new_functions_score
        
#         # Normalize to 1-10 scale
#         if total_score >= 8:
#             return 10  # Complete coverage
#         elif total_score >= 6:
#             return 8   # High coverage
#         elif total_score >= 4:
#             return 6   # Medium coverage
#         elif total_score >= 2:
#             return 4   # Low-medium coverage
#         else:
#             return 2   # Low coverage
    
#     def _calculate_function_relevance(self, function_name: str, compliance_text: str) -> float:
#         """Calculate how relevant a function is to a compliance requirement"""
        
#         func_lower = function_name.lower()
#         relevance_score = 0.0
        
#         # IAM and Identity Management (more comprehensive matching)
#         if any(term in compliance_text for term in ['iam', 'identity', 'authentication', 'authorization', 'user', 'mfa', 'security key', 'service account', 'corporate', 'consumer']):
#             if any(keyword in func_lower for keyword in ['iam', 'user', 'mfa', 'security', 'authentication', 'authorization', 'service_account', 'corporate', 'consumer', 'account']):
#                 relevance_score += 1.0
        
#         # Compute Services (more comprehensive matching)
#         if any(term in compliance_text for term in ['compute', 'gke', 'cloud run', 'app engine', 'vm', 'instance', 'container', 'kubernetes']):
#             if any(keyword in func_lower for keyword in ['compute', 'gke', 'cloud_run', 'app_engine', 'vm', 'instance', 'container', 'kubernetes']):
#                 relevance_score += 1.0
        
#         # Storage Services (more comprehensive matching)
#         if any(term in compliance_text for term in ['storage', 'bigquery', 'cloud sql', 'bucket', 'dataset', 'database', 'data']):
#             if any(keyword in func_lower for keyword in ['storage', 'bigquery', 'cloud_sql', 'bucket', 'dataset', 'database', 'data']):
#                 relevance_score += 1.0
        
#         # Networking (more comprehensive matching)
#         if any(term in compliance_text for term in ['vpc', 'firewall', 'subnet', 'network', 'traffic', 'access', 'public', 'private']):
#             if any(keyword in func_lower for keyword in ['vpc', 'firewall', 'subnet', 'network', 'traffic', 'access', 'public', 'private']):
#                 relevance_score += 1.0
        
#         # Security Services (more comprehensive matching)
#         if any(term in compliance_text for term in ['kms', 'encryption', 'key', 'security center', 'security', 'compliance', 'audit']):
#             if any(keyword in func_lower for keyword in ['kms', 'encryption', 'key', 'security', 'compliance', 'audit']):
#                 relevance_score += 1.0
        
#         # Monitoring and Logging (more comprehensive matching)
#         if any(term in compliance_text for term in ['logging', 'monitoring', 'audit', 'trace', 'log', 'event', 'activity']):
#             if any(keyword in func_lower for keyword in ['logging', 'monitoring', 'audit', 'trace', 'log', 'event', 'activity']):
#                 relevance_score += 1.0
        
#         # Additional relevance for partial matches
#         if any(word in func_lower for word in compliance_text.split() if len(word) > 3):
#             relevance_score += 0.5
        
#         return relevance_score
    
#     def process_compliance_framework(self, compliance_items: List[ComplianceItem], batch_size: int = 5) -> List[MappingResult]:
#         """Process all compliance items and generate mapping results"""
#         results = []
        
#         # Process in batches
#         for i in range(0, len(compliance_items), batch_size):
#             batch = compliance_items[i:i + batch_size]
#             logger.info(f"Processing batch {i//batch_size + 1}/{(len(compliance_items)-1)//batch_size + 1}")
            
#             for item in batch:
#                 logger.info(f"Processing compliance item: {item.id}")
                
#                 try:
#                     result = self.map_compliance_item(item)
                    
#                     if result is None:
#                         logger.warning(f"Failed to map compliance item: {item.id}")
#                         continue
                    
#                     results.append(result)
                    
#                     # Rate limiting
#                     time.sleep(1)
                    
#                 except Exception as e:
#                     logger.error(f"Error processing {item.id}: {e}")
#                     continue
        
#         return results
    
#     def save_results(self, results: List[MappingResult], timestamp: str):
#         """Save mapping results to output files"""
        
#         # Save comprehensive results
#         output_file = self.output_dir / "updated_compliance" / f"gcp_mapping_results_{timestamp}.json"
#         with open(output_file, 'w') as f:
#             json.dump([result.__dict__ for result in results], f, indent=2)
#         logger.info(f"Saved comprehensive results to {output_file}")
        
#         # Save new functions needed
#         new_functions = []
#         for result in results:
#             new_functions.extend(result.new_functions_needed)
        
#         if new_functions:
#             new_functions_file = self.output_dir / "new_functions" / f"gcp_new_functions_{timestamp}.json"
#             with open(new_functions_file, 'w') as f:
#                 json.dump(new_functions, f, indent=2)
#             logger.info(f"Saved {len(new_functions)} new functions to {new_functions_file}")
        
#         # Save functions to rename
#         rename_functions = []
#         for result in results:
#             rename_functions.extend(result.functions_to_rename)

#         if rename_functions:
#             rename_file = self.output_dir / "updated_functions" / f"gcp_rename_functions_{timestamp}.json"
#             with open(rename_file, 'w') as f:
#                 json.dump(rename_functions, f, indent=2)
#             logger.info(f"Saved {len(rename_functions)} rename suggestions to {rename_file}")

#         # Save functions to rename
#         # rename_functions = []
#         # for result in results:
#         #     rename_functions.extend(result.functions_to_rename)
        
#         # if rename_functions:
#         #     rename_file = self.output_dir / "updated_functions" / f"gcp_rename_functions_{timestamp}.json"
#         #     with open(rename_file, 'w') as f:
#         #         json.dump(rename_functions, f, indent=2)
#         #     logger.info(f"Saved {len(rename_functions)} rename suggestions to {rename_file}")
        
#         # Generate summary report with coverage breakdown
#         coverage_breakdown = {
#             "10 (Complete)": len([r for r in results if r.coverage_assessment == 10]),
#             "7-9 (High)": len([r for r in results if 7 <= r.coverage_assessment <= 9]),
#             "4-6 (Medium)": len([r for r in results if 4 <= r.coverage_assessment <= 6]),
#             "1-3 (Low)": len([r for r in results if 1 <= r.coverage_assessment <= 3])
#         }
        
#         avg_coverage = sum(r.coverage_assessment for r in results) / len(results) if results else 0
        
#         summary = {
#             "total_compliance_items": len(results),
#             "average_coverage_score": round(avg_coverage, 2),
#             "coverage_breakdown": coverage_breakdown,
#             "total_new_functions_needed": len(new_functions),
#             "total_rename_suggestions": len(rename_functions),
#             "timestamp": timestamp
#         }
        
#         summary_file = self.output_dir / f"gcp_mapping_summary_{timestamp}.json"
#         with open(summary_file, 'w') as f:
#             json.dump(summary, f, indent=2)
#         logger.info(f"Saved summary to {summary_file}")
        
#         return summary
    
#     def run_mapping(self, gcp_file: str, compliance_file: str, max_items: int = None, test_mode: bool = False):
#         """Run the complete mapping process"""
#         if test_mode:
#             print("🧪 TEST MODE ENABLED - Processing limited items for validation")
#             print("="*60)
#         else:
#             print("🚀 PRODUCTION MODE - Processing all compliance items")
#             print("="*60)
        
#         logger.info("Starting GCP compliance mapping process...")
        
#         # Load data
#         if not self.load_gcp_database(gcp_file):
#             logger.error("Failed to load GCP database")
#             return
        
#         compliance_items = self.load_compliance_framework(compliance_file)
#         if not compliance_items:
#             logger.error("Failed to load compliance framework")
#             return
        
#         # Limit items for testing if specified
#         if max_items:
#             compliance_items = compliance_items[:max_items]
#             if test_mode:
#                 print(f"✅ Testing with first {len(compliance_items)} compliance items")
#                 print(f"   This allows you to validate the mapping quality before full run")
#             else:
#                 logger.info(f"Limited to first {len(compliance_items)} compliance items")
        
#         # Process compliance items
#         results = self.process_compliance_framework(compliance_items)
        
#         # Save results
#         timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#         summary = self.save_results(results, timestamp)
        
#         # Print summary
#         print("\n" + "="*60)
#         if test_mode:
#             print("🧪 GCP COMPLIANCE MAPPING TEST COMPLETE")
#         else:
#             print("🚀 GCP COMPLIANCE MAPPING COMPLETE")
#         print("="*60)
#         print(f"Total compliance items processed: {summary['total_compliance_items']}")
#         print(f"Average coverage score: {summary['average_coverage_score']}/10")
#         print("\nCoverage Breakdown:")
#         for coverage_range, count in summary['coverage_breakdown'].items():
#             print(f"  {coverage_range}: {count} items")
#         print(f"\nNew functions needed: {summary['total_new_functions_needed']}")
#         print(f"Rename suggestions: {summary['total_rename_suggestions']}")
#         print(f"Results saved to: {self.output_dir}")
        
#         if test_mode:
#             print("\n📋 NEXT STEPS:")
#             print("   1. Review the mapping results in output/ directory")
#             print("   2. Validate function suggestions and naming quality")
#             print("   3. If satisfied, run without --test flag for full compliance framework")
#             print("   4. Example: python gcp_compliance_mapper.py input.json compliance.json")
        
#         print("="*60)

# def main():
#     """Main function"""
#     if len(sys.argv) < 3:
#         print("Usage: python gcp_compliance_mapper.py <gcp_functions_file> <compliance_file> [--test] [max_items]")
#         print("\nExamples:")
#         print("  # Test mode with 15 items")
#         print("  python gcp_compliance_mapper.py gcp_functions.json compliance.json --test 15")
#         print("\n  # Production mode - all items")
#         print("  python gcp_compliance_mapper.py gcp_functions.json compliance.json")
#         print("\n  # Limited items without test mode")
#         print("  python gcp_compliance_mapper.py gcp_functions.json compliance.json 20")
#         sys.exit(1)
    
#     gcp_file = sys.argv[1]
#     compliance_file = sys.argv[2]
    
#     # Parse arguments
#     test_mode = False
#     max_items = None
    
#     for arg in sys.argv[3:]:
#         if arg == "--test":
#             test_mode = True
#         elif arg.isdigit():
#             max_items = int(arg)
#         else:
#             print(f"Error: Unknown argument: {arg}")
#             print("Use --test for test mode, or a number for max items")
#             sys.exit(1)
    
#     # Check if files exist
#     if not os.path.exists(gcp_file):
#         print(f"Error: GCP functions file not found: {gcp_file}")
#         sys.exit(1)
    
#     if not os.path.exists(compliance_file):
#         print(f"Error: Compliance file not found: {compliance_file}")
#         sys.exit(1)
    
#     # Initialize and run mapper
#     mapper = GCPComplianceMapper()
#     mapper.run_mapping(gcp_file, compliance_file, max_items, test_mode)

# if __name__ == "__main__":
#     main()




#!/usr/bin/env python3
"""
GCP Compliance Function Mapping Tool using OpenAI

This tool maps existing security functions from gcp_simplified_function_names.json to CIS GCP compliance frameworks 
and suggests new functions where gaps exist, following the same high-quality standards as Azure and Kubernetes mappers.
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
        logging.FileHandler('gcp_compliance_mapping.log'),
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
    coverage_assessment: int  # 1-10 scale (1=no coverage, 10=complete coverage)
    new_functions_needed: List[Dict[str, str]]
    mapping_notes: str

class GCPComplianceMapper:
    """Main class for mapping GCP compliance items to security functions"""
    
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
        self.gcp_functions = {}
        self.all_function_names = set()
        
        # Create output directories
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)
        
        # Create subdirectories
        (self.output_dir / "updated_compliance").mkdir(exist_ok=True)
        (self.output_dir / "new_functions").mkdir(exist_ok=True)
        (self.output_dir / "updated_functions").mkdir(exist_ok=True)
        
    def load_gcp_database(self, gcp_file: str) -> bool:
        """Load the GCP function database"""
        try:
            with open(gcp_file, 'r') as f:
                data = json.load(f)
            
            # GCP functions are stored as a list of objects with function_name field
            if isinstance(data, list):
                self.gcp_functions = {"GCP_Functions": data}
                
                # Extract function names from objects
                for item in data:
                    if isinstance(item, dict) and 'function_name' in item:
                        func_name = item['function_name']
                        if isinstance(func_name, str) and func_name.strip():
                            self.all_function_names.add(func_name.strip())
            else:
                self.gcp_functions = data
                
                # Handle nested structure if needed
                for service_data in self.gcp_functions.values():
                    if isinstance(service_data, list):
                        for item in service_data:
                            if isinstance(item, dict) and 'function_name' in item:
                                func_name = item['function_name']
                                if isinstance(func_name, str) and func_name.strip():
                                    self.all_function_names.add(func_name.strip())
                    elif isinstance(service_data, dict):
                        for func_name in service_data.get('check_functions', []):
                            if isinstance(func_name, str) and func_name.strip():
                                self.all_function_names.add(func_name.strip())
            
            logger.info(f"Loaded {len(self.all_function_names)} functions from GCP database")
            return True
            
        except FileNotFoundError:
            logger.error(f"GCP file not found: {gcp_file}")
            return False
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing GCP JSON: {e}")
            return False
    
    def load_compliance_framework(self, compliance_file: str) -> List[ComplianceItem]:
        """Load compliance framework from JSON file"""
        try:
            with open(compliance_file, 'r') as f:
                data = json.load(f)
            
            compliance_items = []
            for item in data:
                if isinstance(item, dict) and 'id' in item and 'title' in item:
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
    
    def analyze_existing_functions_for_compliance(self, compliance_item: ComplianceItem) -> List[str]:
        """Analyze existing functions to find potential matches for compliance item"""
        potential_matches = []
        
        # Keywords from compliance item
        compliance_text = f"{compliance_item.title} {compliance_item.description}".lower()
        
        # Extract key terms based on GCP services
        key_terms = []
        
        # IAM and Identity Management
        if any(term in compliance_text for term in ["iam", "identity", "authentication", "authorization", "service account", "mfa", "security key"]):
            key_terms.extend(["iam", "identity", "authentication", "authorization", "service_account", "mfa", "security_key"])
        
        # Compute Services
        if any(term in compliance_text for term in ["compute", "gke", "cloud run", "app engine", "cloud functions", "vm", "instance"]):
            key_terms.extend(["compute", "gke", "cloud_run", "app_engine", "cloud_functions", "vm", "instance"])
        
        # Storage Services
        if any(term in compliance_text for term in ["storage", "bigquery", "cloud sql", "spanner", "firestore", "bucket", "dataset"]):
            key_terms.extend(["storage", "bigquery", "cloud_sql", "spanner", "firestore", "bucket", "dataset"])
        
        # Networking
        if any(term in compliance_text for term in ["vpc", "firewall", "subnet", "load balancer", "cloud armor", "cdn", "interconnect"]):
            key_terms.extend(["vpc", "firewall", "subnet", "load_balancer", "cloud_armor", "cdn", "interconnect"])
        
        # Security Services
        if any(term in compliance_text for term in ["kms", "security center", "access context", "binary authorization", "assured workloads"]):
            key_terms.extend(["kms", "security_center", "access_context", "binary_authorization", "assured_workloads"])
        
        # Monitoring and Logging
        if any(term in compliance_text for term in ["logging", "monitoring", "trace", "error reporting", "profiler", "debugger"]):
            key_terms.extend(["logging", "monitoring", "trace", "error_reporting", "profiler", "debugger"])
        
        # Organization and Policies
        if any(term in compliance_text for term in ["organization", "policy", "resource manager", "billing", "quotas"]):
            key_terms.extend(["organization", "policy", "resource_manager", "billing", "quotas"])
        
        # Encryption and Keys
        if any(term in compliance_text for term in ["encryption", "cmek", "kms", "key", "certificate", "tls", "ssl"]):
            key_terms.extend(["encryption", "cmek", "kms", "key", "certificate", "tls", "ssl"])
        
        # Search for functions that match key terms
        for func_name in self.all_function_names:
            func_lower = func_name.lower()
            if any(term in func_lower for term in key_terms):
                potential_matches.append(func_name)
        
        return potential_matches
    
    def create_mapping_prompt(self, compliance_item: ComplianceItem, potential_existing_functions: List[str]) -> str:
        """Create high-quality AI prompt for mapping compliance items"""
        
        # Get available function names as context - limit to avoid token overflow
        available_functions = list(self.all_function_names)
        # Limit to 25 functions to stay well within token limits
        functions_text = "\n".join([f"- {func}" for func in sorted(available_functions)[:25]])
        
        prompt = f"""
You are a GCP security expert working with a CSMP tool. You have access to an existing function database with {len(self.all_function_names)} GCP security check functions in snake_case format.

## TASK:
Map the following compliance item to existing functions and suggest new ones where gaps exist, following STRICT quality standards.

## COMPLIANCE ITEM:
- **ID**: {compliance_item.id}
- **Title**: {compliance_item.title}
- **Assessment**: {compliance_item.assessment}
- **Description**: {compliance_item.description[:200]}{'...' if len(compliance_item.description) > 200 else ''}
- **Rationale**: {compliance_item.rationale[:150] + '...' if compliance_item.rationale and len(compliance_item.rationale) > 150 else (compliance_item.rationale or 'Not provided')}

## AVAILABLE FUNCTIONS DATABASE ({len(self.all_function_names)} functions):
**Note: Showing first 25 functions for token efficiency. Search the full database for best matches.**
{functions_text}

## POTENTIAL EXISTING FUNCTIONS TO CONSIDER:
{', '.join(potential_existing_functions) if potential_existing_functions else 'None identified'}

## IMPORTANT INSTRUCTIONS:
- **ALWAYS check the functions database above FIRST** before suggesting new functions
- **ONLY use function names that actually exist** in the database for mapping
- **Be THOROUGH in function discovery** - look for semantic matches, not just exact name matches
- **If no existing functions match**, then suggest new functions to fill gaps
- **Coverage score should reflect**: existing function mapping quality + new function completeness
- **Goal: Maximize coverage by finding ALL relevant existing functions**

## MAPPING STRATEGY (FOLLOW EXACTLY):

1. **EXISTING FUNCTION MAPPING (FIRST PRIORITY)**:
   - **MUST check the GCP functions database first** - look for existing functions that can cover this compliance requirement
   - Map existing functions that can implement the compliance check
   - **Be THOROUGH** - look for semantic matches, related functions, and partial matches
   - **Map MULTIPLE functions** if they can collectively cover the requirement
   - Focus on semantic matching, not just exact name matches
   - If multiple existing functions can cover it, map ALL relevant ones
   - ONLY map functions that genuinely relate to the compliance requirement
   - **CRITICAL**: Use the actual function names from the database, don't make up function names

2. **FUNCTION CONSOLIDATION (SECOND PRIORITY - STRICT RULES)**:
   - For remaining compliance requirements NOT covered by existing functions:
   - **MUST consolidate into ONE function** either by:
     a) Selecting an existing function that can be extended/renamed, OR
     b) Creating ONE new consolidated function
   - **NO EXCEPTIONS**: Multiple similar functions are NOT allowed
   - Goal: Minimize total function count while maintaining coverage

3. **NAMING STANDARDS (STRICT ENFORCEMENT)**:
   - **MUST follow**: <service><resource><requirement>[_<qualifier>]
   - **GCP Service Examples**:
     ✅ `iam_user_mfa_enabled`
     ✅ `compute_instance_public_access_blocked`
     ✅ `storage_bucket_public_access_restricted`
     ✅ `kms_key_rotation_enabled`
     ❌ `gcp_compute_instance_public_access_blocked` (redundant 'gcp')
     ❌ `compute_vm_instance_public_access_blocked` (redundant 'vm_instance')
   - **Service names**: Use short, clear names (iam, compute, storage, kms, bigquery, gke)
   - **Resource names**: Use clear, specific names (user, instance, bucket, key, cluster, dataset)
   - **Requirements**: Use clear, specific requirements (mfa_enabled, public_access_blocked, encryption_enabled)
   - **NO vague verbs**: check, validate, verify, inspect, audit
   - **Focus on state**: Describe desired secure state, not the action

4. **CONSOLIDATION RULES (MANDATORY)**:
   - **Similar functions MUST be consolidated**: If multiple functions check the same thing, consolidate into ONE
   - **Cross-service functions**: If a requirement applies to multiple services, create ONE generic function
   - **Examples of what to consolidate**:
     - Multiple "MFA" functions → ONE `user_mfa_enabled`
     - Multiple "TLS version" functions → ONE `minimum_tls_version_12`
     - Multiple "public access" functions → ONE `public_access_restricted`

5. **COVERAGE ASSESSMENT (FINAL CHECK)**:
   - After mapping existing functions AND suggesting new functions, assess overall coverage
   - Consider THREE categories for complete coverage:
     a) Existing functions mapped from database
     b) Unmapped potential functions from database that could cover gaps
     c) New functions proposed to fill remaining gaps
   - 10 = Complete coverage (all three categories combined cover ALL requirements)
   - 7-9 = High coverage (three categories combined cover most requirements, minor gaps)
   - 4-6 = Medium coverage (three categories combined cover some requirements, significant gaps)
   - 1-3 = Low coverage (three categories combined cover few requirements, major gaps)
   - Goal: Ensure the combination of all three categories provides comprehensive compliance coverage

## RESPONSE FORMAT (JSON ONLY):
{{
    "compliance_id": "{compliance_item.id}",
    "title": "{compliance_item.title}",
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
    "coverage_assessment": 7,
    "new_functions_needed": [
        {{
            "function_name": "service_resource_requirement_qualifier",
            "description": "One-line description of what this function checks",
            "gcp_api_example": "gcloud service resource get --project=PROJECT_ID",
            "service_category": "Identity|Compute|Storage|Network|Security|Monitoring|Organization"
        }}
    ],
    "mapping_notes": "Technical explanation of mapping decisions, consolidation benefits, and naming optimizations"
}}

## QUALITY REQUIREMENTS:
- **Function names MUST be in snake_case format**
- **Functions MUST be implementable with real GCP APIs (gcloud, REST API)**
- **Service field MUST match GCP service names (iam, compute, storage, kms, etc.)**
- **Be specific and conservative in suggestions**
- **NO over-engineering or unnecessary complexity**

## MAPPING APPROACH:
1. FIRST: Try to map existing functions that can cover this compliance
2. SECOND: If gaps remain, consolidate into ONE function (existing or new) - NO EXCEPTIONS
3. THIRD: Assess final coverage - do we need additional functions?
4. GOAL: Maximum coverage with minimum function count

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
                # Analyze existing functions first
                potential_existing_functions = self.analyze_existing_functions_for_compliance(compliance_item)
                
                # Create high-quality prompt
                prompt = self.create_mapping_prompt(compliance_item, potential_existing_functions)
                
                # Check prompt length to avoid token issues
                estimated_tokens = len(prompt.split()) * 1.3  # Rough token estimation
                if estimated_tokens > 6000:  # Leave room for response
                    logger.warning(f"Prompt too long ({estimated_tokens:.0f} estimated tokens) for {compliance_item.id}, truncating...")
                    # Truncate the prompt
                    prompt = prompt[:4000] + "\n\n[Prompt truncated for token efficiency]"
                
                # Add rate limiting to prevent 429 errors
                time.sleep(5)  # 5 second delay between requests to avoid rate limiting
                
                response = self.client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are a GCP security expert specializing in compliance and security functions. Always respond with valid JSON only. Be conservative and accurate in your mappings."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.2,  # Slightly higher temperature for better coverage discovery
                    max_tokens=600,  # Reduced tokens to avoid context length issues
                    top_p=0.3,       # Allow more variety in function selection
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
                            # Calculate intelligent coverage score
                            existing_functions = result_data['existing_functions_mapped']
                            new_functions = result_data['new_functions_needed']
                            intelligent_coverage = self._calculate_intelligent_coverage(existing_functions, new_functions, compliance_item)
                            
                            # Create MappingResult with intelligent coverage
                            # Check for unmapped potential functions
                            potential_existing = self.analyze_existing_functions_for_compliance(compliance_item)
                            unmapped_potential = [f for f in potential_existing if f not in existing_functions]
                            
                            coverage_note = f"""Coverage Analysis:
- Coverage Score: {intelligent_coverage}/10
- Existing Functions Mapped: {len(existing_functions)} ({', '.join(existing_functions) if existing_functions else 'None'})
- Unmapped Potential Functions: {len(unmapped_potential)} ({', '.join(unmapped_potential[:3]) if unmapped_potential else 'None'}{'...' if len(unmapped_potential) > 3 else ''})
- New Functions Proposed: {len(new_functions)} ({', '.join([f['function_name'] for f in new_functions]) if new_functions else 'None'})

Total Coverage: The combination of mapped existing functions + unmapped potential functions + new proposed functions should provide comprehensive compliance coverage."""
                            
                            updated_mapping_notes = f"{result_data['mapping_notes']}\n\n{coverage_note}"
                            
                            mapping_result = MappingResult(
                                compliance_id=result_data['compliance_id'],
                                title=result_data['title'],
                                existing_functions_mapped=result_data['existing_functions_mapped'],
                                functions_to_rename=result_data.get('functions_to_rename', []),
                                functions_to_consolidate=result_data.get('functions_to_consolidate', []),
                                coverage_assessment=intelligent_coverage,
                                new_functions_needed=result_data['new_functions_needed'],
                                mapping_notes=updated_mapping_notes
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
        
        # Create a fallback result with basic information
        fallback_coverage = self._calculate_intelligent_coverage([], [], compliance_item)
        fallback_result = MappingResult(
            compliance_id=compliance_item.id,
            title=compliance_item.title,
            existing_functions_mapped=[],
            functions_to_rename=[],
            functions_to_consolidate=[],
            coverage_assessment=fallback_coverage,
            new_functions_needed=[],
            mapping_notes=f"Failed to process due to API errors. Coverage score {fallback_coverage}/10 calculated based on basic analysis."
        )
        
        return fallback_result
    
    def _validate_mapping_quality(self, result_data: Dict[str, Any], compliance_item: ComplianceItem) -> bool:
        """Validate the quality of the mapping result"""
        
        # Check if mapped functions actually exist in our database
        mapped_functions = result_data.get('existing_functions_mapped', [])
        invalid_functions = [f for f in mapped_functions if f not in self.all_function_names]
        
        if invalid_functions:
            logger.warning(f"Invalid functions suggested: {invalid_functions}")
            return False
        
        # Validate coverage assessment values (1-10 scale)
        coverage_score = result_data.get('coverage_assessment')
        if not isinstance(coverage_score, int) or coverage_score < 1 or coverage_score > 10:
            logger.warning(f"Invalid coverage assessment: {coverage_score}. Must be integer 1-10.")
            return False
        
        # Check new functions format
        new_functions = result_data.get('new_functions_needed', [])
        for func in new_functions:
            if not isinstance(func, dict):
                return False
            required_func_fields = ['function_name', 'description', 'gcp_api_example', 'service_category']
            if not all(field in func for field in required_func_fields):
                logger.warning(f"New function missing required fields: {func}")
                return False
            
            # Validate function name format (snake_case)
            func_name = func.get('function_name', '')
            if not func_name.islower() or not all(c.isalnum() or c == '_' for c in func_name):
                logger.warning(f"Invalid function name format: {func_name}")
                return False
        
        return True
    
    def _calculate_intelligent_coverage(self, existing_functions: List[str], new_functions: List[Dict], compliance_item: ComplianceItem) -> int:
        """Calculate intelligent coverage score based on comprehensive function analysis"""
        
        # Analyze compliance requirements
        compliance_text = f"{compliance_item.title} {compliance_item.description}".lower()
        
        # Check if we have existing functions that could cover this (even if not mapped)
        potential_existing_functions = self.analyze_existing_functions_for_compliance(compliance_item)
        
        # Calculate coverage components
        existing_mapped_score = 0
        unmapped_potential_score = 0
        new_functions_score = 0
        
        # 1. Score for existing functions mapped (max 4 points)
        if existing_functions:
            for func in existing_functions:
                if func in self.all_function_names:
                    # Check relevance to compliance requirement
                    relevance = self._calculate_function_relevance(func, compliance_text)
                    existing_mapped_score += relevance
            existing_mapped_score = min(4, existing_mapped_score)
        
        # 2. Score for unmapped potential functions (max 3 points)
        unmapped_potential = [f for f in potential_existing_functions if f not in existing_functions]
        if unmapped_potential:
            # These functions exist but weren't mapped - they could fill gaps
            unmapped_potential_score = min(3, len(unmapped_potential) * 0.8)
        
        # 3. Score for new functions proposed (max 3 points)
        if new_functions:
            # Assess quality and completeness of new function suggestions
            new_functions_score = min(3, len(new_functions) * 1.0)
        
        # Calculate total coverage score
        total_score = existing_mapped_score + unmapped_potential_score + new_functions_score
        
        # Normalize to 1-10 scale
        if total_score >= 8:
            return 10  # Complete coverage
        elif total_score >= 6:
            return 8   # High coverage
        elif total_score >= 4:
            return 6   # Medium coverage
        elif total_score >= 2:
            return 4   # Low-medium coverage
        else:
            return 2   # Low coverage
    
    def _calculate_function_relevance(self, function_name: str, compliance_text: str) -> float:
        """Calculate how relevant a function is to a compliance requirement"""
        
        func_lower = function_name.lower()
        relevance_score = 0.0
        
        # IAM and Identity Management (more comprehensive matching)
        if any(term in compliance_text for term in ['iam', 'identity', 'authentication', 'authorization', 'user', 'mfa', 'security key', 'service account', 'corporate', 'consumer']):
            if any(keyword in func_lower for keyword in ['iam', 'user', 'mfa', 'security', 'authentication', 'authorization', 'service_account', 'corporate', 'consumer', 'account']):
                relevance_score += 1.0
        
        # Compute Services (more comprehensive matching)
        if any(term in compliance_text for term in ['compute', 'gke', 'cloud run', 'app engine', 'vm', 'instance', 'container', 'kubernetes']):
            if any(keyword in func_lower for keyword in ['compute', 'gke', 'cloud_run', 'app_engine', 'vm', 'instance', 'container', 'kubernetes']):
                relevance_score += 1.0
        
        # Storage Services (more comprehensive matching)
        if any(term in compliance_text for term in ['storage', 'bigquery', 'cloud sql', 'bucket', 'dataset', 'database', 'data']):
            if any(keyword in func_lower for keyword in ['storage', 'bigquery', 'cloud_sql', 'bucket', 'dataset', 'database', 'data']):
                relevance_score += 1.0
        
        # Networking (more comprehensive matching)
        if any(term in compliance_text for term in ['vpc', 'firewall', 'subnet', 'network', 'traffic', 'access', 'public', 'private']):
            if any(keyword in func_lower for keyword in ['vpc', 'firewall', 'subnet', 'network', 'traffic', 'access', 'public', 'private']):
                relevance_score += 1.0
        
        # Security Services (more comprehensive matching)
        if any(term in compliance_text for term in ['kms', 'encryption', 'key', 'security center', 'security', 'compliance', 'audit']):
            if any(keyword in func_lower for keyword in ['kms', 'encryption', 'key', 'security', 'compliance', 'audit']):
                relevance_score += 1.0
        
        # Monitoring and Logging (more comprehensive matching)
        if any(term in compliance_text for term in ['logging', 'monitoring', 'audit', 'trace', 'log', 'event', 'activity']):
            if any(keyword in func_lower for keyword in ['logging', 'monitoring', 'audit', 'trace', 'log', 'event', 'activity']):
                relevance_score += 1.0
        
        # Additional relevance for partial matches
        if any(word in func_lower for word in compliance_text.split() if len(word) > 3):
            relevance_score += 0.5
        
        return relevance_score
    
    def process_compliance_framework(self, compliance_items: List[ComplianceItem], batch_size: int = 5) -> List[MappingResult]:
        """Process all compliance items and generate mapping results"""
        results = []
        
        # Process in batches
        for i in range(0, len(compliance_items), batch_size):
            batch = compliance_items[i:i + batch_size]
            logger.info(f"Processing batch {i//batch_size + 1}/{(len(compliance_items)-1)//batch_size + 1}")
            
            for item in batch:
                logger.info(f"Processing compliance item: {item.id}")
                
                try:
                    result = self.map_compliance_item(item)
                    
                    if result is None:
                        logger.warning(f"Failed to map compliance item: {item.id}")
                        continue
                    
                    results.append(result)
                    
                    # Rate limiting
                    time.sleep(1)
                    
                except Exception as e:
                    logger.error(f"Error processing {item.id}: {e}")
                    continue
        
        return results
    
    def save_results(self, results: List[MappingResult], timestamp: str):
        """Save mapping results to output files"""
        
        # Save comprehensive results
        output_file = self.output_dir / "updated_compliance" / f"gcp_mapping_results_{timestamp}.json"
        with open(output_file, 'w') as f:
            json.dump([result.__dict__ for result in results], f, indent=2)
        logger.info(f"Saved comprehensive results to {output_file}")
        
        # Save new functions needed
        new_functions = []
        for result in results:
            new_functions.extend(result.new_functions_needed)
        
        if new_functions:
            new_functions_file = self.output_dir / "new_functions" / f"gcp_new_functions_{timestamp}.json"
            with open(new_functions_file, 'w') as f:
                json.dump(new_functions, f, indent=2)
            logger.info(f"Saved {len(new_functions)} new functions to {new_functions_file}")
        
        # Save functions to rename
        rename_functions = []
        for result in results:
            rename_functions.extend(result.functions_to_rename)
        
        if rename_functions:
            rename_file = self.output_dir / "updated_functions" / f"gcp_rename_functions_{timestamp}.json"
            with open(rename_file, 'w') as f:
                json.dump(rename_functions, f, indent=2)
            logger.info(f"Saved {len(rename_functions)} rename suggestions to {rename_file}")
        
        # Generate summary report with coverage breakdown
        coverage_breakdown = {
            "10 (Complete)": len([r for r in results if r.coverage_assessment == 10]),
            "7-9 (High)": len([r for r in results if 7 <= r.coverage_assessment <= 9]),
            "4-6 (Medium)": len([r for r in results if 4 <= r.coverage_assessment <= 6]),
            "1-3 (Low)": len([r for r in results if 1 <= r.coverage_assessment <= 3])
        }
        
        avg_coverage = sum(r.coverage_assessment for r in results) / len(results) if results else 0
        
        summary = {
            "total_compliance_items": len(results),
            "average_coverage_score": round(avg_coverage, 2),
            "coverage_breakdown": coverage_breakdown,
            "total_new_functions_needed": len(new_functions),
            "total_rename_suggestions": len(rename_functions),
            "timestamp": timestamp
        }
        
        summary_file = self.output_dir / f"gcp_mapping_summary_{timestamp}.json"
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        logger.info(f"Saved summary to {summary_file}")
        
        return summary
    
    def run_mapping(self, gcp_file: str, compliance_file: str, max_items: int = None, test_mode: bool = False):
        """Run the complete mapping process"""
        if test_mode:
            print("🧪 TEST MODE ENABLED - Processing limited items for validation")
            print("="*60)
        else:
            print("🚀 PRODUCTION MODE - Processing all compliance items")
            print("="*60)
        
        logger.info("Starting GCP compliance mapping process...")
        
        # Load data
        if not self.load_gcp_database(gcp_file):
            logger.error("Failed to load GCP database")
            return
        
        compliance_items = self.load_compliance_framework(compliance_file)
        if not compliance_items:
            logger.error("Failed to load compliance framework")
            return
        
        # Limit items for testing if specified
        if max_items:
            compliance_items = compliance_items[:max_items]
            if test_mode:
                print(f"✅ Testing with first {len(compliance_items)} compliance items")
                print(f"   This allows you to validate the mapping quality before full run")
            else:
                logger.info(f"Limited to first {len(compliance_items)} compliance items")
        
        # Process compliance items
        results = self.process_compliance_framework(compliance_items)
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        summary = self.save_results(results, timestamp)
        
        # Print summary
        print("\n" + "="*60)
        if test_mode:
            print("🧪 GCP COMPLIANCE MAPPING TEST COMPLETE")
        else:
            print("🚀 GCP COMPLIANCE MAPPING COMPLETE")
        print("="*60)
        print(f"Total compliance items processed: {summary['total_compliance_items']}")
        print(f"Average coverage score: {summary['average_coverage_score']}/10")
        print("\nCoverage Breakdown:")
        for coverage_range, count in summary['coverage_breakdown'].items():
            print(f"  {coverage_range}: {count} items")
        print(f"\nNew functions needed: {summary['total_new_functions_needed']}")
        print(f"Rename suggestions: {summary['total_rename_suggestions']}")
        print(f"Results saved to: {self.output_dir}")
        
        if test_mode:
            print("\n📋 NEXT STEPS:")
            print("   1. Review the mapping results in output/ directory")
            print("   2. Validate function suggestions and naming quality")
            print("   3. If satisfied, run without --test flag for full compliance framework")
            print("   4. Example: python gcp_compliance_mapper.py input.json compliance.json")
        
        print("="*60)

def main():
    """Main function"""
    if len(sys.argv) < 3:
        print("Usage: python gcp_compliance_mapper.py <gcp_functions_file> <compliance_file> [--test] [max_items]")
        print("\nExamples:")
        print("  # Test mode with 15 items")
        print("  python gcp_compliance_mapper.py gcp_functions.json compliance.json --test 15")
        print("\n  # Production mode - all items")
        print("  python gcp_compliance_mapper.py gcp_functions.json compliance.json")
        print("\n  # Limited items without test mode")
        print("  python gcp_compliance_mapper.py gcp_functions.json compliance.json 20")
        sys.exit(1)
    
    gcp_file = sys.argv[1]
    compliance_file = sys.argv[2]
    
    # Parse arguments
    test_mode = False
    max_items = None
    
    for arg in sys.argv[3:]:
        if arg == "--test":
            test_mode = True
        elif arg.isdigit():
            max_items = int(arg)
        else:
            print(f"Error: Unknown argument: {arg}")
            print("Use --test for test mode, or a number for max items")
            sys.exit(1)
    
    # Check if files exist
    if not os.path.exists(gcp_file):
        print(f"Error: GCP functions file not found: {gcp_file}")
        sys.exit(1)
    
    if not os.path.exists(compliance_file):
        print(f"Error: Compliance file not found: {compliance_file}")
        sys.exit(1)
    
    # Initialize and run mapper
    mapper = GCPComplianceMapper()
    mapper.run_mapping(gcp_file, compliance_file, max_items, test_mode)

if __name__ == "__main__":
    main()
