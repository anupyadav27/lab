#!/usr/bin/env python3
"""
NIST SP 800-53 Rev 5 Parser
Extracts controls, sub-parts, and enhancements from HTML file
Generates JSON with cumulative descriptions for CSPM mapping
"""

import json
import re
import html
from collections import defaultdict

def clean_text(text):
    """Clean and normalize text"""
    if not text:
        return ""
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove non-breaking spaces
    text = text.replace('\u00a0', ' ')
    return text.strip()

def extract_control_id_and_name(soup_section):
    """Extract control ID and name from a section"""
    # Look for patterns like <b>AC-1</b> followed by name
    bold_tags = soup_section.find_all('b')
    
    for i, tag in enumerate(bold_tags):
        text = clean_text(tag.get_text())
        # Match control ID pattern: AC-1, AC-2, etc.
        if re.match(r'^[A-Z]{2,3}-\d+$', text):
            control_id = text
            # Get control name from next bold tag or nearby text
            control_name = ""
            if i + 1 < len(bold_tags):
                next_text = clean_text(bold_tags[i + 1].get_text())
                if next_text and not re.match(r'^[A-Z]{2,3}-\d+', next_text):
                    control_name = next_text
            return control_id, control_name
    
    return None, None

def extract_control_statement(text):
    """Extract the control statement section"""
    # Find text between "Control:" and "Discussion:"
    match = re.search(r'Control:\s*(.*?)\s*Discussion:', text, re.DOTALL | re.IGNORECASE)
    if match:
        return clean_text(match.group(1))
    return ""

def extract_discussion(text):
    """Extract the discussion section"""
    # Find text between "Discussion:" and "Related Controls:" or "Control Enhancements:"
    match = re.search(r'Discussion:\s*(.*?)\s*(?:Related Controls:|Control Enhancements:)', text, re.DOTALL | re.IGNORECASE)
    if match:
        return clean_text(match.group(1))
    return ""

def extract_related_controls(text):
    """Extract related controls list"""
    # Find text after "Related Controls:"
    match = re.search(r'Related Controls:\s*(.*?)(?:Control Enhancements:|References:|$)', text, re.DOTALL | re.IGNORECASE)
    if not match:
        return []
    
    controls_text = match.group(1)
    # Extract control IDs (e.g., AC-1, IA-5, PM-10)
    control_ids = re.findall(r'\b[A-Z]{2,3}-\d+(?:\(\d+\))?\b', controls_text)
    
    # Remove duplicates and "None"
    controls = []
    for cid in control_ids:
        if cid not in controls and cid.lower() != 'none':
            controls.append(cid)
    
    return controls

def split_control_into_parts(control_statement):
    """Split control statement into parts (a, b, c, etc.)"""
    parts = {}
    
    # Split by pattern like "a.", "b.", "c." at the beginning of lines
    # This regex looks for lowercase letter followed by period at word boundary
    pattern = r'\b([a-l])\.\s+'
    
    splits = re.split(pattern, control_statement)
    
    if len(splits) > 1:
        # First element is text before first part (usually empty or "Control:")
        for i in range(1, len(splits), 2):
            if i + 1 < len(splits):
                part_letter = splits[i]
                part_text = splits[i + 1].strip()
                parts[part_letter] = part_text
    
    return parts

def extract_enhancements(text, control_id):
    """Extract control enhancements"""
    enhancements = []
    
    # Look for "Control Enhancements:" section
    match = re.search(r'Control Enhancements:\s*(.*?)(?:References:|$)', text, re.DOTALL | re.IGNORECASE)
    if not match:
        return enhancements
    
    enh_section = match.group(1)
    
    # Check if it says "None"
    if re.search(r'^\s*None\s*\.?\s*$', enh_section, re.IGNORECASE):
        return enhancements
    
    # Split by enhancement pattern: (1), (2), (3), etc.
    # Look for pattern like "(1)" followed by enhancement name
    pattern = r'\((\d+)\)\s+(.*?)(?=\(\d+\)|$)'
    matches = re.findall(pattern, enh_section, re.DOTALL)
    
    for enh_num, enh_text in matches:
        enhancements.append({
            'number': enh_num,
            'text': clean_text(enh_text)
        })
    
    return enhancements

def extract_text_from_html(html_content):
    """Extract text from HTML without BeautifulSoup"""
    # Remove HTML tags but keep content
    text = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<[^>]+>', ' ', text)
    # Decode HTML entities
    text = html.unescape(text)
    # Clean up whitespace
    text = re.sub(r'\s+', ' ', text)
    return text

def parse_nist_html(html_file):
    """Main parser function"""
    print(f"Reading HTML file: {html_file}")
    
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Extract text from HTML
    full_text = extract_text_from_html(html_content)
    
    print(f"Extracted text length: {len(full_text)} characters")
    
    controls_data = []
    
    # Find all control patterns: AC-1 POLICY AND PROCEDURES
    # Look for pattern: uppercase letters-number followed by uppercase title
    control_pattern = r'\b([A-Z]{2,3}-\d+)\s+([A-Z][A-Z\s\-/]+?)\s+Control:\s'
    
    control_matches = list(re.finditer(control_pattern, full_text))
    
    print(f"Found {len(control_matches)} control matches")
    
    for i, match in enumerate(control_matches):
        control_id = match.group(1)
        control_name_raw = match.group(2)
        # Clean up control name
        control_name = re.sub(r'\s+', ' ', control_name_raw).strip()
        
        # Get the text for this control (until next control or end)
        start_pos = match.start()
        if i + 1 < len(control_matches):
            end_pos = control_matches[i + 1].start()
        else:
            end_pos = len(full_text)
        
        control_text = full_text[start_pos:end_pos]
        
        print(f"\n  Processing: {control_id} - {control_name}")
        
        # Extract control statement
        control_statement = extract_control_statement(control_text)
        if not control_statement:
            print(f"    ⚠️  No control statement found")
            continue
        
        # Extract discussion
        discussion = extract_discussion(control_text)
        
        # Extract related controls
        related_controls = extract_related_controls(control_text)
        
        # Split into parts
        parts = split_control_into_parts(control_statement)
        
        # Extract enhancements
        enhancements = extract_enhancements(control_text, control_id)
        
        print(f"    Parts: {len(parts)}, Enhancements: {len(enhancements)}")
        
        # Generate rows for sub-parts
        if parts:
            for part_letter, part_text in sorted(parts.items()):
                # Create shorter title from first few words of part
                part_words = part_text.split()[:5]
                part_title = ' '.join(part_words)
                if len(part_text.split()) > 5:
                    part_title += '...'
                
                row = {
                    'id': f"{control_id}-{part_letter}",
                    'title': f"{control_name.title()} - {part_title.capitalize()}",
                    'description': f"Control: {control_statement}\n\nThis control addresses part ({part_letter}): {part_text}",
                    'discussion': discussion,
                    'related_controls': related_controls,
                    'source': 'NIST SP 800-53 Rev 5'
                }
                controls_data.append(row)
        
        # Generate rows for enhancements
        if enhancements:
            for enh in enhancements:
                # Extract enhancement name (usually first sentence or until first colon)
                enh_text = enh['text']
                enh_name_match = re.match(r'([^:\.]{10,80})', enh_text)
                enh_name = enh_name_match.group(1).strip() if enh_name_match else enh_text[:60]
                
                row = {
                    'id': f"{control_id}({enh['number']})",
                    'title': f"{control_name.title()} - {enh_name.capitalize()}",
                    'description': f"Control: {control_statement}\n\nEnhancement ({enh['number']}): {enh_text}",
                    'discussion': discussion,
                    'related_controls': related_controls,
                    'source': 'NIST SP 800-53 Rev 5'
                }
                controls_data.append(row)
        
        # Generate standalone row if NO sub-parts AND NO enhancements
        if not parts and not enhancements:
            print(f"    → Standalone control (no sub-parts, no enhancements)")
            row = {
                'id': control_id,
                'title': control_name.title(),
                'description': f"Control: {control_statement}",
                'discussion': discussion,
                'related_controls': related_controls,
                'source': 'NIST SP 800-53 Rev 5'
            }
            controls_data.append(row)
    
    return controls_data

def main():
    html_file = '/Users/apple/Desktop/compliance_Database/compliance_document/nist/NIST.SP.800-53r5.html'
    output_file = '/Users/apple/Desktop/compliance_Database/compliance_document/nist/NIST_SP_800-53_Rev5_controls.json'
    
    print("="*90)
    print("NIST SP 800-53 Rev 5 Parser")
    print("="*90)
    
    # Parse HTML
    controls = parse_nist_html(html_file)
    
    print(f"\n{'='*90}")
    print(f"Extraction complete!")
    print(f"Total records: {len(controls)}")
    print(f"{'='*90}")
    
    # Save to JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(controls, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ JSON saved to: {output_file}")
    
    # Show sample
    if controls:
        print(f"\n{'='*90}")
        print("Sample record:")
        print(f"{'='*90}")
        print(json.dumps(controls[0], indent=2))

if __name__ == '__main__':
    main()

