#!/usr/bin/env python3
"""
AWS Compliance Quality Check
Validates the quality of all decisions made by the three-AI pipeline.
"""

import argparse
import glob
import json
import logging
import re
from datetime import datetime
from typing import Dict, List


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def validate_program_name(name: str) -> Dict:
    """Validate AWS program name format."""
    issues = []
    
    if not name:
        return {"valid": False, "issues": ["Empty program name"]}
    
    # Check format: aws_<service>_<resource>_<intent>
    if not name.startswith("aws_"):
        issues.append("Must start with 'aws_'")
    
    if not re.match(r'^aws_[a-z0-9]+(_[a-z0-9]+)*$', name):
        issues.append("Must be snake_case with only lowercase letters, numbers, and underscores")
    
    parts = name.split("_")
    if len(parts) < 4:
        issues.append("Should have at least 4 parts: aws_<service>_<resource>_<intent>")
    
    # Check for common AWS services
    aws_services = ['s3', 'iam', 'ec2', 'vpc', 'rds', 'kms', 'cloudtrail', 'lambda', 'eks', 'ecs', 'sns', 'sqs']
    if len(parts) >= 2 and parts[1] not in aws_services and not any(svc in name for svc in aws_services):
        issues.append(f"Consider using standard AWS service names: {', '.join(aws_services[:8])}")
    
    return {"valid": len(issues) == 0, "issues": issues}


def check_decision_quality(json_path: str) -> Dict:
    """Check quality of a single decision."""
    
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    control_id = data.get("control_id", "Unknown")
    final_decision = data.get("step3_final_decision", {})
    
    issues = []
    warnings = []
    
    # Check if all steps completed
    if "step1_initial_assessment" not in data:
        issues.append("Missing Step 1 assessment")
    if "step2_review" not in data:
        issues.append("Missing Step 2 review")
    if "step3_final_decision" not in data:
        issues.append("Missing Step 3 final decision")
    
    # Check final decision fields
    approach = final_decision.get("final_approach", "")
    confidence = final_decision.get("confidence", "")
    program_name = final_decision.get("program_name", "")
    
    if approach not in ["Manual", "Automated"]:
        issues.append(f"Invalid approach: '{approach}' (must be Manual or Automated)")
    
    if confidence not in ["HIGH", "MEDIUM", "LOW"]:
        issues.append(f"Invalid confidence: '{confidence}' (must be HIGH, MEDIUM, or LOW)")
    
    # Validate program name for automated controls
    if approach == "Automated":
        if not program_name:
            issues.append("Automated control missing program name")
        else:
            name_validation = validate_program_name(program_name)
            if not name_validation["valid"]:
                issues.extend([f"Program name: {issue}" for issue in name_validation["issues"]])
    
    # Check for low confidence
    if confidence == "LOW":
        warnings.append("Low confidence decision - needs human review")
    
    return {
        "control_id": control_id,
        "valid": len(issues) == 0,
        "issues": issues,
        "warnings": warnings,
        "approach": approach,
        "confidence": confidence,
        "program_name": program_name,
    }


def run_quality_check(input_dir: str, output_file: str = None) -> None:
    """Run quality check on all final decisions."""
    
    json_files = glob.glob(f"{input_dir}/*.json")
    
    logging.info("=" * 80)
    logging.info("🔍 AWS Compliance Quality Check")
    logging.info(f"Input: {input_dir}")
    logging.info(f"Files: {len(json_files)}")
    logging.info("=" * 80)
    
    results = []
    total = len(json_files)
    valid = 0
    with_warnings = 0
    invalid = 0
    
    for json_file in json_files:
        result = check_decision_quality(json_file)
        results.append(result)
        
        if result["valid"]:
            valid += 1
            if result["warnings"]:
                with_warnings += 1
        else:
            invalid += 1
            logging.error(f"❌ {result['control_id']}: {', '.join(result['issues'])}")
    
    # Statistics
    automated = sum(1 for r in results if r["approach"] == "Automated")
    manual = sum(1 for r in results if r["approach"] == "Manual")
    high_conf = sum(1 for r in results if r["confidence"] == "HIGH")
    medium_conf = sum(1 for r in results if r["confidence"] == "MEDIUM")
    low_conf = sum(1 for r in results if r["confidence"] == "LOW")
    
    # Program name issues
    program_name_issues = [r for r in results if r["approach"] == "Automated" and not r["valid"]]
    
    # Generate report
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report = f"""
# AWS Compliance Quality Check Report

**Generated:** {timestamp}
**Input Directory:** {input_dir}

## 📊 Overall Quality

- **Total Controls:** {total}
- **Valid:** {valid} ({valid*100//total if total else 0}%)
- **With Warnings:** {with_warnings} ({with_warnings*100//total if total else 0}%)
- **Invalid:** {invalid} ({invalid*100//total if total else 0}%)

## 🎯 Decisions

- **Automated:** {automated} ({automated*100//total if total else 0}%)
- **Manual:** {manual} ({manual*100//total if total else 0}%)

## ⭐ Confidence

- **HIGH:** {high_conf} ({high_conf*100//total if total else 0}%)
- **MEDIUM:** {medium_conf} ({medium_conf*100//total if total else 0}%)
- **LOW:** {low_conf} ({low_conf*100//total if total else 0}%)

## ❌ Issues Found

### Invalid Decisions: {len([r for r in results if not r['valid']])}

"""
    
    for r in results:
        if not r["valid"]:
            report += f"\n**Control: {r['control_id']}**\n"
            for issue in r["issues"]:
                report += f"  - {issue}\n"
    
    report += f"\n\n### Warnings: {sum(len(r['warnings']) for r in results)}\n"
    
    for r in results:
        if r["warnings"]:
            report += f"\n**Control: {r['control_id']}**\n"
            for warning in r["warnings"]:
                report += f"  - ⚠️ {warning}\n"
    
    report += f"""

## ✅ Quality Pass Criteria

| Criteria | Target | Actual | Status |
|----------|--------|--------|--------|
| Valid Decisions | 100% | {valid*100//total if total else 0}% | {'✅' if valid == total else '❌'} |
| Automation Rate | >80% | {automated*100//total if total else 0}% | {'✅' if automated*100//total >= 80 else '❌'} |
| HIGH Confidence | >90% | {high_conf*100//total if total else 0}% | {'✅' if high_conf*100//total >= 90 else '❌'} |
| Program Name Errors | 0 | {len(program_name_issues)} | {'✅' if len(program_name_issues) == 0 else '❌'} |

## 📝 Recommendations

"""
    
    if invalid > 0:
        report += f"1. ❌ **Fix {invalid} invalid decisions** before proceeding\n"
    if low_conf > 0:
        report += f"2. ⚠️ **Review {low_conf} low confidence controls** manually\n"
    if len(program_name_issues) > 0:
        report += f"3. 🔧 **Fix {len(program_name_issues)} program name issues**\n"
    if automated*100//total < 80:
        report += f"4. 📈 **Increase automation rate** (current: {automated*100//total}%, target: >80%)\n"
    
    if invalid == 0 and low_conf == 0:
        report += "✅ **All quality checks passed! Ready for implementation.**\n"
    
    # Print to console
    print(report)
    
    # Save to file
    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(report)
        logging.info(f"📄 Report saved: {output_file}")
    
    logging.info("=" * 80)
    logging.info(f"✅ Quality Check Complete")
    logging.info(f"   Valid: {valid}/{total}")
    logging.info(f"   Automated: {automated} ({automated*100//total if total else 0}%)")
    logging.info(f"   HIGH Confidence: {high_conf} ({high_conf*100//total if total else 0}%)")
    logging.info("=" * 80)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="AWS Compliance Quality Check")
    parser.add_argument(
        "--input-dir",
        required=True,
        help="Directory with Step 3 final decision outputs"
    )
    parser.add_argument(
        "--output-file",
        default=None,
        help="Output file for quality report (optional)"
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run_quality_check(
        input_dir=args.input_dir,
        output_file=args.output_file,
    )
