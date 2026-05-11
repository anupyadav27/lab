#!/usr/bin/env python3
"""
Extract compliance, title, and section from CIS AWS benchmark JSON files.
Outputs to CSV for easy consumption.
"""

import json
import csv
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent
OUTPUT_CSV = OUTPUT_DIR / "cis_metadata_extracted.csv"


def get_compliance_from_filename(filename: str) -> str:
    """Derive compliance/benchmark name from JSON filename."""
    # e.g., CIS_AWS_Storage_Services_Benchmark_v1.0.0.json
    # -> CIS AWS Storage Services Benchmark v1.0.0
    name = Path(filename).stem
    # Replace underscores with spaces, keep version as-is
    return name.replace("_", " ")


def extract_from_json(json_path: Path) -> list[dict]:
    """Extract compliance, title, section from a CIS JSON file."""
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        return []
    compliance = get_compliance_from_filename(json_path.name)
    rows = []
    for item in data:
        rows.append({
            "compliance": compliance,
            "section": item.get("section", ""),
            "id": item.get("id", ""),
            "title": item.get("title", ""),
        })
    return rows


def main():
    all_rows = []
    for json_file in sorted(OUTPUT_DIR.glob("*.json")):
        if json_file.name == "cis_metadata_extracted.csv":
            continue
        try:
            rows = extract_from_json(json_file)
            all_rows.extend(rows)
            print(f"  {json_file.name}: {len(rows)} controls")
        except Exception as e:
            print(f"  ERROR {json_file.name}: {e}")

    # Write CSV
    if all_rows:
        with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["compliance", "section", "id", "title"])
            w.writeheader()
            w.writerows(all_rows)
        print(f"\nWritten: {OUTPUT_CSV}")
        print(f"Total: {len(all_rows)} controls")
    else:
        print("No data extracted.")


if __name__ == "__main__":
    main()
