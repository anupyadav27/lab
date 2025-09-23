#!/usr/bin/env python3
"""
Suggest AWS-equivalent canonical names for items marked provider_guess == "unknown"
inside the AWS cleanup TODO file, using the naming format `<service>_<resource>_<requirement>[_<qualifier>]`.

- Auto-detects the latest aws_function_cleanup_todo_*.json if --todo is not provided
- Generates suggestions and writes a sidecar file: aws_unknown_suggestions_TIMESTAMP.json
- Also updates the TODO file in-place by adding `suggested_canonical_name` and `suggestion_confidence`

Usage:
  python suggest_aws_equivalents_from_unknown.py [--todo <path_to_todo_json>] [--outdir <dir>]
"""

import argparse
import glob
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

THIS_DIR = Path(__file__).parent
DEFAULT_TODO_DIR = THIS_DIR.parent / "fn_list_finalisation" / "aws" / "complete_fn_list"


def find_latest_todo(tododir: Path) -> Path:
    candidates = sorted(tododir.glob("aws_function_cleanup_todo_*.json"))
    return candidates[-1] if candidates else None


def transform_unknown_to_aws(name: str) -> Tuple[str, float, str]:
    n = name.lower()
    # Normalize multiple underscores
    n = re.sub(r"__+", "_", n)

    # Heuristic mappings: (pattern, replacement_prefix, confidence, rationale)
    rules: List[Tuple[re.Pattern, str, float, str]] = [
        # API Gateway
        (re.compile(r"^api_gateway_(stage_|authorizer_|access_|logs_|.*)", re.I), "apigateway_", 0.85, "API Gateway -> apigateway_*"),
        # AppConfig
        (re.compile(r"^appconfig_", re.I), "appconfig_", 0.95, "AWS AppConfig"),
        # CloudFormation
        (re.compile(r"^cloudformation_", re.I), "cloudformation_", 0.95, "AWS CloudFormation"),
        # AWS Config
        (re.compile(r"^config_rule_", re.I), "config_rule_", 0.8, "AWS Config rule related"),
        (re.compile(r"^config_", re.I), "config_", 0.7, "AWS Config generic"),
        # IAM/Console
        (re.compile(r"^console_session_", re.I), "iam_console_session_", 0.85, "IAM console session controls"),
        # Compute -> EC2
        (re.compile(r"^compute_instance_", re.I), "ec2_instance_", 0.8, "Map generic compute instance -> EC2 instance"),
        (re.compile(r"^compute_vm_", re.I), "ec2_instance_", 0.75, "Map generic VM -> EC2 instance"),
        (re.compile(r"^compute_time_service_", re.I), "ec2_instance_time_service_", 0.7, "Time/NTP on EC2"),
        # Container -> EKS/ECS
        (re.compile(r"^container_image_.*env", re.I), "ecs_task_definition_", 0.75, "Secrets in container env -> ECS task definition"),
        (re.compile(r"^container_image_", re.I), "ecr_image_", 0.6, "Generic container image -> ECR image"),
        (re.compile(r"^container_cluster_", re.I), "eks_cluster_", 0.6, "Generic container cluster -> EKS cluster"),
        (re.compile(r"^container_node_", re.I), "eks_node_group_", 0.6, "Generic container node -> EKS node group"),
        # Lambda (Cloud Functions analogue)
        (re.compile(r"^cloud_functions_", re.I), "lambda_function_", 0.7, "GCP Cloud Functions analogue -> Lambda"),
        # Anti-malware generic -> EC2 or GuardDuty
        (re.compile(r"^anti_malware_solution_", re.I), "ec2_instance_antimalware_", 0.6, "Generic anti-malware -> EC2 instance control"),
        # Application secrets -> Secrets Manager
        (re.compile(r"^application_secret_", re.I), "secretsmanager_secret_", 0.7, "App secret -> Secrets Manager secret"),
        # Cloud audit generic -> CloudTrail/CloudWatch Logs (keep as cloudtrail_ when about admin/logs)
        (re.compile(r"^cloud_audit_log_", re.I), "cloudtrail_log_", 0.65, "Generic audit logs -> CloudTrail/CloudWatch"),
    ]

    for pat, prefix, conf, why in rules:
        if pat.match(n):
            # Replace the leading matched part with the target prefix, keep the rest
            m = pat.match(n)
            suffix = n[m.end():]
            # Special handling: if rule already includes part of the suffix (like "stage_") and we have double resource, normalize later
            suggestion = prefix + suffix
            suggestion = re.sub(r"__+", "_", suggestion).strip("_")
            return suggestion, conf, why

    # Default: no clear mapping
    return n, 0.3, "No clear AWS service mapping; needs manual review"


def build_suggestions(todo_path: Path) -> Dict:
    data = json.loads(todo_path.read_text())
    items = data.get("items", [])
    suggestions = []

    for it in items:
        if it.get("provider_guess") != "unknown":
            continue
        name = it.get("function_name")
        if not name:
            continue
        suggested, conf, why = transform_unknown_to_aws(name)

        # Write suggestion back to item (non-destructive fields)
        it["suggested_canonical_name"] = suggested
        it["suggestion_confidence"] = conf

        suggestions.append({
            "function_name": name,
            "suggested_canonical_name": suggested,
            "confidence": conf,
            "rationale": why
        })

    return {"data": data, "suggestions": suggestions}


def main():
    parser = argparse.ArgumentParser(description="Suggest AWS-equivalent canonical names for unknown items in the AWS cleanup TODO")
    parser.add_argument("--todo", help="Path to aws_function_cleanup_todo_*.json; defaults to latest in standard dir")
    parser.add_argument("--outdir", help="Directory to write the suggestions file", default=str(DEFAULT_TODO_DIR))
    args = parser.parse_args()

    todo_path = Path(args.todo) if args.todo else find_latest_todo(DEFAULT_TODO_DIR)
    if not todo_path or not todo_path.exists():
        print("ERROR: Could not find the TODO file. Provide --todo explicitly.")
        return 2

    result = build_suggestions(todo_path)
    data = result["data"]
    suggestions = result["suggestions"]

    # Save updated TODO (with suggestion fields)
    todo_backup = todo_path.with_suffix(todo_path.suffix + ".bak")
    todo_backup.write_text(todo_path.read_text())
    todo_path.write_text(json.dumps(data, indent=2))

    # Save suggestions sidecar
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    suggestions_path = outdir / f"aws_unknown_suggestions_{ts}.json"

    side_output = {
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "todo_file": str(todo_path),
            "total_unknown": sum(1 for it in data.get("items", []) if it.get("provider_guess") == "unknown"),
            "total_suggestions": len(suggestions)
        },
        "suggestions": suggestions
    }
    suggestions_path.write_text(json.dumps(side_output, indent=2))

    print(f"Updated TODO with suggestion fields: {todo_path}")
    print(f"Backup saved: {todo_backup}")
    print(f"Suggestions written: {suggestions_path}")
    print(f"Total suggestions: {len(suggestions)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
