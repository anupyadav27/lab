#!/usr/bin/env python3
import json
import os
from datetime import datetime
from typing import Any, Dict, List, Tuple

MATRIX_PATH = \
    "/Users/apple/Desktop/compliance_Database/rule-generator-engine/Step3-matrices-per-cloud-provider/azure_matrix_2025-01-09_enriched_complete_final_with_taxonomy.json"
ASSERTIONS_PATH = \
    "/Users/apple/Desktop/compliance_Database/rule-generator-engine/step-2-common-assercian-id/assertions_pack_final_2025-09-11T18-41-14_enhanced.json"
OUTPUT_PATH = \
    "/Users/apple/Desktop/compliance_Database/rule-generator-engine/step4-rune-per-cloud-provider/azure_rules_generated_2025-09-24.json"


def load_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def flatten_matrix(matrix: Dict[str, Dict[str, List[Dict[str, Any]]]]) -> List[Tuple[str, str, Dict[str, Any]]]:
    items: List[Tuple[str, str, Dict[str, Any]]] = []
    # matrix is like {"domain.subcat": {"core": [...], "extended": [...]}}
    for domain_subcat, tiers in matrix.items():
        if "." in domain_subcat:
            domain_key, subcat_id = domain_subcat.split(".", 1)
        else:
            domain_key, subcat_id = domain_subcat, ""
        for coverage_tier, entries in tiers.items():
            if not isinstance(entries, list):
                continue
            for entry in entries:
                entry_copy = dict(entry)
                entry_copy["coverage_tier"] = coverage_tier
                items.append((domain_key, subcat_id, entry_copy))
    return items


def index_assertions_by_domain_subcat(assertions_root: Dict[str, Any]) -> Dict[Tuple[str, str], List[Dict[str, Any]]]:
    by_key: Dict[Tuple[str, str], List[Dict[str, Any]]] = {}
    assertions = assertions_root.get("assertions") or assertions_root.get("data") or []
    for a in assertions:
        assert_id = a.get("assertion_id")
        subref = a.get("subcat_ref") or {}
        domain_key = subref.get("domain_key")
        subcat_id = subref.get("subcat_id")
        if not domain_key or not subcat_id or not assert_id:
            continue
        by_key.setdefault((domain_key, subcat_id), []).append(a)
    return by_key


def derive_rule_from_pair(provider: str, domain_key: str, subcat_id: str, matrix_entry: Dict[str, Any], assertion: Dict[str, Any]) -> Dict[str, Any]:
    adapter = matrix_entry.get("adapter") or matrix_entry.get("adapter_id") or ""
    service = matrix_entry.get("service") or (adapter.split(".")[1] if "." in adapter else "")
    resource_type = matrix_entry.get("resource_type") or matrix_entry.get("resource") or ""

    rule_id = f"{adapter}.{assertion['assertion_id'].split('.')[-1]}" if adapter else f"azure.{service}.{resource_type}.{assertion['assertion_id'].split('.')[-1]}"

    rule: Dict[str, Any] = {
        "rule_id": rule_id,
        "assertion_id": assertion["assertion_id"],
        "provider": provider,
        "service": service or "",
        "resource_type": resource_type,
        "adapter": adapter,
        "params": assertion.get("params") or {},
        "pass_condition": "resource.compliant == true",
        "severity": matrix_entry.get("severity") or assertion.get("severity") or "medium",
        "coverage_tier": matrix_entry.get("coverage_tier") or "core",
        "not_applicable_when": matrix_entry.get("not_applicable_when"),
        "evidence_type": (matrix_entry.get("signal") or {}).get("evidence_type") or "config_read",
        "rationale": f"Azure {service} security compliance check for {subcat_id}",
        "adapter_spec": {
            "returns": {
                "compliant": "boolean - whether the resource is compliant",
                "details": "object - compliance check details",
            }
        },
        "notes": f"Generated on {datetime.utcnow().isoformat()}Z"
    }
    return rule


def generate_rules() -> Dict[str, Any]:
    matrix = load_json(MATRIX_PATH)
    assertions_root = load_json(ASSERTIONS_PATH)

    matrix_items = flatten_matrix(matrix)
    assertions_by_key = index_assertions_by_domain_subcat(assertions_root)

    provider = "azure"
    rules: List[Dict[str, Any]] = []
    unmatched_matrix: List[Dict[str, Any]] = []
    unmatched_assertions: List[Dict[str, Any]] = []

    matched_assertion_ids = set()

    for domain_key, subcat_id, entry in matrix_items:
        key = (domain_key, subcat_id)
        matched_assertions = assertions_by_key.get(key, [])
        if not matched_assertions:
            unmatched_matrix.append({"domain_key": domain_key, "subcat_id": subcat_id, **entry})
            continue
        for assertion in matched_assertions:
            rules.append(derive_rule_from_pair(provider, domain_key, subcat_id, entry, assertion))
            matched_assertion_ids.add(assertion["assertion_id"])

    # Track assertions that had no matrix entries
    for (domain_key, subcat_id), assertion_list in assertions_by_key.items():
        # Check if any matrix item existed for this pair
        if not any((dk == domain_key and sc == subcat_id) for (dk, sc, _e) in matrix_items):
            for assertion in assertion_list:
                unmatched_assertions.append(assertion)

    out: Dict[str, Any] = {
        "provider": provider,
        "version": "3.0.0",
        "rule_count": len(rules),
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "rules": rules,
        "_meta": {
            "source_matrix": os.path.basename(MATRIX_PATH),
            "source_assertions": os.path.basename(ASSERTIONS_PATH),
            "unmatched_matrix_count": len(unmatched_matrix),
            "unmatched_assertions_count": len(unmatched_assertions)
        }
    }
    return out


def main() -> None:
    data = generate_rules()
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Wrote {len(data.get('rules', []))} rules to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
