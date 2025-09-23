#!/usr/bin/env python3
"""
Build an AWS cleanup TODO list from a function list comparison JSON.

- Reads only_in_unique from the source JSON
- Strips backticks
- Classifies provider by prefix heuristics
- Proposes action:
  - delete_non_aws for non-AWS
  - review for AWS/unknown (for later dedupe/rename/consolidation)
- Writes a progress-tracking TODO JSON with per-item status fields

Usage:
  python build_aws_cleanup_todo.py [--src <path_to_function_set_comparison.json>] [--outdir <output_dir>]
"""

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List

# Heuristic patterns to classify provider by function name prefix
PROVIDER_PATTERNS = {
    "azure": re.compile(r"^(azure_|aks_|app_service_|app_gateway_|blob_storage_)", re.IGNORECASE),
    "gcp": re.compile(r"^(gke_|app_engine_|artifact_registry_|security_command_center_|cloud_cdn_|cloud_dns_|cloud_function_|cloud_deploy_|cloud_nat_gateway_)", re.IGNORECASE),
    "k8s": re.compile(r"^(k8s_|kubernetes_)", re.IGNORECASE),
    # AWS common services prefixes
    "aws": re.compile(r"^(aws_|ec2_|s3_|rds_|kms_|iam_|cloudtrail_|cloudwatch_|lambda_|redshift_|guardduty_|waf_|vpc_|route53_|eks_|ecs_|codebuild_|codepipeline_|ssm_|secretsmanager_|cloudfront_|batch_|backup_|appstream_|workspaces_)",
                       re.IGNORECASE),
}

# Some ambiguous/generic prefixes we want to flag for review even if they look cloud-y
AMBIGUOUS_PREFIXES = (
    "cloud_hsm_",   # AWS has CloudHSM; GCP has Cloud HSM
    "cloud_logging_",  # GCP Cloud Logging vs CloudWatch Logs
    "cloud_kms_",   # GCP KMS vs AWS KMS (we use kms_ for AWS)
    "cloud_load_balancer_",  # Could be various providers
    "cloud_account_",
    "cloud_diagram_",
    "cloud_dr_",
    "cloud_dlp_",
    "cloud_deployment_",
)


def classify_provider(name: str) -> str:
    n = name.lower()
    for provider, pattern in PROVIDER_PATTERNS.items():
        if pattern.match(n):
            return provider
    # Flag ambiguous as unknown for manual review
    if any(n.startswith(p) for p in AMBIGUOUS_PREFIXES):
        return "unknown"
    return "aws" if n.startswith("cloudtrail_") or n.startswith("cloudwatch_") or n.startswith("secrets_manager_") else "unknown"


def build_todo_items(function_names: List[str]) -> List[Dict]:
    items = []
    for raw in function_names:
        # Normalize and strip markdown-style backticks/quotes
        name = str(raw).strip().strip('`').strip('"')
        if not name:
            continue
        provider = classify_provider(name)
        if provider == "aws":
            proposed_action = "review"  # further dedupe/consolidation/rename will be handled later
        elif provider in ("azure", "gcp", "k8s"):
            proposed_action = "delete_non_aws"
        else:
            proposed_action = "review"

        items.append({
            "function_name": name,
            "provider_guess": provider,
            "proposed_action": proposed_action,
            "status": "todo",           # can be: todo | in_progress | done | skipped
            "canonical_name": None,      # fill if rename decided
            "consolidate_into": None,    # fill if consolidation decided
            "notes": "auto-classified; update as you progress"
        })
    return items


def main():
    parser = argparse.ArgumentParser(description="Build AWS cleanup TODO list from function set comparison JSON")
    parser.add_argument("--src", default=str(Path(__file__).parents[2] / "etl-job_mapping _final_fn_name_generator" / "fn_list_finalisation" / "aws" / "complete_fn_list" / "function_set_comparison.json"), help="Path to function_set_comparison.json")
    parser.add_argument("--outdir", default=str(Path(__file__).parents[2] / "etl-job_mapping _final_fn_name_generator" / "fn_list_finalisation" / "aws" / "complete_fn_list"), help="Directory to write TODO file into")
    args = parser.parse_args()

    src_path = Path(args.src)
    if not src_path.exists():
        print(f"ERROR: Source file not found: {src_path}")
        return 2

    try:
        data = json.loads(src_path.read_text())
    except Exception as e:
        print(f"ERROR: Failed to read/parse JSON: {src_path}: {e}")
        return 3

    if "only_in_unique" not in data or not isinstance(data["only_in_unique"], list):
        print("ERROR: JSON missing only_in_unique array")
        return 4

    raw_functions = data["only_in_unique"]
    items = build_todo_items(raw_functions)

    # Summaries
    counts_by_provider: Dict[str, int] = {}
    for it in items:
        counts_by_provider[it["provider_guess"]] = counts_by_provider.get(it["provider_guess"], 0) + 1

    delete_non_aws_count = sum(1 for it in items if it["proposed_action"] == "delete_non_aws")
    review_count = sum(1 for it in items if it["proposed_action"] == "review")

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = outdir / f"aws_function_cleanup_todo_{ts}.json"

    output = {
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "provider": "aws",
            "source_file": str(src_path),
            "classification_rule_doc": {
                "azure": "^(azure_|aks_|app_service_|app_gateway_|blob_storage_)",
                "gcp": "^(gke_|app_engine_|artifact_registry_|security_command_center_|cloud_cdn_|cloud_dns_|cloud_function_|cloud_deploy_|cloud_nat_gateway_)",
                "k8s": "^(k8s_|kubernetes_)",
                "aws": "^(aws_|ec2_|s3_|rds_|kms_|iam_|cloudtrail_|cloudwatch_|lambda_|redshift_|guardduty_|waf_|vpc_|route53_|eks_|ecs_|codebuild_|codepipeline_|ssm_|secretsmanager_|cloudfront_|batch_|backup_|appstream_|workspaces_)",
                "ambiguous_prefixes": list(AMBIGUOUS_PREFIXES),
            }
        },
        "summary": {
            "total_items": len(items),
            "counts_by_provider": counts_by_provider,
            "delete_non_aws": delete_non_aws_count,
            "review": review_count
        },
        "items": items
    }

    out_path.write_text(json.dumps(output, indent=2))

    print(f"TODO written: {out_path}")
    print("Summary:")
    for prov, cnt in sorted(counts_by_provider.items()):
        print(f"  {prov or 'unknown'}: {cnt}")
    print(f"  delete_non_aws: {delete_non_aws_count}")
    print(f"  review: {review_count}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
