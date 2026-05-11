"""
Pass 1 normalizer for consolidated_compliance_rules_FINAL.csv.

Fixes legacy PDF-extraction artifacts so the UI can render descriptions
and references as proper structured content (markdown / HTML).

What it changes:
  1. Inline bullets (`•`) -> newline + "- " (markdown bullet)
  2. Inline numbered lists in references (" 1. ... 2. ...") -> split list
  3. Broken URLs ("id_root-<space>user_...") -> whitespace stripped inside
     URL tokens in references
  4. Numbered-list sentences in descriptions ("1) ... 2) ...") -> newline-
     separated items when a sequence is detected
  5. Separators standardized to "; " across multi-value mapping columns
     (handles legacy ":" separator in *_mapped_rules)
  6. Collapse runs of whitespace, trim trailing whitespace

Smart punctuation (em-dash, curly quotes, ellipsis) is preserved. Most
modern web stacks handle it fine, and normalizing loses fidelity.

Run:
    python3 clean_compliance_csv.py           # dry-run (prints diff stats)
    python3 clean_compliance_csv.py --write   # writes *_CLEAN.csv
"""

import csv
import re
import sys
from datetime import date
from pathlib import Path

SRC = Path(__file__).parent / "consolidated_compliance_rules_FINAL.csv"
DST = Path(__file__).parent / f"consolidated_compliance_rules_FINAL_CLEAN_{date.today().isoformat()}.csv"

MAPPING_COLS = [
    "aws_mapped_rules", "azure_mapped_rules", "gcp_mapped_rules",
    "oci_mapped_rules", "ibm_mapped_rules", "k8s_mapped_rules",
    "aws_mapped_compliance_ids", "azure_mapped_compliance_ids",
    "gcp_mapped_compliance_ids", "oci_mapped_compliance_ids",
    "ibm_mapped_compliance_ids", "k8s_mapped_compliance_ids",
    "aws_mapped_functions", "azure_mapped_functions",
    "gcp_mapped_functions", "ibm_mapped_functions",
]

def fix_bullets(text: str) -> str:
    if "•" not in text:
        return text
    # "intro: • item • item" -> "intro:\n- item\n- item"
    text = re.sub(r"\s*•\s*", "\n- ", text)
    # Tidy a leading "\n- " that attaches to a colon line
    text = re.sub(r":\s*\n- ", ":\n- ", text)
    return text


def fix_description_numbered_list(text: str) -> str:
    # Only act when 2+ sequential markers exist — avoid touching "CIS 2.1.7".
    # Matches "1) "/"1. " after ": " or " " boundaries.
    marker_re = re.compile(r"(?<=[\s:])(\d+)[\.\)]\s")
    markers = marker_re.findall(text)
    if len(markers) < 2:
        return text
    # Confirm it's a list: markers form 1,2,3... sequence
    try:
        nums = [int(m) for m in markers]
    except ValueError:
        return text
    if nums[:3] != list(range(nums[0], nums[0] + len(nums[:3]))):
        return text
    return marker_re.sub(lambda m: f"\n{m.group(1)}. ", text)


def _repair_url_linewrap(item: str) -> str:
    """Remove soft-wrap whitespace inside a URL token.

    PDF extracts produced things like `id_root- user_manage_mfa` where the
    space is a wrap artifact. Only touches whitespace that lives inside the
    URL itself, never between URL and following text.
    """
    def _fix(m: re.Match) -> str:
        # Walk forward char by char from the URL start, absorbing whitespace
        # only when the next non-ws char looks like URL continuation.
        url = m.group(0)
        out, i = [], 0
        while i < len(url):
            c = url[i]
            if c.isspace():
                j = i
                while j < len(url) and url[j].isspace():
                    j += 1
                # If next non-ws char is URL-safe, absorb the whitespace
                if j < len(url) and re.match(r"[A-Za-z0-9_\-./?#=&%+]", url[j]):
                    i = j
                    continue
                break
            out.append(c)
            i += 1
        return "".join(out) + url[i:]
    return re.sub(r"https?://\S.*", _fix, item)


def fix_references(text: str) -> str:
    if not text:
        return text
    # Split "1. X 2. Y 3. Z" into lines using lookahead so the marker stays.
    parts = re.split(r"(?<=\s)(?=\d+\.\s)", " " + text)
    if len(parts) < 2:
        return _repair_url_linewrap(text)

    items = []
    for p in parts:
        p = p.strip()
        if not p:
            continue
        items.append(_repair_url_linewrap(p))
    return "\n".join(items)


def standardize_separator(text: str) -> str:
    if not text:
        return text
    # Legacy ":" separator in *_mapped_rules cells — convert to "; "
    # But don't touch single rule IDs like "aws:ec2:..." (dot-separated style here)
    if ":" in text and ";" not in text and " " not in text:
        # Only split if every segment looks like a rule id (contains a dot)
        segs = text.split(":")
        if len(segs) > 1 and all("." in s for s in segs):
            return "; ".join(s.strip() for s in segs if s.strip())
    # Normalize existing "; " spacing
    return re.sub(r"\s*;\s*", "; ", text).strip("; ")


def collapse_ws(text: str) -> str:
    # Collapse runs of spaces/tabs but preserve newlines we inserted.
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    return text.strip()


def clean_row(row: dict) -> tuple[dict, dict]:
    """Return (new_row, change_log)."""
    changes = {}

    desc = row.get("requirement_description") or ""
    new_desc = fix_bullets(desc)
    new_desc = fix_description_numbered_list(new_desc)
    new_desc = collapse_ws(new_desc)
    if new_desc != desc:
        changes["requirement_description"] = True

    refs = row.get("references") or ""
    new_refs = fix_references(refs)
    new_refs = collapse_ws(new_refs)
    if new_refs != refs:
        changes["references"] = True

    name = row.get("requirement_name") or ""
    new_name = collapse_ws(name)
    if new_name != name:
        changes["requirement_name"] = True

    row["requirement_description"] = new_desc
    row["references"] = new_refs
    row["requirement_name"] = new_name

    for col in MAPPING_COLS:
        if col not in row:
            continue
        orig = row[col] or ""
        fixed = standardize_separator(orig)
        if fixed != orig:
            row[col] = fixed
            changes[col] = True

    return row, changes


def main() -> None:
    write = "--write" in sys.argv
    totals = {}
    diffs = []  # (unique_id, col, before, after)
    rows_out = []

    with open(SRC, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        cols = reader.fieldnames
        for row in reader:
            before = {k: (row.get(k) or "") for k in cols}
            new_row, changes = clean_row(dict(row))
            rows_out.append(new_row)
            for col in changes:
                totals[col] = totals.get(col, 0) + 1
                if len(diffs) < 20 and col in ("requirement_description", "references"):
                    diffs.append((new_row["unique_compliance_id"], col,
                                  before[col][:200], new_row[col][:240]))

    print(f"Rows processed: {len(rows_out)}")
    print("Changes per column:")
    for c, n in sorted(totals.items(), key=lambda x: -x[1]):
        print(f"  {c}: {n}")

    print("\n--- Sample diffs ---")
    for uid, col, b, a in diffs[:6]:
        print(f"\n[{uid}] {col}")
        print(f"  BEFORE: {b!r}")
        print(f"  AFTER : {a!r}")

    if write:
        with open(DST, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=cols)
            writer.writeheader()
            writer.writerows(rows_out)
        print(f"\nWrote {DST}")
    else:
        print("\n(dry-run — pass --write to persist)")


if __name__ == "__main__":
    main()
