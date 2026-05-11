import json
import os
import re
import csv
from typing import Dict, Optional
from datetime import datetime
from collections import defaultdict


def extract_approach(text: str) -> str:
    """Extract audit approach from response text."""
    if not text:
        return "Unknown"
    
    # Look for explicit approach markers
    if "**AUDIT APPROACH:** Manual" in text or "**AUDIT APPROACH:** MANUAL" in text:
        return "Manual"
    elif "**AUDIT APPROACH:** Automated" in text or "**AUDIT APPROACH:** AUTOMATED" in text:
        return "Automated"
    
    # Fallback to content analysis
    if "MANUAL STEPS:" in text and "PROGRAM NAME:" not in text:
        return "Manual"
    elif "PROGRAM NAME:" in text:
        return "Automated"
    
    return "Unknown"


def extract_program_name(text: str) -> Optional[str]:
    """Extract program name from automated response."""
    if not text:
        return None
    
    # Look for program name pattern
    pattern = r"\*\*PROGRAM NAME:\*\*\s*[`]?([a-z_]+)[`]?"
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    
    # Alternative pattern
    pattern2 = r"Program Name:?\s*[`]?([a-z_]+)[`]?"
    match2 = re.search(pattern2, text, re.IGNORECASE)
    if match2:
        return match2.group(1).strip()
    
    return None


def extract_manual_steps(text: str) -> Optional[str]:
    """Extract manual steps from response."""
    if not text:
        return None
    
    # Find the manual steps section
    pattern = r"\*\*MANUAL STEPS:\*\*\s*(.*?)(?:\*\*[A-Z]|$)"
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    if match:
        steps = match.group(1).strip()
        return steps if steps else None
    
    return None


def extract_automation_details(text: str) -> Optional[str]:
    """Extract automation details from response."""
    if not text:
        return None
    
    # Find the automation details section
    pattern = r"\*\*AUTOMATION DETAILS:\*\*\s*(.*?)(?:\*\*SOURCE:|$)"
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    if match:
        details = match.group(1).strip()
        return details if details else None
    
    return None


def extract_review_validation(text: str) -> Dict:
    """Extract validation decision from GPT-4o review."""
    if not text:
        return {"validation": "Unknown", "score": 0, "confidence": "Unknown"}
    
    result = {
        "validation": "Unknown",
        "score": 0,
        "confidence": "Unknown",
        "recommendation": None
    }
    
    # Extract validation
    if "APPROACH VALIDATION:** AGREE" in text:
        result["validation"] = "AGREE"
    elif "APPROACH VALIDATION:** DISAGREE" in text:
        result["validation"] = "DISAGREE"
    elif "APPROACH VALIDATION:** PARTIALLY_AGREE" in text:
        result["validation"] = "PARTIALLY_AGREE"
    
    # Extract technical accuracy score
    score_pattern = r"TECHNICAL ACCURACY:\*\*\s*(\d+)"
    score_match = re.search(score_pattern, text, re.IGNORECASE)
    if score_match:
        result["score"] = int(score_match.group(1))
    
    # Extract confidence
    if "CONFIDENCE:** HIGH" in text or "CONFIDENCE: HIGH" in text:
        result["confidence"] = "HIGH"
    elif "CONFIDENCE:** MEDIUM" in text or "CONFIDENCE: MEDIUM" in text:
        result["confidence"] = "MEDIUM"
    elif "CONFIDENCE:** LOW" in text or "CONFIDENCE: LOW" in text:
        result["confidence"] = "LOW"
    
    # Extract recommendation
    rec_pattern = r"FINAL RECOMMENDATION:\*\*\s*(.*?)(?:\n\n|$)"
    rec_match = re.search(rec_pattern, text, re.DOTALL | re.IGNORECASE)
    if rec_match:
        result["recommendation"] = rec_match.group(1).strip()[:200]
    
    return result


def determine_final_approach(original_approach: str, review_validation: str) -> str:
    """Determine final approach based on original and review."""
    if review_validation == "DISAGREE":
        # If GPT-4o disagrees, flag for manual review
        return f"{original_approach} (Under Review)"
    elif review_validation == "PARTIALLY_AGREE":
        # If partially agrees, keep original but note concern
        return f"{original_approach} (Verify)"
    else:
        # If agrees or unknown, keep original
        return original_approach


def consolidate_control(reviewed_json: Dict) -> Dict:
    """Consolidate a single control into final format."""
    
    # Extract original assessment
    original = reviewed_json.get("original_assessment", {})
    original_response = original.get("response", "")
    original_approach = extract_approach(original_response)
    
    # Extract review
    review = reviewed_json.get("review", {})
    review_response = review.get("response", "")
    review_data = extract_review_validation(review_response)
    
    # Determine final approach
    final_approach = determine_final_approach(original_approach, review_data["validation"])
    
    # Extract details based on approach
    program_name = None
    automation_details = None
    manual_steps = None
    
    if "Automated" in original_approach or "Automated" in final_approach:
        program_name = extract_program_name(original_response)
        automation_details = extract_automation_details(original_response)
    
    if "Manual" in original_approach or "Manual" in final_approach:
        manual_steps = extract_manual_steps(original_response)
    
    # Get input row data
    input_row = reviewed_json.get("input_row", {})
    
    # Build final consolidated record
    consolidated = {
        "unique_id": reviewed_json.get("unique_id", ""),
        "control_id": reviewed_json.get("control_id", ""),
        "source": reviewed_json.get("source", ""),
        "title": input_row.get("title", ""),
        "description": input_row.get("description", ""),
        
        # Final Decision
        "final_approach": final_approach,
        "original_approach": original_approach,
        "review_validation": review_data["validation"],
        
        # Quality Metrics
        "technical_accuracy_score": review_data["score"],
        "confidence_level": review_data["confidence"],
        
        # Implementation Details
        "program_name": program_name,
        "automation_details": automation_details,
        "manual_steps": manual_steps,
        
        # Review Details
        "review_recommendation": review_data.get("recommendation"),
        
        # Full Responses (for reference)
        "original_response": original_response,
        "review_response": review_response,
        
        # Metadata
        "reviewed_at": review.get("reviewed_at"),
        "original_model": original.get("model", "gpt-4o-mini"),
        "review_model": review.get("model", "gpt-4o"),
    }
    
    return consolidated


def main():
    print("╔════════════════════════════════════════════════════════════════════════════════╗")
    print("║              📊 CONSOLIDATING FINAL COMPLIANCE DECISIONS                       ║")
    print("╚════════════════════════════════════════════════════════════════════════════════╝")
    print()
    
    # Output directory
    output_dir = f"output_final_consolidated_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(output_dir, exist_ok=True)
    
    reviewed_dir = "output_reviewed_20251026_195327"
    
    if not os.path.exists(reviewed_dir):
        print(f"❌ Error: {reviewed_dir} not found!")
        return
    
    # Process all reviewed files
    consolidated_records = []
    stats = defaultdict(int)
    
    files = [f for f in os.listdir(reviewed_dir) if f.endswith('.json')]
    total_files = len(files)
    
    print(f"📁 Processing {total_files} reviewed files...")
    print()
    
    for idx, filename in enumerate(files, 1):
        filepath = os.path.join(reviewed_dir, filename)
        
        try:
            with open(filepath, 'r') as f:
                reviewed_json = json.load(f)
            
            # Consolidate
            consolidated = consolidate_control(reviewed_json)
            consolidated_records.append(consolidated)
            
            # Update stats
            stats['total'] += 1
            stats[f"approach_{consolidated['final_approach'].replace(' ', '_')}"] += 1
            stats[f"validation_{consolidated['review_validation']}"] += 1
            stats[f"confidence_{consolidated['confidence_level']}"] += 1
            
            if consolidated['technical_accuracy_score'] >= 8:
                stats['high_quality'] += 1
            elif consolidated['technical_accuracy_score'] >= 6:
                stats['medium_quality'] += 1
            else:
                stats['low_quality'] += 1
            
            if idx % 50 == 0:
                print(f"   Processed: {idx}/{total_files}")
        
        except Exception as e:
            print(f"   ❌ Error processing {filename}: {e}")
            stats['errors'] += 1
    
    print()
    print(f"✅ Processed {stats['total']} controls")
    print()
    
    # Save consolidated JSON
    json_output = os.path.join(output_dir, "consolidated_all_controls.json")
    with open(json_output, 'w') as f:
        json.dump(consolidated_records, f, indent=2, ensure_ascii=False)
    print(f"📄 Saved: {json_output}")
    
    # Save as CSV for easy viewing
    csv_output = os.path.join(output_dir, "consolidated_all_controls.csv")
    if consolidated_records:
        fieldnames = [
            'unique_id', 'control_id', 'source', 'title',
            'final_approach', 'original_approach', 'review_validation',
            'technical_accuracy_score', 'confidence_level',
            'program_name', 'review_recommendation'
        ]
        
        with open(csv_output, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(consolidated_records)
        
        print(f"📄 Saved: {csv_output}")
    
    # Create separate lists for Automated and Manual
    automated = [r for r in consolidated_records if 'Automated' in r['final_approach']]
    manual = [r for r in consolidated_records if 'Manual' in r['final_approach']]
    under_review = [r for r in consolidated_records if 'Review' in r['final_approach'] or 'Verify' in r['final_approach']]
    
    # Save Automated controls with program names
    if automated:
        automated_output = os.path.join(output_dir, "automated_controls_with_programs.json")
        with open(automated_output, 'w') as f:
            json.dump(automated, f, indent=2, ensure_ascii=False)
        print(f"📄 Saved: {automated_output}")
        
        # CSV for automated
        auto_csv = os.path.join(output_dir, "automated_controls.csv")
        auto_fields = ['control_id', 'title', 'program_name', 'technical_accuracy_score', 'confidence_level', 'source']
        with open(auto_csv, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=auto_fields, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(automated)
        print(f"📄 Saved: {auto_csv}")
    
    # Save Manual controls
    if manual:
        manual_output = os.path.join(output_dir, "manual_controls_with_steps.json")
        with open(manual_output, 'w') as f:
            json.dump(manual, f, indent=2, ensure_ascii=False)
        print(f"📄 Saved: {manual_output}")
        
        # CSV for manual
        manual_csv = os.path.join(output_dir, "manual_controls.csv")
        manual_fields = ['control_id', 'title', 'confidence_level', 'source']
        with open(manual_csv, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=manual_fields, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(manual)
        print(f"📄 Saved: {manual_csv}")
    
    # Save under review controls
    if under_review:
        review_output = os.path.join(output_dir, "controls_under_review.json")
        with open(review_output, 'w') as f:
            json.dump(under_review, f, indent=2, ensure_ascii=False)
        print(f"📄 Saved: {review_output}")
    
    # Generate summary report
    print()
    print("=" * 80)
    print("📊 FINAL STATISTICS")
    print("=" * 80)
    print()
    print(f"Total Controls:                {stats['total']}")
    print()
    print("BY APPROACH:")
    print(f"  Automated:                   {len(automated)} ({len(automated)/stats['total']*100:.1f}%)")
    print(f"  Manual:                      {len(manual)} ({len(manual)/stats['total']*100:.1f}%)")
    print(f"  Under Review/Verify:         {len(under_review)} ({len(under_review)/stats['total']*100:.1f}%)")
    print()
    print("BY VALIDATION:")
    print(f"  AGREE:                       {stats.get('validation_AGREE', 0)}")
    print(f"  PARTIALLY_AGREE:             {stats.get('validation_PARTIALLY_AGREE', 0)}")
    print(f"  DISAGREE:                    {stats.get('validation_DISAGREE', 0)}")
    print(f"  Unknown:                     {stats.get('validation_Unknown', 0)}")
    print()
    print("BY QUALITY SCORE:")
    print(f"  High (8-10):                 {stats.get('high_quality', 0)}")
    print(f"  Medium (6-7):                {stats.get('medium_quality', 0)}")
    print(f"  Low (1-5):                   {stats.get('low_quality', 0)}")
    print()
    print("BY CONFIDENCE:")
    print(f"  HIGH:                        {stats.get('confidence_HIGH', 0)}")
    print(f"  MEDIUM:                      {stats.get('confidence_MEDIUM', 0)}")
    print(f"  LOW:                         {stats.get('confidence_LOW', 0)}")
    print(f"  Unknown:                     {stats.get('confidence_Unknown', 0)}")
    print()
    print("=" * 80)
    print()
    print(f"✅ All files saved to: {output_dir}/")
    print()
    
    # Create summary report file
    summary_file = os.path.join(output_dir, "SUMMARY_REPORT.txt")
    with open(summary_file, 'w') as f:
        f.write("FINAL COMPLIANCE CONTROLS SUMMARY\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"Total Controls: {stats['total']}\n\n")
        f.write(f"Automated: {len(automated)} ({len(automated)/stats['total']*100:.1f}%)\n")
        f.write(f"Manual: {len(manual)} ({len(manual)/stats['total']*100:.1f}%)\n")
        f.write(f"Under Review: {len(under_review)} ({len(under_review)/stats['total']*100:.1f}%)\n\n")
        
        f.write("AUTOMATED CONTROLS (with program names):\n")
        f.write("-" * 80 + "\n")
        for ctrl in automated[:20]:
            f.write(f"{ctrl['control_id']}: {ctrl['program_name'] or 'N/A'}\n")
        if len(automated) > 20:
            f.write(f"... and {len(automated) - 20} more\n")
        
        f.write("\n")
        f.write("MANUAL CONTROLS:\n")
        f.write("-" * 80 + "\n")
        for ctrl in manual[:20]:
            f.write(f"{ctrl['control_id']}: {ctrl['title'][:60]}...\n")
        if len(manual) > 20:
            f.write(f"... and {len(manual) - 20} more\n")
        
        if under_review:
            f.write("\n")
            f.write("CONTROLS NEEDING REVIEW:\n")
            f.write("-" * 80 + "\n")
            for ctrl in under_review:
                f.write(f"{ctrl['control_id']}: {ctrl['final_approach']} - {ctrl['review_recommendation'][:80] or 'N/A'}\n")
    
    print(f"📄 Saved: {summary_file}")
    print()
    print("🎉 Consolidation Complete!")


if __name__ == "__main__":
    main()

