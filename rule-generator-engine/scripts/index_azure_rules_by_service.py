#!/usr/bin/env python3
import json
from collections import defaultdict
from pathlib import Path
from typing import Dict, List

RULES_PATH = Path("/Users/apple/Desktop/compliance_Database/rule-generator-engine/step4-rune-per-cloud-provider/azure_rules_generated_2025-09-24.json")
OUTPUT_INDEX_PATH = Path("/Users/apple/Desktop/compliance_Database/rule-generator-engine/step4-rune-per-cloud-provider/azure_rules_index_by_service_2025-09-24.json")


def main() -> None:
    data = json.loads(RULES_PATH.read_text(encoding="utf-8"))
    rules: List[Dict] = data.get("rules", [])

    service_to_rule_ids: Dict[str, List[str]] = defaultdict(list)
    for r in rules:
        service = r.get("service") or "unknown"
        rid = r.get("rule_id")
        if rid:
            service_to_rule_ids[service].append(rid)

    # Sort services and rule_ids for readability
    sorted_index = {svc: sorted(rids) for svc, rids in sorted(service_to_rule_ids.items())}

    OUTPUT_INDEX_PATH.write_text(json.dumps(sorted_index, indent=2), encoding="utf-8")

    # Print a brief summary
    print("Services and counts:")
    for svc, rids in sorted_index.items():
        print(f"- {svc}: {len(rids)} rules")


if __name__ == "__main__":
    main()
