#!/usr/bin/env python3
"""
GCP NIST Compliance Function Mapping Tool - COMBINED VERSION

This tool:
1. Maps existing security functions from gcp_consolidated_function_database.json to NIST controls
2. Suggests new functions where gaps exist
3. Suggests function renames for clarity
4. Automatically updates the GCP function database with new functions and renames
5. Creates all output files in one run

All in a single, efficient script!
"""

import json
import os
import sys
import time
import shutil
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
        logging.FileHandler('gcp_nist_compliance_mapping_combined.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class NISTControl:
    """Represents a single NIST control"""
    control_id: str
    title: str
    control: Dict[str, Any]
    discussion: str
    related_controls: List[str]
    control_enhancements: List[str]
    references: List[str]
    function_names: List[str]

@dataclass
class MappingResult:
    """Represents the result of mapping a NIST control to functions"""
    control_id: str
    title: str
    existing_functions_mapped: List[str]
    functions_to_rename: List[Dict[str, str]]  # Functions to rename for clarity
    functions_to_consolidate: List[Dict[str, Any]]  # Functions to consolidate for efficiency
    coverage_assessment: int  # 1-10 scale (1=no coverage, 10=complete coverage)
    new_functions_needed: List[Dict[str, str]]
    mapping_notes: str

class GCPNISTComplianceMapperCombined:
    """Main class for mapping NIST controls to GCP security functions AND updating database"""
    
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
        
        # Create all output directories
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)
        
        # Create subdirectories
        (self.output_dir / "updated_compliance").mkdir(exist_ok=True)
        (self.output_dir / "new_functions").mkdir(exist_ok=True)
        (self.output_dir / "updated_functions").mkdir(exist_ok=True)
        
        # Create updated database directory under output
        self.updated_db_dir = self.output_dir / "updated fn database"
        self.updated_db_dir.mkdir(exist_ok=True)
        
    def load_gcp_database(self, gcp_file: str) -> bool:
        """Load the GCP function database"""
        try:
            with open(gcp_file, 'r') as f:
                data = json.load(f)
            
            # GCP functions are stored as a list of objects with function_name field
            if isinstance(data, list):
                self.gcp_functions = {"GCP_Functions": data}
                
                # Extract function names from objects
                for func in data:
                    if isinstance(func, dict) and 'function_name' in func:
                        self.all_function_names.add(func['function_name'])
                
                logger.info(f"Loaded {len(self.all_function_names)} functions from GCP database")
                return True
            else:
                logger.error("GCP database should be a list of function objects")
                return False
                
        except FileNotFoundError:
            logger.error(f"GCP database file not found: {gcp_file}")
            return False
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing GCP database JSON: {e}")
            return False
    
    def load_nist_controls(self, nist_file: str) -> List[NISTControl]:
        """Load NIST controls from JSON file"""
        try:
            with open(nist_file, 'r') as f:
                data = json.load(f)
            
            nist_controls = []
            for item in data:
                if isinstance(item, dict) and 'control_id' in item:
                    control = NISTControl(
                        control_id=item.get('control_id', ''),
                        title=item.get('title', ''),
                        control=item.get('control', {}),
                        discussion=item.get('discussion', ''),
                        related_controls=item.get('related_controls', []),
                        control_enhancements=item.get('control_enhancements', []),
                        references=item.get('references', []),
                        function_names=item.get('function_names', [])
                    )
                    nist_controls.append(control)
            
            logger.info(f"Loaded {len(nist_controls)} NIST controls")
            return nist_controls
            
        except FileNotFoundError:
            logger.error(f"NIST controls file not found: {nist_file}")
            return []
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing NIST controls JSON: {e}")
            return []
    
    def analyze_existing_functions_for_control(self, control: NISTControl) -> List[str]:
        """Analyze existing functions to find potential matches for NIST control"""
        potential_matches = []
        
        # Keywords from control
        control_text = f"{control.title} {control.discussion}".lower()
        
        # Extract key terms based on GCP services
        key_terms = []
        
        # IAM and Identity Management
        if any(term in control_text for term in ["iam", "identity", "authentication", "authorization", "service account", "mfa", "security key"]):
            key_terms.extend(["iam", "identity", "authentication", "authorization", "service_account", "mfa", "security_key"])
        
        # Compute Services
        if any(term in control_text for term in ["compute", "gke", "cloud run", "app engine", "cloud functions", "vm", "instance"]):
            key_terms.extend(["compute", "gke", "cloud_run", "app_engine", "cloud_functions", "vm", "instance"])
        
        # Storage Services
        if any(term in control_text for term in ["storage", "bigquery", "cloud sql", "spanner", "firestore", "bucket", "dataset"]):
            key_terms.extend(["storage", "bigquery", "cloud_sql", "spanner", "firestore", "bucket", "dataset"])
        
        # Networking
        if any(term in control_text for term in ["vpc", "firewall", "subnet", "load balancer", "cloud armor", "cdn", "interconnect"]):
            key_terms.extend(["vpc", "firewall", "subnet", "load_balancer", "cloud_armor", "cdn", "interconnect"])
        
        # Security Services
        if any(term in control_text for term in ["kms", "security center", "access context", "binary authorization", "assured workloads"]):
            key_terms.extend(["kms", "security_center", "access_context", "binary_authorization", "assured_workloads"])
        
        # Monitoring and Logging
        if any(term in control_text for term in ["logging", "monitoring", "trace", "error reporting", "profiler", "debugger"]):
            key_terms.extend(["logging", "monitoring", "trace", "error_reporting", "profiler", "debugger"])
        
        # Organization and Policies
        if any(term in control_text for term in ["organization", "policy", "resource manager", "billing", "quotas"]):
            key_terms.extend(["organization", "policy", "resource_manager", "billing", "quotas"])
        
        # Encryption and Keys
        if any(term in control_text for term in ["encryption", "cmek", "kms", "key", "certificate", "tls", "ssl"]):
            key_terms.extend(["encryption", "cmek", "kms", "key", "certificate", "tls", "ssl"])
        
        # Search for functions that match key terms
        for func_name in self.all_function_names:
            func_lower = func_name.lower()
            if any(term in func_lower for term in key_terms):
                potential_matches.append(func_name)
        
        return potential_matches
    
    def create_mapping_prompt(self, control: NISTControl, potential_existing_functions: List[str]) -> str:
        """Create high-quality AI prompt for mapping NIST controls"""
        
        # Get available function names as context - limit to avoid token overflow
        available_functions = list(self.all_function_names)
        # Limit to 25 functions to stay well within token limits
        functions_text = "\n".join([f"- {func}" for func in sorted(available_functions)[:25]])
        
        prompt = f"""
You are a GCP security expert working with a CSMP tool. You have access to an existing function database with {len(self.all_function_names)} GCP security check functions in snake_case format.

## TASK:
Map the following NIST control to existing functions and suggest new ones where gaps exist, following STRICT quality standards.

## NIST CONTROL:
- **Control ID**: {control.control_id}
- **Title**: {control.title}
- **Discussion**: {control.discussion[:500]}...
- **Related Controls**: {', '.join(control.related_controls)}

## EXISTING FUNCTIONS DATABASE (Sample):
{functions_text}
... and {len(self.all_function_names) - 25} more functions

## POTENTIAL MATCHES FOUND:
{chr(10).join([f"- {func}" for func in potential_existing_functions[:10]])}

## REQUIREMENTS:
1. **Function Names**: Must be in snake_case format with GCP service prefixes (e.g., gke_, iam_, storage_, compute_)
2. **Executable**: Must be implementable using GCP APIs (gcloud, Python client libraries, REST APIs)
3. **No Manual Processes**: Do not suggest policy, documentation, procedures, training, or manual processes
4. **Specific**: Focus on technical security controls that can be automated
5. **GCP-Specific**: Use GCP services and APIs, not generic cloud concepts

## OUTPUT FORMAT (JSON):
{{
    "existing_functions_mapped": ["function1", "function2"],
    "functions_to_rename": [
        {{"old_name": "old_function", "new_name": "new_function", "reason": "reason"}}
    ],
    "functions_to_consolidate": [
        {{"functions": ["func1", "func2"], "consolidated_name": "new_name", "reason": "reason"}}
    ],
    "coverage_assessment": 8,
    "new_functions_needed": [
        {{
            "function_name": "gke_cluster_encryption_at_rest",
            "description": "Check if GKE clusters have encryption at rest enabled",
            "gcp_sdk_example": "gcloud container clusters describe CLUSTER_NAME --zone=ZONE --format='value(masterAuth.clusterCaCertificate)'"
        }}
    ],
    "mapping_notes": "Detailed explanation of mapping decisions"
}}

## IMPORTANT:
- Coverage assessment: 1-10 scale (1=no coverage, 10=complete coverage)
- Only suggest functions that can be implemented with GCP APIs
- Focus on technical security controls, not policy/procedures
- Ensure function names follow GCP service naming conventions
"""
        return prompt
    
    def call_openai_api(self, prompt: str) -> Optional[Dict[str, Any]]:
        """Call OpenAI API with rate limiting"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a GCP security expert specializing in compliance mapping and security controls."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=2000
            )
            
            # Rate limiting
            time.sleep(2)
            
            content = response.choices[0].message.content
            return json.loads(content)
            
        except Exception as e:
            logger.error(f"OpenAI API call failed: {e}")
            return None
    
    def process_nist_control(self, control: NISTControl) -> MappingResult:
        """Process a single NIST control"""
        logger.info(f"Processing NIST control: {control.control_id}")
        
        # Analyze existing functions
        potential_functions = self.analyze_existing_functions_for_control(control)
        
        # Create AI prompt
        prompt = self.create_mapping_prompt(control, potential_functions)
        
        # Call OpenAI API
        result = self.call_openai_api(prompt)
        
        if result:
            return MappingResult(
                control_id=control.control_id,
                title=control.title,
                existing_functions_mapped=result.get('existing_functions_mapped', []),
                functions_to_rename=result.get('functions_to_rename', []),
                functions_to_consolidate=result.get('functions_to_consolidate', []),
                coverage_assessment=result.get('coverage_assessment', 1),
                new_functions_needed=result.get('new_functions_needed', []),
                mapping_notes=result.get('mapping_notes', '')
            )
        else:
            # Fallback result
            return MappingResult(
                control_id=control.control_id,
                title=control.title,
                existing_functions_mapped=potential_functions[:3],
                functions_to_rename=[],
                functions_to_consolidate=[],
                coverage_assessment=3,
                new_functions_needed=[],
                mapping_notes="API call failed, using fallback mapping"
            )
    
    def process_nist_controls(self, controls: List[NISTControl]) -> List[MappingResult]:
        """Process all NIST controls"""
        results = []
        
        for i, control in enumerate(controls, 1):
            logger.info(f"Processing control {i}/{len(controls)}: {control.control_id}")
            result = self.process_nist_control(control)
            results.append(result)
            
            # Progress update
            if i % 10 == 0:
                logger.info(f"Progress: {i}/{len(controls)} controls processed")
        
        return results
    
    def save_mapping_results(self, results: List[MappingResult], timestamp: str) -> Dict[str, Any]:
        """Save mapping results to files"""
        
        # Save updated compliance items
        updated_controls = []
        for result in results:
            control_data = {
                "control_id": result.control_id,
                "title": result.title,
                "function_names": result.existing_functions_mapped,
                "mapping_result": {
                    "coverage_assessment": result.coverage_assessment,
                    "new_functions_needed": result.new_functions_needed,
                    "functions_to_rename": result.functions_to_rename,
                    "functions_to_consolidate": result.functions_to_consolidate,
                    "mapping_notes": result.mapping_notes
                }
            }
            updated_controls.append(control_data)
        
        updated_file = self.output_dir / "updated_compliance" / f"nist_controls_updated_{timestamp}.json"
        with open(updated_file, 'w') as f:
            json.dump(updated_controls, f, indent=2)
        
        # Save new functions
        all_new_functions = []
        for result in results:
            all_new_functions.extend(result.new_functions_needed)
        
        if all_new_functions:
            new_functions_file = self.output_dir / "new_functions" / f"gcp_new_functions_{timestamp}.json"
            with open(new_functions_file, 'w') as f:
                json.dump(all_new_functions, f, indent=2)
        
        # Save rename suggestions
        all_renames = []
        for result in results:
            all_renames.extend(result.functions_to_rename)
        
        if all_renames:
            renames_file = self.output_dir / "updated_functions" / f"gcp_rename_functions_{timestamp}.json"
            with open(renames_file, 'w') as f:
                json.dump(all_renames, f, indent=2)
        
        # Calculate summary statistics
        total_controls = len(results)
        total_new_functions = len(all_new_functions)
        total_renames = len(all_renames)
        avg_coverage = sum(r.coverage_assessment for r in results) / total_controls if total_controls > 0 else 0
        
        coverage_breakdown = {}
        for result in results:
            score = result.coverage_assessment
            if score <= 2:
                range_key = "1-2 (Poor)"
            elif score <= 4:
                range_key = "3-4 (Fair)"
            elif score <= 6:
                range_key = "5-6 (Good)"
            elif score <= 8:
                range_key = "7-8 (Very Good)"
            else:
                range_key = "9-10 (Excellent)"
            
            coverage_breakdown[range_key] = coverage_breakdown.get(range_key, 0) + 1
        
        summary = {
            "total_controls": total_controls,
            "average_coverage_score": round(avg_coverage, 2),
            "total_new_functions_needed": total_new_functions,
            "total_rename_suggestions": total_renames,
            "coverage_breakdown": coverage_breakdown,
            "files_created": {
                "updated_controls": str(updated_file),
                "new_functions": str(new_functions_file) if all_new_functions else None,
                "rename_suggestions": str(renames_file) if all_renames else None
            }
        }
        
        # Save summary
        summary_file = self.output_dir / f"mapping_summary_{timestamp}.json"
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        return summary
    
    def update_gcp_database(self, timestamp: str) -> Dict[str, Any]:
        """Update the GCP function database with mapping results"""
        
        # File paths
        original_db = "gcp_consolidated_function_database.json"
        
        # Load original database
        logger.info("Loading original GCP function database...")
        with open(original_db, 'r') as f:
            original_data = json.load(f)
        
        original_count = len(original_data)
        logger.info(f"Original database has {original_count} functions")
        
        # Create backup
        backup_file = self.updated_db_dir / f"gcp_consolidated_function_database_backup_{timestamp}.json"
        shutil.copy2(original_db, backup_file)
        logger.info(f"Created backup: {backup_file}")
        
        # Load new functions
        new_functions_file = self.output_dir / "new_functions" / f"gcp_new_functions_{timestamp}.json"
        new_functions = []
        if new_functions_file.exists():
            logger.info(f"Loading new functions from: {new_functions_file}")
            with open(new_functions_file, 'r') as f:
                new_functions = json.load(f)
            logger.info(f"Loaded {len(new_functions)} new functions")
        
        # Load rename suggestions
        rename_functions_file = self.output_dir / "updated_functions" / f"gcp_rename_functions_{timestamp}.json"
        rename_functions = []
        if rename_functions_file.exists():
            logger.info(f"Loading rename suggestions from: {rename_functions_file}")
            with open(rename_functions_file, 'r') as f:
                rename_functions = json.load(f)
            logger.info(f"Loaded {len(rename_functions)} rename suggestions")
        
        # Apply renames first
        if rename_functions:
            logger.info("Applying function renames...")
            rename_map = {}
            for rename_item in rename_functions:
                old_name = rename_item.get('old_name', '')
                new_name = rename_item.get('new_name', '')
                if old_name and new_name:
                    rename_map[old_name] = new_name
            
            # Apply renames to existing functions
            renamed_count = 0
            for func in original_data:
                if func.get('function_name') in rename_map:
                    func['function_name'] = rename_map[func['function_name']]
                    renamed_count += 1
            
            logger.info(f"Renamed {renamed_count} functions")
        
        # Add new functions
        if new_functions:
            logger.info("Adding new functions...")
            
            # Convert new functions to match database format
            for new_func in new_functions:
                # Create function entry in database format
                db_func = {
                    "function_name": new_func.get('function_name', ''),
                    "description": new_func.get('description', ''),
                    "service_category": "security",  # Default category
                    "gcp_sdk_example": new_func.get('gcp_sdk_example', ''),
                    "confidence": 0.8,  # Default confidence
                    "source": "nist_mapper",
                    "sheet": "NIST_Controls",
                    "rule_id": f"NIST_{timestamp}"
                }
                
                # Check if function already exists (by name)
                existing_names = {f.get('function_name', '') for f in original_data}
                if db_func['function_name'] not in existing_names:
                    original_data.append(db_func)
                    logger.info(f"Added new function: {db_func['function_name']}")
                else:
                    logger.warning(f"Function already exists: {db_func['function_name']}")
        
        # Save updated database
        updated_db_file = self.updated_db_dir / f"gcp_consolidated_function_database_updated_{timestamp}.json"
        with open(updated_db_file, 'w') as f:
            json.dump(original_data, f, indent=2)
        
        # Final statistics
        final_count = len(original_data)
        added_count = final_count - original_count
        
        logger.info("=" * 60)
        logger.info("DATABASE UPDATE COMPLETE")
        logger.info("=" * 60)
        logger.info(f"Original functions: {original_count}")
        logger.info(f"Final functions: {final_count}")
        logger.info(f"Functions added: {added_count}")
        logger.info(f"Functions renamed: {len(rename_functions) if rename_functions else 0}")
        logger.info(f"Backup saved: {backup_file}")
        logger.info(f"Updated database: {updated_db_file}")
        
        # Save update summary
        update_summary = {
            "timestamp": timestamp,
            "original_count": original_count,
            "final_count": final_count,
            "functions_added": added_count,
            "functions_renamed": len(rename_functions) if rename_functions else 0,
            "backup_file": str(backup_file),
            "updated_database": str(updated_db_file),
            "new_functions_source": str(new_functions_file) if new_functions else None,
            "rename_suggestions_source": str(rename_functions_file) if rename_functions else None
        }
        
        update_summary_file = self.updated_db_dir / f"update_summary_{timestamp}.json"
        with open(update_summary_file, 'w') as f:
            json.dump(update_summary, f, indent=2)
        
        return update_summary
    
    def run_complete_mapping_and_update(self, gcp_file: str, nist_file: str, max_controls: int = None, test_mode: bool = False):
        """Run the complete NIST compliance mapping AND database update process"""
        
        if test_mode:
            print("🧪 TEST MODE ENABLED - Processing limited controls for validation")
            print("=" * 60)
        
        logger.info("Starting GCP NIST compliance mapping AND database update process...")
        
        # Load data
        if not self.load_gcp_database(gcp_file):
            logger.error("Failed to load GCP database")
            return
        
        nist_controls = self.load_nist_controls(nist_file)
        if not nist_controls:
            logger.error("Failed to load NIST controls")
            return
        
        # Limit controls for testing if specified
        if max_controls:
            nist_controls = nist_controls[:max_controls]
            if test_mode:
                print(f"✅ Testing with first {len(nist_controls)} NIST controls")
                print(f"   This allows you to validate the mapping quality before full run")
            else:
                logger.info(f"Limited to first {len(nist_controls)} NIST controls")
        
        # Process NIST controls
        results = self.process_nist_controls(nist_controls)
        
        # Save mapping results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        mapping_summary = self.save_mapping_results(results, timestamp)
        
        # Update GCP database
        logger.info("🔄 Updating GCP function database...")
        update_summary = self.update_gcp_database(timestamp)
        
        # Print final summary
        print("\n" + "="*60)
        if test_mode:
            print("🧪 GCP NIST COMPLIANCE MAPPING + DATABASE UPDATE TEST COMPLETE")
        else:
            print("🚀 GCP NIST COMPLIANCE MAPPING + DATABASE UPDATE COMPLETE")
        print("="*60)
        print(f"Total NIST controls processed: {mapping_summary['total_controls']}")
        print(f"Average coverage score: {mapping_summary['average_coverage_score']}/10")
        print("\nCoverage Breakdown:")
        for coverage_range, count in mapping_summary['coverage_breakdown'].items():
            print(f"  {coverage_range}: {count} controls")
        print(f"\nNew functions needed: {mapping_summary['total_new_functions_needed']}")
        print(f"Rename suggestions: {mapping_summary['total_rename_suggestions']}")
        print(f"\n📊 DATABASE UPDATE RESULTS:")
        print(f"  Functions added: {update_summary['functions_added']}")
        print(f"  Functions renamed: {update_summary['functions_renamed']}")
        print(f"  Final function count: {update_summary['final_count']}")
        print(f"\n📁 All results saved to: {self.output_dir}")
        print(f"💾 Updated database: {update_summary['updated_database']}")
        
        if test_mode:
            print("\n📋 NEXT STEPS:")
            print("   1. Review the mapping results in output/ directory")
            print("   2. Validate function suggestions and naming quality")
            print("   3. If satisfied, run without --test flag for full NIST framework")
            print("   4. Example: python gcp_nist_compliance_mapper_combined.py gcp_database.json nist_controls.json")
        
        print("="*60)

def main():
    """Main function"""
    if len(sys.argv) < 3:
        print("Usage: python gcp_nist_compliance_mapper_combined.py <gcp_functions_file> <nist_controls_file> [--test] [max_controls]")
        print("\nExamples:")
        print("  # Test mode with 10 controls")
        print("  python gcp_nist_compliance_mapper_combined.py gcp_consolidated_function_database.json nist_controls.json --test 10")
        print("\n  # Production mode - all controls")
        print("  python gcp_nist_compliance_mapper_combined.py gcp_consolidated_function_database.json nist_controls.json")
        print("\n  # Limited controls without test mode")
        print("  python gcp_nist_compliance_mapper_combined.py gcp_consolidated_function_database.json nist_controls.json 20")
        sys.exit(1)
    
    gcp_file = sys.argv[1]
    nist_file = sys.argv[2]
    
    # Parse arguments
    test_mode = False
    max_controls = None
    
    for arg in sys.argv[3:]:
        if arg == "--test":
            test_mode = True
        elif arg.isdigit():
            max_controls = int(arg)
        else:
            print(f"Error: Unknown argument: {arg}")
            print("Use --test for test mode, or a number for max controls")
            sys.exit(1)
    
    # Check if files exist
    if not os.path.exists(gcp_file):
        print(f"Error: GCP functions file not found: {gcp_file}")
        sys.exit(1)
    
    if not os.path.exists(nist_file):
        print(f"Error: NIST controls file not found: {nist_file}")
        sys.exit(1)
    
    # Initialize and run combined mapper
    mapper = GCPNISTComplianceMapperCombined()
    mapper.run_complete_mapping_and_update(gcp_file, nist_file, max_controls, test_mode)

if __name__ == "__main__":
    main()
