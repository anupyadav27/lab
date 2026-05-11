#!/usr/bin/env python3
import json
import os
from datetime import datetime
from typing import Any, Dict, List, Tuple

BASE_MATRIX_PATH = \
    "/Users/apple/Desktop/compliance_Database/rule-generator-engine/Step3-matrices-per-cloud-provider/aws_matrix_2025-09-11T20-00-38.json.backup"
ENRICHED_MATRIX_PATH = \
    "/Users/apple/Desktop/compliance_Database/rule-generator-engine/Step3-matrices-per-cloud-provider/aws_matrix_enriched_atomic_full_plus5_2025-09-24.json"
OUTPUT_MERGED_PATH = \
    "/Users/apple/Desktop/compliance_Database/rule-generator-engine/Step3-matrices-per-cloud-provider/aws_matrix_enriched_atomic_merged_2025-09-24.json"


def load_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_json_merge_dupe_keys(path: str) -> Dict[str, Any]:
    # Use object_pairs_hook to capture duplicates and merge arrays
    def hook(pairs):
        merged: Dict[str, Any] = {}
        for k, v in pairs:
            if k in merged:
                # If both are lists, concatenate
                if isinstance(merged[k], list) and isinstance(v, list):
                    merged[k].extend(v)
                # If existing is list and new is dict with tiers, flatten
                elif isinstance(merged[k], list) and isinstance(v, dict):
                    for tier, arr in v.items():
                        if isinstance(arr, list):
                            merged[k].extend(arr)
                # If existing is dict and new is list, flatten
                elif isinstance(merged[k], dict) and isinstance(v, list):
                    # Flatten any tiers inside existing dict
                    flat = []
                    for tier, arr in merged[k].items():
                        if isinstance(arr, list):
                            flat.extend(arr)
                    flat.extend(v)
                    merged[k] = flat
                # If both dicts, keep later (rare at top level here)
                else:
                    merged[k] = v
            else:
                merged[k] = v
        return merged

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f, object_pairs_hook=hook)


def save_json(path: str, data: Any) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def normalize_key(domain_subcat: str) -> str:
    return domain_subcat.strip()


def to_entries_map(matrix: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
    # Supports either tiered or flat list
    out: Dict[str, List[Dict[str, Any]]] = {}
    for k, v in matrix.items():
        key = normalize_key(k)
        if isinstance(v, list):
            out.setdefault(key, []).extend(v)
        elif isinstance(v, dict):
            for tier, arr in v.items():
                if isinstance(arr, list):
                    for e in arr:
                        e2 = dict(e)
                        e2.setdefault("coverage_tier", tier)
                        out.setdefault(key, []).append(e2)
    return out


def signal_from_adapter(service: str, adapter: str, resource_type: str) -> Dict[str, Any]:
    a = (adapter or "").lower()
    s = (service or "").lower()
    # Minimal enriched heuristics reused
    if "s3.public_access_block" in a:
        return {
            "fields": [
                "blockPublicAcls", "ignorePublicAcls", "blockPublicPolicy", "restrictPublicBuckets"
            ],
            "predicate": "blockPublicAcls === true && ignorePublicAcls === true && blockPublicPolicy === true && restrictPublicBuckets === true",
            "paths_doc": ["S3:GetPublicAccessBlock -> PublicAccessBlockConfiguration"],
            "evidence_type": "config_read",
        }
    if "s3.bucket_encryption" in a or "bucket_encryption" in a:
        return {
            "fields": ["serverSideEncryption.enabled", "serverSideEncryption.kmsKeyId"],
            "predicate": "serverSideEncryption.enabled === true",
            "paths_doc": ["S3:GetBucketEncryption -> ServerSideEncryptionConfiguration"],
            "evidence_type": "config_read",
        }
    if "cloudtrail" in a and ("log_collection" in a or "audit_logging" in a):
        return {
            "fields": ["trail.enabled", "trail.multiRegion", "trail.logFileValidation"],
            "predicate": "trail.enabled === true && trail.multiRegion === true && trail.logFileValidation === true",
            "paths_doc": ["CloudTrail:DescribeTrails", "CloudTrail:GetTrailStatus"],
            "evidence_type": "config_read",
        }
    if ".kms." in a and ("rotation" in a):
        return {
            "fields": ["rotationEnabled"],
            "predicate": "rotationEnabled === true",
            "paths_doc": ["KMS:GetKeyRotationStatus"],
            "evidence_type": "config_read",
        }
    if "elbv2" in a and ("ssl" in a or "listeners" in a):
        return {
            "fields": ["listeners[].protocol", "listeners[].sslPolicy"],
            "predicate": "listeners.every(l => l.protocol === 'HTTPS')",
            "paths_doc": ["ELBv2:DescribeListeners"],
            "evidence_type": "config_read",
        }
    # Fallback
    return {
        "fields": ["compliant"],
        "predicate": "compliant === true",
        "paths_doc": [f"{s.upper()}:Describe* or Get* for {resource_type}"],
        "evidence_type": "config_read",
    }


def enrich_entry_defaults(entry: Dict[str, Any]) -> Dict[str, Any]:
    e = dict(entry)
    e.setdefault("coverage_tier", "core")
    e.setdefault("params", {})
    if "signal" not in e:
        sig = signal_from_adapter(e.get("service"), e.get("adapter") or e.get("adapter_id"), e.get("resource_type") or e.get("resource"))
        e["signal"] = sig
    return e


def merge() -> Dict[str, Any]:
    base = load_json_merge_dupe_keys(BASE_MATRIX_PATH)
    enriched_root = load_json(ENRICHED_MATRIX_PATH)

    base_map = to_entries_map(base)
    cur_map = enriched_root.get("matrix") or to_entries_map(enriched_root)

    merged: Dict[str, List[Dict[str, Any]]] = {k: [dict(x) for x in v] for k, v in cur_map.items()}

    def entry_key(e: Dict[str, Any]) -> Tuple[str, str, str]:
        return (
            (e.get("service") or "").lower(),
            (e.get("resource") or e.get("resource_type") or "").lower(),
            (e.get("adapter") or e.get("adapter_id") or "").lower(),
        )

    for domain_subcat, base_entries in base_map.items():
        existing = merged.setdefault(domain_subcat, [])
        seen = {entry_key(x) for x in existing}
        for be in base_entries:
            k = entry_key(be)
            if k in seen:
                continue
            merged[domain_subcat].append(enrich_entry_defaults(be))
            seen.add(k)

    out = {
        "provider": "aws",
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "source_base": os.path.basename(BASE_MATRIX_PATH),
        "source_enriched": os.path.basename(ENRICHED_MATRIX_PATH),
        "matrix": merged,
    }
    return out


def main() -> None:
    data = merge()
    save_json(OUTPUT_MERGED_PATH, data)
    total = sum(len(v) for v in data.get("matrix", {}).values())
    print(f"Wrote merged enriched matrix with {total} rows to {OUTPUT_MERGED_PATH}")


if __name__ == "__main__":
    main()
