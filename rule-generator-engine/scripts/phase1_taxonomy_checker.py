#!/usr/bin/env python3
import sys, json, argparse, pathlib, csv

DEFAULT_TARGETS = {
  "Performance & Availability": 10,
  "Multi-tenant Controls": 6,
  "Network & Exposure": 10,
  "Data Governance & Privacy": 10,
}

CANON_DOMAINS = [
  "Identity & Authentication",
  "Authorization",
  "Secrets & Cryptography",
  "Network & Exposure",
  "Audit & Monitoring",
  "Configuration Baseline & Hardening",
  "Backup, Recovery & DR",
  "Governance & Operations",
  "Performance & Availability",
  "Data Governance & Privacy",
  "Multi-tenant Controls",
]

def load(fp: pathlib.Path):
    return json.loads(fp.read_text())

def main():
    ap = argparse.ArgumentParser(description='Phase-1 taxonomy checker')
    ap.add_argument('file', help='taxonomy JSON path')
    ap.add_argument('--csv-out', help='emit domain,risk_id,title CSV to this path')
    ap.add_argument('--fail-uncategorized', action='store_true', default=True)
    ap.add_argument('--targets', help='JSON object of domain->min_count overrides')
    args = ap.parse_args()

    fp = pathlib.Path(args.file)
    obj = load(fp)

    # Gather domains
    domains = obj.get('domains', [])
    domain_counts = {}
    uncategorized = None
    rows = []
    for d in domains:
        name = d.get('domain', '')
        subs = d.get('subcategories', [])
        domain_counts[name] = len(subs)
        if name.lower().startswith('uncategorized'):
            uncategorized = d
        for s in subs:
            rows.append((name, s.get('risk_id',''), s.get('title','')))

    # CSV output
    if args.csv_out:
        with open(args.csv_out, 'w', newline='') as f:
            w = csv.writer(f)
            w.writerow(['domain','risk_id','title'])
            w.writerows(rows)

    # Enforce canon domains presence
    missing = [d for d in CANON_DOMAINS if d not in domain_counts]

    # Targets
    targets = DEFAULT_TARGETS.copy()
    if args.targets:
        try:
            targets.update(json.loads(args.targets))
        except Exception as e:
            print('Invalid targets JSON:', e, file=sys.stderr)

    # Evaluate
    errors = []
    warnings = []
    if args.fail_uncategorized and uncategorized and uncategorized.get('subcategories'):
        errors.append(f"Uncategorized has {len(uncategorized['subcategories'])} items")

    for dom, minv in targets.items():
        count = domain_counts.get(dom, 0)
        if count < minv:
            warnings.append(f"Domain '{dom}' below target: {count} < {minv}")

    if missing:
        warnings.append('Missing canonical domains: ' + ', '.join(missing))

    # Print summary
    print('Domain counts:')
    for k in sorted(domain_counts):
        print(f"- {k}: {domain_counts[k]}")
    if warnings:
        print('\nWarnings:')
        for w in warnings:
            print('-', w)
    if errors:
        print('\nErrors:')
        for e in errors:
            print('-', e)
        sys.exit(2)

if __name__ == '__main__':
    main()
