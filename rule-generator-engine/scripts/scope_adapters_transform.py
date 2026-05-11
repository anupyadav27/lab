import json
import sys
from pathlib import Path


def derive_scoped_adapter(service: str, resource: str, adapter: str) -> str:
    # adapter like aws.<service>.<slug> -> make aws.<service>.<resource_short>.<slug>
    try:
        parts = adapter.split(".")
        if len(parts) < 3 or parts[0] != "aws":
            return adapter
        slug = ".".join(parts[2:])  # keep any nested slug
    except Exception:
        return adapter

    # resource like iam.user or s3.bucket
    resource_short = resource.split(".", 1)[1] if "." in resource else resource
    # Avoid duplicating resource name if slug already starts with it
    if slug.startswith(f"{resource_short}."):
        return f"aws.{service}.{slug}"
    return f"aws.{service}.{resource_short}.{slug}"


def transform_matrix(in_path: Path, out_path: Path) -> int:
    with in_path.open("r") as f:
        data = json.load(f)

    matrix = data.get("matrix", {})
    updated = 0
    for bucket, checks in matrix.items():
        for row in checks:
            service = row.get("service")
            resource = row.get("resource")
            adapter = row.get("adapter")
            if not service or not resource or not adapter:
                continue

            scoped = derive_scoped_adapter(service, resource, adapter)
            if scoped != adapter:
                row["adapter"] = scoped
                # also rebuild rule_id if present
                adapter_slug = scoped.split(".", 2)[-1]
                signal_slug = row.get("signal_slug")
                base_rule = f"aws.{service}.{resource}.{adapter_slug}"
                row["rule_id"] = base_rule + (f".{signal_slug}" if signal_slug else "")
                updated += 1

    # Second pass: ensure adapter uniqueness by appending assertion tail for remaining duplicates
    usage = {}
    for bucket, checks in matrix.items():
        for row in checks:
            a = row.get("adapter")
            usage.setdefault(a, 0)
            usage[a] += 1

    duplicates = {a for a, c in usage.items() if c > 1}
    if duplicates:
        # Build assertion tail slug per row
        for bucket, checks in matrix.items():
            for row in checks:
                adapter = row.get("adapter")
                if adapter not in duplicates:
                    continue
                assertion_id = row.get("assertion_id", "")
                # tail is text after last dot
                tail = assertion_id.split(".")[-1] if assertion_id else "assertion"
                tail = tail.replace("-", "_")
                # Only append if not already present
                if not adapter.endswith(f".{tail}"):
                    new_adapter = f"{adapter}.{tail}"
                    row["adapter"] = new_adapter
                    # rebuild rule_id accordingly
                    service = row.get("service")
                    resource = row.get("resource")
                    adapter_slug = new_adapter.split(".", 2)[-1]
                    signal_slug = row.get("signal_slug")
                    base_rule = f"aws.{service}.{resource}.{adapter_slug}"
                    row["rule_id"] = base_rule + (f".{signal_slug}" if signal_slug else "")
                    updated += 1

    # Third pass: if still duplicates, append domain.subcat tail from bucket
    usage2 = {}
    for bucket, checks in matrix.items():
        for row in checks:
            a = row.get("adapter")
            usage2.setdefault(a, 0)
            usage2[a] += 1
    duplicates2 = {a for a, c in usage2.items() if c > 1}
    if duplicates2:
        for bucket, checks in matrix.items():
            domain_tail = bucket.split(".")[-1] if "." in bucket else bucket
            domain_tail = domain_tail.replace("-", "_")
            for row in checks:
                adapter = row.get("adapter")
                if adapter not in duplicates2:
                    continue
                if not adapter.endswith(f".{domain_tail}"):
                    new_adapter = f"{adapter}.{domain_tail}"
                    row["adapter"] = new_adapter
                    service = row.get("service")
                    resource = row.get("resource")
                    adapter_slug = new_adapter.split(".", 2)[-1]
                    signal_slug = row.get("signal_slug")
                    base_rule = f"aws.{service}.{resource}.{adapter_slug}"
                    row["rule_id"] = base_rule + (f".{signal_slug}" if signal_slug else "")
                    updated += 1

    data["matrix"] = matrix
    with out_path.open("w") as f:
        json.dump(data, f, indent=2)
    return updated


def main():
    if len(sys.argv) < 3:
        print("Usage: scope_adapters_transform.py <in_json> <out_json>")
        sys.exit(1)
    in_path = Path(sys.argv[1])
    out_path = Path(sys.argv[2])
    updated = transform_matrix(in_path, out_path)
    print(f"Scoped adapters updated: {updated}")


if __name__ == "__main__":
    main()


