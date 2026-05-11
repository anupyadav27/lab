import csv
import json
import os
import re
from typing import Dict, Optional
from datetime import datetime


def extract_final_approach(text: str) -> str:
    """Extract final approach from decision text."""
    if not text:
        return "Unknown"
    
    # Look for explicit final approach
    pattern = r"\*\*FINAL APPROACH:\*\*\s*(Manual|Automated)"
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return match.group(1).capitalize()
    
    return "Unknown"


def extract_confidence(text: str) -> str:
    """Extract confidence level from decision text."""
    if not text:
        return "Unknown"
    
    pattern = r"\*\*CONFIDENCE:\*\*\s*(HIGH|MEDIUM|LOW)"
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return match.group(1).upper()
    
    return "Unknown"


def extract_program_name(text: str) -> Optional[str]:
    """Extract program name from decision text."""
    if not text or "Manual" in text:
        return None
    
    # Look for program name in final decision
    pattern = r"\*\*PROGRAM NAME:\*\*\s*[`]?([a-z_]+)[`]?"
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    
    return None


def extract_justification(text: str) -> Optional[str]:
    """Extract justification from decision text."""
    if not text:
        return None
    
    pattern = r"\*\*JUSTIFICATION:\*\*\s*(.*?)(?:\n\n\*\*|$)"
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()[:300]  # Limit to 300 chars
    
    return None


def extract_automation_summary(text: str) -> Optional[str]:
    """Extract automation details summary."""
    if not text or "Manual" in extract_final_approach(text):
        return None
    
    # Extract Azure Resource/Service
    resource_pattern = r"Azure Resource/Service:\s*([^\n]+)"
    resource_match = re.search(resource_pattern, text, re.IGNORECASE)
    resource = resource_match.group(1).strip() if resource_match else None
    
    # Extract API/CLI Method
    api_pattern = r"API/CLI Method:\s*([^\n]+)"
    api_match = re.search(api_pattern, text, re.IGNORECASE)
    api = api_match.group(1).strip() if api_match else None
    
    if resource or api:
        return f"Resource: {resource or 'N/A'} | API: {api or 'N/A'}"
    
    return None


def extract_manual_summary(text: str) -> Optional[str]:
    """Extract manual steps summary."""
    if not text or "Automated" in extract_final_approach(text):
        return None
    
    # Look for "WHY NOT AUTOMATED"
    pattern = r"\*\*WHY NOT AUTOMATED:\*\*\s*(.*?)(?:\n\n|$)"
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()[:200]
    
    return "Requires manual verification"


def main():
    print("╔════════════════════════════════════════════════════════════════════════════════╗")
    print("║              📝 UPDATING CSV WITH FINAL DECISIONS                              ║")
    print("╚════════════════════════════════════════════════════════════════════════════════╝")
    print()
    
    # Paths
    input_csv = "controls_batch_cleaned.csv"
    final_decisions_dir = "output_final_decisions_20251027_192344"
    output_csv = f"controls_batch_FINAL_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    if not os.path.exists(input_csv):
        print(f"❌ Error: {input_csv} not found!")
        return
    
    if not os.path.exists(final_decisions_dir):
        print(f"❌ Error: {final_decisions_dir} not found!")
        return
    
    # Load all final decisions into memory
    print("📂 Loading final decisions...")
    final_decisions = {}
    
    for filename in os.listdir(final_decisions_dir):
        if filename.endswith('.json'):
            filepath = os.path.join(final_decisions_dir, filename)
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    control_id = data.get('control_id')
                    unique_id = data.get('unique_id')
                    
                    # Store by both control_id and unique_id for lookup
                    if control_id:
                        final_decisions[control_id] = data
                    if unique_id:
                        final_decisions[unique_id] = data
            except Exception as e:
                print(f"   ⚠️  Error loading {filename}: {e}")
    
    print(f"   ✅ Loaded {len(final_decisions)} final decisions")
    print()
    
    # Read original CSV and update
    print("📋 Processing CSV...")
    updated_rows = []
    matched = 0
    unmatched = 0
    
    with open(input_csv, 'r') as f:
        reader = csv.DictReader(f)
        original_fieldnames = reader.fieldnames
        
        # Add new fields for final decisions
        new_fieldnames = list(original_fieldnames) + [
            'final_approach',
            'final_confidence',
            'program_name',
            'justification',
            'automation_summary',
            'manual_summary',
            'three_ai_consensus',
            'decision_timestamp'
        ]
        
        for row_idx, row in enumerate(reader, start=2):
            control_id = row.get('id', '').strip()
            unique_id = row.get('unique_id', '').strip()
            
            # Try to find final decision
            final_data = None
            if control_id and control_id in final_decisions:
                final_data = final_decisions[control_id]
            elif unique_id and unique_id in final_decisions:
                final_data = final_decisions[unique_id]
            
            if final_data:
                # Extract data from final decision
                final_decision_text = final_data.get('final_decision', {}).get('response', '')
                
                row['final_approach'] = extract_final_approach(final_decision_text)
                row['final_confidence'] = extract_confidence(final_decision_text)
                row['program_name'] = extract_program_name(final_decision_text) or ''
                row['justification'] = extract_justification(final_decision_text) or ''
                row['automation_summary'] = extract_automation_summary(final_decision_text) or ''
                row['manual_summary'] = extract_manual_summary(final_decision_text) or ''
                row['three_ai_consensus'] = 'Yes'
                row['decision_timestamp'] = final_data.get('final_decision', {}).get('decided_at', '')
                
                matched += 1
            else:
                # No final decision found
                row['final_approach'] = 'Not Reviewed'
                row['final_confidence'] = 'N/A'
                row['program_name'] = ''
                row['justification'] = ''
                row['automation_summary'] = ''
                row['manual_summary'] = ''
                row['three_ai_consensus'] = 'No'
                row['decision_timestamp'] = ''
                
                unmatched += 1
            
            updated_rows.append(row)
            
            if (row_idx - 1) % 100 == 0:
                print(f"   Processed: {row_idx - 1} rows")
    
    print(f"   ✅ Total processed: {len(updated_rows)}")
    print(f"   ✅ Matched: {matched}")
    print(f"   ⚠️  Unmatched: {unmatched}")
    print()
    
    # Write updated CSV
    print(f"💾 Writing updated CSV...")
    
    # Clean rows - ensure all fields are in fieldnames
    cleaned_rows = []
    for row in updated_rows:
        cleaned_row = {k: v for k, v in row.items() if k in new_fieldnames and k is not None}
        # Ensure all new fields exist
        for field in new_fieldnames:
            if field not in cleaned_row:
                cleaned_row[field] = ''
        cleaned_rows.append(cleaned_row)
    
    with open(output_csv, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=new_fieldnames)
        writer.writeheader()
        writer.writerows(cleaned_rows)
    
    print(f"   ✅ Saved: {output_csv}")
    print()
    
    # Generate statistics
    print("=" * 80)
    print("📊 FINAL STATISTICS")
    print("=" * 80)
    
    automated = sum(1 for r in updated_rows if r.get('final_approach') == 'Automated')
    manual = sum(1 for r in updated_rows if r.get('final_approach') == 'Manual')
    not_reviewed = sum(1 for r in updated_rows if r.get('final_approach') == 'Not Reviewed')
    
    high_conf = sum(1 for r in updated_rows if r.get('final_confidence') == 'HIGH')
    medium_conf = sum(1 for r in updated_rows if r.get('final_confidence') == 'MEDIUM')
    low_conf = sum(1 for r in updated_rows if r.get('final_confidence') == 'LOW')
    
    programs_count = sum(1 for r in updated_rows if r.get('program_name', '').strip())
    
    print()
    print(f"Total Rows:                {len(updated_rows)}")
    print()
    print("BY APPROACH:")
    print(f"  Automated:               {automated} ({automated/len(updated_rows)*100:.1f}%)")
    print(f"  Manual:                  {manual} ({manual/len(updated_rows)*100:.1f}%)")
    print(f"  Not Reviewed:            {not_reviewed} ({not_reviewed/len(updated_rows)*100:.1f}%)")
    print()
    print("BY CONFIDENCE:")
    print(f"  HIGH:                    {high_conf}")
    print(f"  MEDIUM:                  {medium_conf}")
    print(f"  LOW:                     {low_conf}")
    print()
    print(f"Program Names Assigned:    {programs_count}")
    print()
    print("=" * 80)
    print()
    
    # Create summary files
    print("📄 Creating summary files...")
    
    # Automated controls with program names
    automated_csv = f"automated_programs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    automated_rows = [r for r in updated_rows if r.get('final_approach') == 'Automated']
    if automated_rows:
        auto_fields = ['id', 'title', 'program_name', 'final_confidence', 'automation_summary', 'source']
        with open(automated_csv, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=auto_fields, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(automated_rows)
        print(f"   ✅ {automated_csv} ({len(automated_rows)} controls)")
    
    # Manual controls
    manual_csv = f"manual_controls_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    manual_rows = [r for r in updated_rows if r.get('final_approach') == 'Manual']
    if manual_rows:
        manual_fields = ['id', 'title', 'manual_summary', 'final_confidence', 'source']
        with open(manual_csv, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=manual_fields, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(manual_rows)
        print(f"   ✅ {manual_csv} ({len(manual_rows)} controls)")
    
    # High confidence controls
    high_conf_csv = f"high_confidence_controls_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    high_conf_rows = [r for r in updated_rows if r.get('final_confidence') == 'HIGH']
    if high_conf_rows:
        conf_fields = ['id', 'title', 'final_approach', 'program_name', 'source']
        with open(high_conf_csv, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=conf_fields, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(high_conf_rows)
        print(f"   ✅ {high_conf_csv} ({len(high_conf_rows)} controls)")
    
    # Create program names list (unique)
    programs_txt = f"program_names_list_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    program_names = set(r.get('program_name', '').strip() for r in updated_rows if r.get('program_name', '').strip())
    if program_names:
        with open(programs_txt, 'w') as f:
            f.write("# Azure Compliance Program Names\n")
            f.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"# Total: {len(program_names)} unique programs\n\n")
            for prog in sorted(program_names):
                f.write(f"{prog}\n")
        print(f"   ✅ {programs_txt} ({len(program_names)} unique programs)")
    
    print()
    print("=" * 80)
    print("🎉 CSV UPDATE COMPLETE!")
    print("=" * 80)
    print()
    print(f"📝 Main Output:      {output_csv}")
    print(f"🤖 Automated:        {automated_csv}")
    print(f"👤 Manual:           {manual_csv}")
    print(f"⭐ High Confidence:  {high_conf_csv}")
    print(f"📋 Program Names:    {programs_txt}")
    print()


if __name__ == "__main__":
    main()

