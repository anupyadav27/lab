import json
import sys
from pathlib import Path


def make_row_key(row):
    return (
        row.get("service", ""),
        row.get("resource", ""),
        row.get("adapter", ""),
        row.get("assertion_id", ""),
    )


def dedupe_matrix(in_path: Path, out_path: Path) -> tuple[int, int]:
    with in_path.open("r") as f:
        data = json.load(f)

    matrix = data.get("matrix", {})
    removed = 0
    kept = 0

    for bucket, checks in list(matrix.items()):
        seen = set()
        new_checks = []
        for row in checks:
            key = make_row_key(row)
            if key in seen:
                removed += 1
                continue
            seen.add(key)
            new_checks.append(row)
        kept += len(new_checks)
        matrix[bucket] = new_checks

    data["matrix"] = matrix
    data["total_checks"] = sum(len(v) for v in matrix.values())
    with out_path.open("w") as f:
        json.dump(data, f, indent=2)
    return kept, removed


def main():
    if len(sys.argv) < 3:
        print("Usage: dedupe_matrix_by_keys.py <in_json> <out_json>")
        sys.exit(1)
    in_path = Path(sys.argv[1])
    out_path = Path(sys.argv[2])
    kept, removed = dedupe_matrix(in_path, out_path)
    print(f"Deduped. Kept: {kept}, Removed: {removed}")


if __name__ == "__main__":
    main()


