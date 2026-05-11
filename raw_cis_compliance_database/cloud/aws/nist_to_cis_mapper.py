#!/usr/bin/env python3
"""
NIST to CIS Schema Mapper
Maps NIST control data to CIS-like schema format for CSPM systems
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional


class NISTToCISMapper:
    """Transform NIST controls to CIS-like schema"""
    
    # Profile applicability mapping based on control families
    PROFILE_MAPPING = {
        'AC': '• Level 1',  # Access Control
        'AT': '• Level 1',  # Awareness and Training
        'AU': '• Level 1',  # Audit and Accountability
        'CA': '• Level 2',  # Assessment, Authorization, and Monitoring
        'CM': '• Level 1',  # Configuration Management
        'CP': '• Level 2',  # Contingency Planning
        'IA': '• Level 1',  # Identification and Authentication
        'IR': '• Level 2',  # Incident Response
        'MA': '• Level 2',  # Maintenance
        'MP': '• Level 2',  # Media Protection
        'PE': '• Level 2',  # Physical and Environmental Protection
        'PL': '• Level 2',  # Planning
        'PS': '• Level 2',  # Personnel Security
        'RA': '• Level 2',  # Risk Assessment
        'SA': '• Level 2',  # System and Services Acquisition
        'SC': '• Level 1',  # System and Communications Protection
        'SI': '• Level 1',  # System and Information Integrity
        'SR': '• Level 2',  # Supply Chain Risk Management
    }
    
    # Section names for control families
    SECTION_NAMES = {
        'AC': 'Access Control',
        'AT': 'Awareness and Training',
        'AU': 'Audit and Accountability',
        'CA': 'Assessment, Authorization, and Monitoring',
        'CM': 'Configuration Management',
        'CP': 'Contingency Planning',
        'IA': 'Identification and Authentication',
        'IR': 'Incident Response',
        'MA': 'Maintenance',
        'MP': 'Media Protection',
        'PE': 'Physical and Environmental Protection',
        'PL': 'Planning',
        'PS': 'Personnel Security',
        'PT': 'Privacy',
        'RA': 'Risk Assessment',
        'SA': 'System and Services Acquisition',
        'SC': 'System and Communications Protection',
        'SI': 'System and Information Integrity',
        'SR': 'Supply Chain Risk Management',
    }
    
    def __init__(self):
        self.stats = {
            'total': 0,
            'mapped': 0,
            'skipped': 0,
            'errors': []
        }
    
    def extract_control_family(self, control_id: str) -> str:
        """Extract control family from control ID (e.g., AC-1 -> AC)"""
        if not control_id or not isinstance(control_id, str):
            return ''
        return control_id.split('-')[0] if '-' in control_id else control_id
    
    def get_section(self, control_id: str) -> str:
        """Get section name from control family"""
        family = self.extract_control_family(control_id)
        return self.SECTION_NAMES.get(family, 'Other Controls')
    
    def extract_additional_information(self, discussion: str, references: List, 
                                       control_enhancements: List) -> str:
        """Extract additional information from various fields"""
        info_parts = []
        
        # Check for specific keywords in discussion that indicate additional info
        if discussion:
            # Look for implementation notes, considerations, or exceptions
            keywords = ['note:', 'notes:', 'additional information:', 'considerations:', 
                       'exceptions:', 'implementation:', 'important:']
            
            discussion_lower = discussion.lower()
            for keyword in keywords:
                if keyword in discussion_lower:
                    # Extract the part after the keyword
                    start_idx = discussion_lower.index(keyword)
                    remaining_text = discussion[start_idx:].strip()
                    # Take up to 500 characters or until double newline
                    end_idx = remaining_text.find('\n\n')
                    if end_idx > 0:
                        info_parts.append(remaining_text[:end_idx])
                    else:
                        info_parts.append(remaining_text[:500])
        
        # Add control enhancements summary if available
        if control_enhancements:
            valid_enhancements = [e for e in control_enhancements if e and isinstance(e, dict)]
            if valid_enhancements:
                info_parts.append(f"This control has {len(valid_enhancements)} enhancement(s) available.")
        
        return " ".join(info_parts) if info_parts else ""
    
    def format_control_description(self, control: Any) -> str:
        """Format control description from various NIST formats"""
        if not control:
            return ""
        
        if isinstance(control, str):
            return control
        
        if isinstance(control, dict):
            # Handle various dict structures
            parts = []
            for key in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']:
                if key in control:
                    value = control[key]
                    if isinstance(value, str):
                        parts.append(f"{key}. {value}")
                    elif isinstance(value, dict):
                        parts.append(f"{key}. {json.dumps(value)}")
            
            if parts:
                return " ".join(parts)
            
            # Try common description fields
            for field in ['Description', 'description', 'requirements', 'control']:
                if field in control:
                    return str(control[field])
            
            return json.dumps(control)
        
        return str(control)
    
    def generate_audit_section(self, control_id: str, description: str, 
                               control_enhancements: List) -> str:
        """Generate audit procedure from control information"""
        audit_template = f"""Perform the following to verify compliance with {control_id}:

From Console:
1. Sign in to the AWS Management Console
2. Navigate to the relevant service dashboard
3. Review the configuration settings
4. Verify that the control requirements are met

From Command Line:
1. Use AWS CLI commands to check the configuration
2. Review the output for compliance with control requirements
3. Document findings

Note: Specific audit procedures should be developed based on your organization's implementation."""
        
        return audit_template
    
    def generate_remediation_section(self, control_id: str, description: str) -> str:
        """Generate remediation guidance from control information"""
        remediation_template = f"""Perform the following to remediate non-compliance with {control_id}:

From Console:
1. Sign in to the AWS Management Console
2. Navigate to the relevant service dashboard
3. Update the configuration to meet control requirements
4. Verify the changes have been applied

From Command Line:
1. Use AWS CLI commands to update the configuration
2. Verify the changes
3. Document the remediation steps taken

References should be consulted for detailed implementation guidance."""
        
        return remediation_template
    
    def map_control(self, nist_control: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Map a single NIST control to CIS format"""
        try:
            # Skip empty or invalid entries
            if not nist_control:
                return None
            
            control_id = nist_control.get('control_id') or nist_control.get('Control_ID')
            if not control_id:
                return None
            
            # Skip entries with only function_names
            if len(nist_control.keys()) == 1 and 'function_names' in nist_control:
                return None
            
            # Extract title from various possible field names
            control_name = (nist_control.get('control_name') or 
                           nist_control.get('Control_Name') or 
                           nist_control.get('title') or 
                           '')
            
            control = nist_control.get('control') or nist_control.get('Control', {})
            discussion = nist_control.get('discussion') or nist_control.get('Discussion', '')
            related_controls = nist_control.get('related_controls') or nist_control.get('Related_Controls', [])
            control_enhancements = nist_control.get('control_enhancements') or nist_control.get('Control_Enhancements', [])
            references = nist_control.get('references') or nist_control.get('References', [])
            function_names = nist_control.get('function_names', [])
            
            # Extract control family for profile mapping
            family = self.extract_control_family(control_id)
            profile = self.PROFILE_MAPPING.get(family, '• Level 2')
            
            # Get section name
            section = self.get_section(control_id)
            
            # Format description
            description = self.format_control_description(control)
            
            # Build rationale from discussion
            rationale = discussion if discussion else f"This control is essential for maintaining security and compliance in accordance with NIST {control_id} requirements."
            
            # Generate audit and remediation sections
            audit = self.generate_audit_section(control_id, description, control_enhancements)
            remediation = self.generate_remediation_section(control_id, description)
            
            # Format references
            if isinstance(references, list):
                references_str = "\n".join([f"{i+1}. {ref}" for i, ref in enumerate(references) if ref])
            else:
                references_str = str(references) if references else ""
            
            # Extract additional information
            additional_info = self.extract_additional_information(discussion, references, control_enhancements)
            
            # Determine assessment type (default to Manual unless automated checks exist)
            assessment = "Automated" if function_names else "Manual"
            
            # Build CIS-like structure
            cis_control = {
                "id": control_id,
                "section": section,
                "title": control_name,
                "assessment": assessment,
                "description": description,
                "rationale": rationale,
                "audit": audit,
                "remediation": remediation,
                "profile_applicability": profile,
                "references": references_str,
                "function_names": function_names if function_names else []
            }
            
            # Add optional fields
            if additional_info:
                cis_control["additional_information"] = additional_info
            
            # Add optional impact field if available in discussion
            if discussion and any(keyword in discussion.lower() for keyword in ['impact', 'consequence', 'effect']):
                cis_control["impact"] = "See rationale for potential impacts."
            
            # Add related controls as additional information
            if related_controls:
                cis_control["related_controls"] = related_controls
            
            # Add control enhancements information
            if control_enhancements:
                valid_enhancements = [e for e in control_enhancements if e and isinstance(e, dict)]
                if valid_enhancements:
                    cis_control["control_enhancements_count"] = len(valid_enhancements)
            
            return cis_control
            
        except Exception as e:
            self.stats['errors'].append(f"Error mapping {control_id}: {str(e)}")
            return None
    
    def map_file(self, input_file: str, output_file: str) -> bool:
        """Map entire NIST JSON file to CIS format"""
        try:
            print(f"Reading NIST controls from: {input_file}")
            with open(input_file, 'r', encoding='utf-8') as f:
                nist_controls = json.load(f)
            
            if not isinstance(nist_controls, list):
                print("Error: Input file must contain a JSON array of controls")
                return False
            
            print(f"Total entries in input file: {len(nist_controls)}")
            
            cis_controls = []
            for control in nist_controls:
                self.stats['total'] += 1
                mapped = self.map_control(control)
                if mapped:
                    cis_controls.append(mapped)
                    self.stats['mapped'] += 1
                else:
                    self.stats['skipped'] += 1
            
            print(f"Successfully mapped {len(cis_controls)} controls")
            
            # Write output
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(cis_controls, f, indent=2, ensure_ascii=False)
            
            print(f"Output written to: {output_file}")
            
            # Print statistics
            print("\n=== Mapping Statistics ===")
            print(f"Total entries processed: {self.stats['total']}")
            print(f"Successfully mapped: {self.stats['mapped']}")
            print(f"Skipped (empty/invalid): {self.stats['skipped']}")
            
            if self.stats['errors']:
                print(f"\nErrors encountered: {len(self.stats['errors'])}")
                for error in self.stats['errors'][:10]:  # Show first 10 errors
                    print(f"  - {error}")
            
            return True
            
        except FileNotFoundError:
            print(f"Error: Input file not found: {input_file}")
            return False
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in input file: {e}")
            return False
        except Exception as e:
            print(f"Error: {e}")
            return False


def main():
    """Main execution function"""
    if len(sys.argv) < 2:
        print("Usage: python nist_to_cis_mapper.py <input_file> [output_file]")
        print("\nExample:")
        print("  python nist_to_cis_mapper.py nist_controls_updated_simple_20250825_130841.json nist_controls_cis_format.json")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    # Generate output filename if not provided
    if len(sys.argv) >= 3:
        output_file = sys.argv[2]
    else:
        input_path = Path(input_file)
        output_file = str(input_path.parent / f"{input_path.stem}_cis_format.json")
    
    mapper = NISTToCISMapper()
    success = mapper.map_file(input_file, output_file)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
