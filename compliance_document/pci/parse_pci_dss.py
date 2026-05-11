#!/usr/bin/env python3
"""
Parse PCI-DSS v4.0.1 HTML document into structured JSON

Schema:
  - id: Requirement ID (e.g., 3.3.1, 10.4.1)
  - title: Requirement title/category
  - description: Complete description including:
    * Defined Approach Requirement
    * Testing Procedures (all .a, .b, .c variants)
    * Purpose
    * Customized Approach Objective
    * Good Practice
    * Applicability Notes
    * Definitions
    * Examples
  - source: "PCI-DSS v4.0.1"
"""

import json
import re
import html as html_module
from collections import defaultdict

def clean_text(text):
    """Clean and normalize text"""
    if not text:
        return ""
    text = re.sub(r'\s+', ' ', text)
    text = text.replace('\u00a0', ' ')
    text = text.strip()
    return text

def extract_text_from_html(html_content):
    """Extract text from HTML without external dependencies"""
    # Remove script and style tags
    text = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)
    
    # Remove HTML tags but keep content
    text = re.sub(r'<[^>]+>', ' ', text)
    
    # Decode HTML entities
    text = html_module.unescape(text)
    
    # Clean up whitespace
    text = re.sub(r'\s+', ' ', text)
    
    return text

def find_requirements(text):
    """
    Find all Defined Approach Requirements in the text
    Pattern: X.X.X followed by requirement text, then testing procedures
    """
    requirements = {}
    
    # Pattern to match requirement IDs like 1.1.1, 3.3.1, 10.4.1, etc.
    # These appear as standalone numbers between sections
    pattern = r'\b(\d+\.\d+\.\d+(?:\.\d+)?)\b'
    
    matches = list(re.finditer(pattern, text))
    
    for i, match in enumerate(matches):
        req_id = match.group(1)
        
        # Skip if this looks like a testing procedure (ends with .a, .b, etc.)
        if re.search(r'\.[a-z]$', req_id):
            continue
            
        # Get text segment for this requirement
        start_pos = match.start()
        if i + 1 < len(matches):
            end_pos = matches[i + 1].start()
        else:
            end_pos = len(text)
        
        req_text = text[start_pos:end_pos]
        
        # Check if this segment contains "Defined Approach Requirements" or similar
        # to confirm it's actually a requirement section
        if 'Defined Approach' in req_text or 'Testing Procedures' in req_text:
            requirements[req_id] = {
                'id': req_id,
                'text': req_text,
                'start': start_pos,
                'end': end_pos
            }
    
    return requirements

def extract_requirement_components(req_id, req_text):
    """
    Extract all components for a requirement:
    - Requirement text
    - Testing procedures
    - Purpose
    - Customized approach
    - Good practice
    - Applicability notes
    - Definitions
    - Examples
    """
    components = {}
    
    # Extract Defined Approach Requirement text
    # Usually appears before "Testing Procedures" or numbered testing items
    req_match = re.search(
        rf'{re.escape(req_id)}\s+(.*?)(?:Defined Approach Testing Procedures|{req_id}\.[a-z]\b|\bCustomized Approach|$)',
        req_text,
        re.DOTALL
    )
    if req_match:
        components['requirement'] = clean_text(req_match.group(1))
    
    # Extract Testing Procedures (X.X.X.a, X.X.X.b, etc.)
    testing_procedures = []
    test_pattern = rf'{re.escape(req_id)}\.([a-z])\s+(.*?)(?={req_id}\.[a-z]\b|\bCustomized Approach|\bPurpose\b|\bApplicability|$)'
    for test_match in re.finditer(test_pattern, req_text, re.DOTALL):
        letter = test_match.group(1)
        test_text = clean_text(test_match.group(2))
        testing_procedures.append({
            'id': f"{req_id}.{letter}",
            'text': test_text
        })
    components['testing_procedures'] = testing_procedures
    
    # Extract Purpose
    purpose_match = re.search(r'Purpose\s+(.*?)(?:\bGood Practice\b|\bDefinitions\b|\bExamples\b|\bCustomized Approach|$)', req_text, re.DOTALL | re.IGNORECASE)
    if purpose_match:
        components['purpose'] = clean_text(purpose_match.group(1))
    
    # Extract Customized Approach Objective
    custom_match = re.search(r'Customized Approach Objective\s+(.*?)(?:\bApplicability\b|\bPurpose\b|$)', req_text, re.DOTALL | re.IGNORECASE)
    if custom_match:
        components['customized_approach'] = clean_text(custom_match.group(1))
    
    # Extract Good Practice
    practice_match = re.search(r'Good Practice\s+(.*?)(?:\bDefinitions\b|\bExamples\b|\bFurther Information\b|$)', req_text, re.DOTALL | re.IGNORECASE)
    if practice_match:
        components['good_practice'] = clean_text(practice_match.group(1))
    
    # Extract Applicability Notes
    applicability_match = re.search(r'Applicability Notes?\s+(.*?)(?:\bPurpose\b|\bGood Practice\b|$)', req_text, re.DOTALL | re.IGNORECASE)
    if applicability_match:
        components['applicability'] = clean_text(applicability_match.group(1))
    
    # Extract Definitions
    definitions_match = re.search(r'Definitions?\s+(.*?)(?:\bExamples\b|\bFurther Information\b|$)', req_text, re.DOTALL | re.IGNORECASE)
    if definitions_match:
        components['definitions'] = clean_text(definitions_match.group(1))
    
    # Extract Examples
    examples_match = re.search(r'Examples?\s+(.*?)(?:\bFurther Information\b|$)', req_text, re.DOTALL | re.IGNORECASE)
    if examples_match:
        components['examples'] = clean_text(examples_match.group(1))
    
    return components

def generate_title(req_id, req_text):
    """Generate a concise title for the requirement"""
    # Try to extract the first sentence or meaningful phrase
    req_match = re.search(rf'{re.escape(req_id)}\s+(.*?)\.', req_text)
    if req_match:
        title = clean_text(req_match.group(1))
        # Limit title length
        if len(title) > 100:
            title = title[:97] + "..."
        return title
    return f"Requirement {req_id}"

def format_description(components):
    """Format all components into a structured description"""
    parts = []
    
    # Defined Approach Requirement
    if components.get('requirement'):
        parts.append(f"Defined Approach Requirement:\n{components['requirement']}")
    
    # Testing Procedures
    if components.get('testing_procedures'):
        procedures_text = "Testing Procedures:\n"
        for proc in components['testing_procedures']:
            procedures_text += f"• {proc['id']}: {proc['text']}\n"
        parts.append(procedures_text.strip())
    
    # Purpose
    if components.get('purpose'):
        parts.append(f"Purpose:\n{components['purpose']}")
    
    # Customized Approach
    if components.get('customized_approach'):
        parts.append(f"Customized Approach Objective:\n{components['customized_approach']}")
    
    # Good Practice
    if components.get('good_practice'):
        parts.append(f"Good Practice:\n{components['good_practice']}")
    
    # Applicability Notes
    if components.get('applicability'):
        parts.append(f"Applicability Notes:\n{components['applicability']}")
    
    # Definitions
    if components.get('definitions'):
        parts.append(f"Definitions:\n{components['definitions']}")
    
    # Examples
    if components.get('examples'):
        parts.append(f"Examples:\n{components['examples']}")
    
    return "\n\n".join(parts)

def parse_pci_dss(html_file, output_file):
    """Main parser function"""
    print(f"="*90)
    print(f"PCI-DSS v4.0.1 PARSER")
    print(f"="*90)
    
    print(f"\n📂 Reading HTML file: {html_file}")
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    print(f"✅ Loaded {len(html_content):,} characters")
    
    # Extract text from HTML
    print(f"\n🔄 Extracting text from HTML...")
    text = extract_text_from_html(html_content)
    print(f"✅ Extracted {len(text):,} characters of text")
    
    # Find all requirements
    print(f"\n🔍 Finding Defined Approach Requirements...")
    requirements = find_requirements(text)
    print(f"✅ Found {len(requirements)} potential requirements")
    
    # Process each requirement
    print(f"\n⚙️  Processing requirements...")
    pci_data = []
    
    for req_id in sorted(requirements.keys(), key=lambda x: [int(p) for p in x.split('.')]):
        req_info = requirements[req_id]
        req_text = req_info['text']
        
        print(f"  📋 Processing {req_id}...")
        
        # Extract components
        components = extract_requirement_components(req_id, req_text)
        
        # Skip if no meaningful content
        if not components.get('requirement') and not components.get('testing_procedures'):
            print(f"     ⚠️  Skipping {req_id} - no content found")
            continue
        
        # Generate title
        title = generate_title(req_id, req_text)
        
        # Format description
        description = format_description(components)
        
        # Create record
        record = {
            'id': req_id,
            'title': title,
            'description': description,
            'source': 'PCI-DSS v4.0.1'
        }
        
        pci_data.append(record)
        print(f"     ✅ Added {req_id} ({len(components.get('testing_procedures', []))} testing procedures)")
    
    # Write output
    print(f"\n💾 Writing output to: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(pci_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Written {len(pci_data)} requirements")
    
    # Summary
    print(f"\n{'='*90}")
    print(f"📊 SUMMARY")
    print(f"{'='*90}")
    print(f"  Total requirements: {len(pci_data)}")
    
    # Count testing procedures
    total_tests = sum(len(r.get('description', '').split('Testing Procedures:')[1].split('•')) - 1 
                     for r in pci_data if 'Testing Procedures:' in r.get('description', ''))
    print(f"  Total testing procedures: ~{total_tests}")
    print(f"  Output file: {output_file}")
    print(f"{'='*90}")

def main():
    import sys
    
    # File paths
    html_file = '/Users/apple/Desktop/compliance_Database/compliance_document/pci/PCI-DSS-v4_0_1.html'
    output_file = '/Users/apple/Desktop/compliance_Database/compliance_document/pci/PCI_DSS_v4_0_1_controls.json'
    
    try:
        parse_pci_dss(html_file, output_file)
        print(f"\n✅ SUCCESS! PCI-DSS parsing complete.")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()

