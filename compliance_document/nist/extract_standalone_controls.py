#!/usr/bin/env python3
"""
Extract NIST controls that have NO sub-parts AND NO enhancements
These are standalone controls that should generate 1 row each
"""

import json
import re
import html as html_module

def clean_text(text):
    """Clean and normalize text"""
    if not text:
        return ""
    text = re.sub(r'\s+', ' ', text)
    text = text.replace('\u00a0', ' ')
    return text.strip()

def extract_control_statement(text):
    """Extract the control statement section"""
    match = re.search(r'Control:\s*(.*?)\s*Discussion:', text, re.DOTALL | re.IGNORECASE)
    if match:
        return clean_text(match.group(1))
    return ""

def extract_discussion(text):
    """Extract the discussion section"""
    match = re.search(r'Discussion:\s*(.*?)\s*(?:Related Controls:|Control Enhancements:|References:|$)', text, re.DOTALL | re.IGNORECASE)
    if match:
        return clean_text(match.group(1))
    return ""

def extract_related_controls(text):
    """Extract related controls list"""
    match = re.search(r'Related Controls:\s*(.*?)(?:Control Enhancements:|References:|$)', text, re.DOTALL | re.IGNORECASE)
    if not match:
        return []
    
    controls_text = match.group(1)
    control_ids = re.findall(r'\b[A-Z]{2,3}-\d+(?:\(\d+\))?\b', controls_text)
    
    controls = []
    for cid in control_ids:
        if cid not in controls and cid.lower() != 'none':
            controls.append(cid)
    
    return controls

def has_sub_parts(control_statement):
    """Check if control has sub-parts (a., b., c., etc.)"""
    # Look for pattern like "a." at the beginning or after whitespace
    return bool(re.search(r'(?:^|\s)a\.\s+', control_statement))

def has_enhancements(control_text):
    """Check if control has enhancements"""
    # Check for "Control Enhancements:" followed by something other than "None"
    match = re.search(r'Control Enhancements:\s*(.*?)(?:References:|$)', control_text, re.DOTALL | re.IGNORECASE)
    if not match:
        return False
    
    enh_text = match.group(1).strip()
    # Check if it's not just "None"
    if re.match(r'^\s*None\s*\.?\s*$', enh_text, re.IGNORECASE):
        return False
    
    # Check if there are actual enhancement numbers like (1), (2)
    return bool(re.search(r'\(\d+\)', enh_text))

def main():
    print("="*90)
    print("EXTRACTING STANDALONE NIST CONTROLS")
    print("="*90)
    
    # Load existing output to see what we already have
    with open('/Users/apple/Desktop/compliance_Database/compliance_document/nist/NIST_SP_800-53_Rev5_controls.json', 'r') as f:
        existing_controls = json.load(f)
    
    # Get all control IDs already in output
    existing_ids = set()
    for c in existing_controls:
        cid = c['id']
        if '(' in cid:
            base = cid.split('(')[0]
        elif '-' in cid and cid[-1].isalpha():
            base = cid.rsplit('-', 1)[0]
        else:
            base = cid
        existing_ids.add(base)
    
    print(f"\nExisting controls covered: {len(existing_ids)}")
    
    # Read and parse HTML
    print(f"\nReading HTML file...")
    with open('/Users/apple/Desktop/compliance_Database/compliance_document/nist/NIST.SP.800-53r5.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Remove HTML tags
    text = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = html_module.unescape(text)
    text = re.sub(r'\s+', ' ', text)
    
    print(f"Extracted text length: {len(text)} characters")
    
    # Find all controls
    control_pattern = r'\b([A-Z]{2,3}-\d+)\s+([A-Z][A-Z\s\-/]+?)\s+Control:\s'
    control_matches = list(re.finditer(control_pattern, text))
    
    print(f"Found {len(control_matches)} total controls in HTML")
    
    # Process each control to find standalone ones
    standalone_controls = []
    
    for i, match in enumerate(control_matches):
        control_id = match.group(1)
        control_name = re.sub(r'\s+', ' ', match.group(2)).strip()
        
        # Get control text
        start_pos = match.start()
        if i + 1 < len(control_matches):
            end_pos = control_matches[i + 1].start()
        else:
            end_pos = len(text)
        
        control_text = text[start_pos:end_pos]
        
        # Extract components
        control_statement = extract_control_statement(control_text)
        if not control_statement:
            continue
        
        # Check if it has sub-parts or enhancements
        has_parts = has_sub_parts(control_statement)
        has_enh = has_enhancements(control_text)
        
        # If NO sub-parts AND NO enhancements, it's standalone
        if not has_parts and not has_enh:
            discussion = extract_discussion(control_text)
            related_controls = extract_related_controls(control_text)
            
            standalone = {
                'id': control_id,
                'title': control_name.title(),
                'description': f"Control: {control_statement}",
                'discussion': discussion,
                'related_controls': related_controls,
                'source': 'NIST SP 800-53 Rev 5'
            }
            standalone_controls.append(standalone)
            print(f"  Found standalone: {control_id} - {control_name}")
    
    print(f"\n{'='*90}")
    print(f"STANDALONE CONTROLS FOUND: {len(standalone_controls)}")
    print(f"{'='*90}")
    
    # Save standalone controls
    standalone_file = '/Users/apple/Desktop/compliance_Database/compliance_document/nist/NIST_SP_800-53_Rev5_standalone.json'
    with open(standalone_file, 'w', encoding='utf-8') as f:
        json.dump(standalone_controls, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Saved {len(standalone_controls)} standalone controls to:")
    print(f"   {standalone_file}")
    
    # Show the controls
    if standalone_controls:
        print(f"\n📋 List of standalone controls:")
        for ctrl in standalone_controls:
            print(f"   • {ctrl['id']}: {ctrl['title']}")
    
    # Now merge with existing
    print(f"\n{'='*90}")
    print(f"MERGING WITH EXISTING CONTROLS")
    print(f"{'='*90}")
    
    # Combine
    all_controls = existing_controls + standalone_controls
    
    # Sort by ID
    all_controls.sort(key=lambda x: (x['id'].split('-')[0], 
                                      int(x['id'].split('-')[1].split('(')[0].rstrip('abcdefghijklmnopqrstuvwxyz') or '0'),
                                      x['id']))
    
    # Save merged file
    merged_file = '/Users/apple/Desktop/compliance_Database/compliance_document/nist/NIST_SP_800-53_Rev5_controls_COMPLETE.json'
    with open(merged_file, 'w', encoding='utf-8') as f:
        json.dump(all_controls, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Merged file created:")
    print(f"   {merged_file}")
    print(f"\n📊 Summary:")
    print(f"   • Previous records: {len(existing_controls)}")
    print(f"   • Standalone controls: {len(standalone_controls)}")
    print(f"   • TOTAL records: {len(all_controls)}")
    
    print(f"\n{'='*90}")
    print(f"✅ COMPLETE! All controls now included.")
    print(f"{'='*90}")

if __name__ == '__main__':
    main()

