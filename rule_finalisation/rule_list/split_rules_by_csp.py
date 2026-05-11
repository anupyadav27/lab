"""Split consolidated rules CSV into one file per CSP.

Keeps only the columns relevant to each CSP (rule identity + that CSP's
compliance mappings), so the per-CSP files aren't bloated with empty columns
from the other six providers.
"""

import csv
from datetime import date
from pathlib import Path

SRC = Path(__file__).parent / "consolidated_rules_phase4_2025-11-08_FINAL_WITH_ALL_IDS.csv"
OUT_DIR = Path(__file__).parent / f"rules_by_csp_{date.today().isoformat()}"

IDENTITY_COLS = [
    "cloud_provider", "rule_id", "uniform_rule_format",
    "service", "category", "provider_service",
]


def main() -> None:
    OUT_DIR.mkdir(exist_ok=True)
    with open(SRC, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows_by_csp: dict[str, list[dict]] = {}
        for row in reader:
            rows_by_csp.setdefault(row["cloud_provider"], []).append(row)

    for csp, rows in rows_by_csp.items():
        prefix = "oci" if csp == "oci" else csp  # rule CSV uses "oci" for oracle
        cols = IDENTITY_COLS + [
            f"{prefix}_mapped_compliance_functions",
            f"{prefix}_mapped_compliance_ids",
        ]
        out_path = OUT_DIR / f"{csp}_rules.csv"
        with open(out_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(rows)
        print(f"{csp:10s} {len(rows):>5} rows -> {out_path.name}")


if __name__ == "__main__":
    main()
