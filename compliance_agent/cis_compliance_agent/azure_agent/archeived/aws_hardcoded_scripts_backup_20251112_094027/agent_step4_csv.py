#!/usr/bin/env python3
"""
AWS Compliance Agent - Step 4: Generate Final CSV
Consolidates all final decisions into a comprehensive CSV.
"""

import argparse
import csv
import glob
import json
import logging
import os
import re
from datetime import datetime
from typing import Dict, List


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def extract_decision_fields(final_json: Dict) -> Dict:
    """Extract key fields from final decision JSON."""
    
    input_row = final_json.get("input_row", {})
    final_decision = final_json.get("step3_final_decision", {})
    decision_text = final_decision.get("decision_text", "")
    
    # Extract structured data
    approach = final_decision.get("final_approach", "Unknown")
    confidence = final_decision.get("confidence", "MEDIUM")
    program_name = final_decision.get("program_name", "")
    
    # Parse decision text for additional details
    justification = ""
    automation_summary = ""
    manual_summary = ""
    
    lines = decision_text.split('\n')
    current_section = None
    
    # Try to capture sections and program name even if formatting varies
    capture_program_next = False
    for line in lines:
        line_strip = line.strip()
        
        if line_strip.startswith("**JUSTIFICATION:**"):
            current_section = "justification"
            justification = line_strip.replace("**JUSTIFICATION:**", "").strip()
        elif line_strip.startswith("**AUTOMATION DETAILS:**"):
            current_section = "automation"
        elif line_strip.startswith("**MANUAL STEPS:**"):
            current_section = "manual"
        elif line_strip.startswith("**PROGRAM NAME:**"):
            # Next non-empty line likely contains the actual name
            capture_program_next = True
            current_section = None
        elif line_strip.startswith("**"):
            current_section = None
        elif capture_program_next and line_strip and not program_name:
            # Accept explicit name or first aws_* token in the line
            if line_strip.startswith("aws_"):
                program_name = line_strip
            else:
                m = re.search(r"\baws_[a-z0-9_]{8,}\b", line_strip)
                if m:
                    program_name = m.group(0)
            capture_program_next = False
        elif current_section == "justification" and line_strip:
            justification += " " + line_strip
        elif current_section == "automation" and line_strip and not line_strip.startswith("---"):
            automation_summary += line_strip + " "
        elif current_section == "manual" and line_strip and not line_strip.startswith("---"):
            manual_summary += line_strip + " "

    # Final fallback: scan entire decision text for plausible program name if still empty
    if (final_decision.get("final_approach", "").lower() == "automated") and not program_name:
        candidates = re.findall(r"\baws_[a-z0-9_]{8,}\b", decision_text)
        candidates = [c for c in candidates if c.count('_') >= 3]
        if candidates:
            program_name = candidates[0]
    
    return {
        "control_id": final_json.get("control_id", ""),
        "unique_id": final_json.get("unique_id", ""),
        "source": final_json.get("source", ""),
        "title": input_row.get("title", ""),
        "description": input_row.get("description", ""),
        "final_approach": approach,
        "final_confidence": confidence,
        "program_name": program_name,
        "justification": justification.strip(),
        "automation_summary": automation_summary.strip(),
        "manual_summary": manual_summary.strip(),
        "three_ai_consensus": "Yes",
        "decision_timestamp": final_decision.get("timestamp", ""),
    }


def generate_final_csv(input_dir: str, original_csv: str, output_dir: str) -> None:
    """Generate final CSV with all decisions."""
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Read all final decision JSONs
    json_files = glob.glob(os.path.join(input_dir, "*.json"))
    logging.info(f"Found {len(json_files)} final decision files")
    
    decisions = {}
    for json_file in json_files:
        with open(json_file, "r", encoding="utf-8") as f:
            final_json = json.load(f)
            decision_data = extract_decision_fields(final_json)
            
            # Use unique_id or control_id as key
            key = decision_data["unique_id"] or decision_data["control_id"]
            decisions[key] = decision_data
    
    logging.info(f"Extracted {len(decisions)} decisions")
    
    # Read original CSV
    with open(original_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        original_rows = list(reader)
        original_fieldnames = reader.fieldnames
    
    logging.info(f"Read {len(original_rows)} rows from original CSV")
    
    # Merge with decisions
    new_fieldnames = list(original_fieldnames) + [
        "final_approach",
        "final_confidence",
        "program_name",
        "justification",
        "automation_summary",
        "manual_summary",
        "three_ai_consensus",
        "decision_timestamp",
    ]
    
    updated_rows = []
    matched = 0
    unmatched = 0
    
    for row in original_rows:
        key = row.get("unique_id") or row.get("id") or row.get("control_id")
        
        if key in decisions:
            decision = decisions[key]
            row.update({
                "final_approach": decision["final_approach"],
                "final_confidence": decision["final_confidence"],
                "program_name": decision["program_name"],
                "justification": decision["justification"],
                "automation_summary": decision["automation_summary"],
                "manual_summary": decision["manual_summary"],
                "three_ai_consensus": decision["three_ai_consensus"],
                "decision_timestamp": decision["decision_timestamp"],
            })
            matched += 1
        else:
            # No decision found
            row.update({
                "final_approach": "",
                "final_confidence": "",
                "program_name": "",
                "justification": "",
                "automation_summary": "",
                "manual_summary": "",
                "three_ai_consensus": "",
                "decision_timestamp": "",
            })
            unmatched += 1
        
        updated_rows.append(row)
    
    logging.info(f"Matched: {matched}, Unmatched: {unmatched}")
    
    # Write final CSV
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    final_csv_path = os.path.join(output_dir, f"aws_controls_FINAL_{timestamp}.csv")
    
    with open(final_csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=new_fieldnames)
        writer.writeheader()
        writer.writerows(updated_rows)
    
    logging.info(f"✅ Final CSV: {final_csv_path}")
    
    # Generate summary CSVs
    automated_rows = [r for r in updated_rows if r.get("final_approach", "").lower() == "automated"]
    manual_rows = [r for r in updated_rows if r.get("final_approach", "").lower() == "manual"]
    high_conf_rows = [r for r in updated_rows if r.get("final_confidence", "").upper() == "HIGH"]
    
    auto_csv = os.path.join(output_dir, f"aws_automated_{timestamp}.csv")
    with open(auto_csv, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=new_fieldnames)
        writer.writeheader()
        writer.writerows(automated_rows)
    
    manual_csv = os.path.join(output_dir, f"aws_manual_{timestamp}.csv")
    with open(manual_csv, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=new_fieldnames)
        writer.writeheader()
        writer.writerows(manual_rows)
    
    high_csv = os.path.join(output_dir, f"aws_high_confidence_{timestamp}.csv")
    with open(high_csv, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=new_fieldnames)
        writer.writeheader()
        writer.writerows(high_conf_rows)
    
    # Program names list
    program_names = sorted(set(r["program_name"] for r in automated_rows if r.get("program_name")))
    programs_file = os.path.join(output_dir, f"aws_program_names_{timestamp}.txt")
    with open(programs_file, "w", encoding="utf-8") as f:
        f.write("# AWS Compliance Program Names\n\n")
        for name in program_names:
            f.write(f"{name}\n")
    
    # Summary report
    summary_file = os.path.join(output_dir, f"AWS_SUMMARY_{timestamp}.md")
    with open(summary_file, "w", encoding="utf-8") as f:
        f.write(f"""# AWS Compliance Audit Summary

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## 📊 Results

- **Total Controls:** {len(updated_rows)}
- **Automated:** {len(automated_rows)} ({len(automated_rows)*100//len(updated_rows) if updated_rows else 0}%)
- **Manual:** {len(manual_rows)} ({len(manual_rows)*100//len(updated_rows) if updated_rows else 0}%)
- **High Confidence:** {len(high_conf_rows)} ({len(high_conf_rows)*100//len(updated_rows) if updated_rows else 0}%)
- **Program Names:** {len(program_names)}

## 📁 Output Files

1. **Main CSV:** `{os.path.basename(final_csv_path)}`
2. **Automated Only:** `{os.path.basename(auto_csv)}`
3. **Manual Only:** `{os.path.basename(manual_csv)}`
4. **High Confidence:** `{os.path.basename(high_csv)}`
5. **Program Names:** `{os.path.basename(programs_file)}`

## ✅ Status

Three-AI pipeline completed successfully for AWS compliance controls.
""")
    
    logging.info("=" * 80)
    logging.info("✅ Step 4 Complete - CSV Generation")
    logging.info(f"   Total: {len(updated_rows)}")
    logging.info(f"   Automated: {len(automated_rows)}")
    logging.info(f"   Manual: {len(manual_rows)}")
    logging.info(f"   High Confidence: {len(high_conf_rows)}")
    logging.info(f"   Program Names: {len(program_names)}")
    logging.info(f"   Output Dir: {output_dir}")
    logging.info("=" * 80)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="AWS Compliance Agent - Step 4: CSV Generation")
    parser.add_argument(
        "--input-dir",
        required=True,
        help="Directory with Step 3 final decision outputs"
    )
    parser.add_argument(
        "--original-csv",
        default="aws_controls.csv",
        help="Original AWS compliance CSV"
    )
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    default_output = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        f"output_final_{timestamp}"
    )
    
    parser.add_argument(
        "--output-dir",
        default=default_output,
        help="Directory for final CSV outputs"
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    generate_final_csv(
        input_dir=args.input_dir,
        original_csv=args.original_csv,
        output_dir=args.output_dir,
    )
