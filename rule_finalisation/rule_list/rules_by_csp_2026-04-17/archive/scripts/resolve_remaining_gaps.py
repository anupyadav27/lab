"""
Resolve three gap categories:

(A) 49 non-aws. format catalog rules — naming duplicates.
    Find best YAML config rules + CIEM rules via token Jaccard (one-to-many OK).

(C) 23 aws. format true gaps with compliance IDs.
    Use DeepSeek AI to find any YAML or CIEM rule covering each.

Outputs:
  aws_gap_resolution_A.csv   mapping for 49 naming duplicates
  aws_gap_resolution_C.csv   mapping for 23 true gaps
  aws_gap_resolution_C_checkpoint.json
"""
import argparse, csv, json, os, sys, time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from openai import OpenAI

csv.field_size_limit(sys.maxsize)

BASE        = Path("/Users/apple/Desktop/compliance_Database/rule_finalisation/rule_list/rules_by_csp_2026-04-17")
MATRIX      = BASE / "aws_catalog_coverage_matrix_final.csv"
YAML_MAP    = BASE / "aws_unified_ai_mapping.csv"
CIEM_JSON   = BASE / "aws_ciem_rules_consolidated.json"
OUT_A       = BASE / "aws_gap_resolution_A.csv"
OUT_C       = BASE / "aws_gap_resolution_C.csv"
CKPT_C      = BASE / "aws_gap_resolution_C_checkpoint.json"

MODEL       = "deepseek-chat"
CONCURRENCY = 10

NOISE = {"aws", "configured", "configuration", "resource"}
SYN = {
    "logging": "log", "logs": "log",
    "encrypted": "encryption", "encrypting": "encryption",
    "policies": "policy", "keys": "key", "accounts": "account",
    "users": "user", "roles": "role", "groups": "group",
    "permissions": "permission", "instances": "instance", "buckets": "bucket",
    "clusters": "cluster", "volumes": "volume", "snapshots": "snapshot",
    "rotation": "rotate", "rotated": "rotate", "rotating": "rotate",
    "restricted": "restrict", "restricting": "restrict",
    "enforced": "enforce", "enforcing": "enforce",
    "required": "require", "requires": "require",
    "disabled": "disable",
}

def norm(rid):
    parts = rid.lower().replace("-","_").split(".")
    svc = parts[1] if len(parts)>=2 and parts[0]=="aws" else (parts[0] if parts else "")
    tail = parts[2:] if len(parts)>=2 and parts[0]=="aws" else parts[1:]
    toks = set()
    for p in tail:
        for t in p.split("_"):
            if not t or t in NOISE: continue
            t = SYN.get(t, t)
            if len(t)>=4 and t.endswith("s") and not t.endswith("ss"): t=t[:-1]
            toks.add(t)
    return svc, frozenset(toks)

def jac(a,b):
    if not a or not b: return 0.0
    return len(a&b)/len(a|b)

def parse_comp(raw):
    if not raw: return frozenset()
    return frozenset(x.strip() for x in raw.split(";") if x.strip())

# ── Load data ────────────────────────────────────────────────────────────────
print("[1] Load data")
matrix_rows = list(csv.DictReader(MATRIX.open()))
gaps        = [r for r in matrix_rows if r["coverage_status"]=="ai_confirmed_gap"]
cat_A       = [r for r in gaps if "," not in r["catalog_rule_id"]
               and not r["catalog_rule_id"].startswith("aws.")
               and r["has_compliance_ids"]=="yes"]
cat_C       = [r for r in gaps if "," not in r["catalog_rule_id"]
               and r["catalog_rule_id"].startswith("aws.")
               and r["has_compliance_ids"]=="yes"]

yaml_rows   = list(csv.DictReader(YAML_MAP.open()))
ciem_recs   = json.loads(CIEM_JSON.read_text())
for c in ciem_recs:
    c["_tok"]  = norm(c.get("rule_id",""))[1]
    c["_comp"] = parse_comp(c.get("aws_mapped_compliance_ids",""))

print(f"   Cat-A (naming dupes): {len(cat_A)}")
print(f"   Cat-C (true gaps):    {len(cat_C)}")

# Build YAML lookup: tokens → list of yaml rows
yaml_by_tok = defaultdict(list)
for r in yaml_rows:
    _, toks = norm(r["yaml_rule_id"])
    for t in toks:
        yaml_by_tok[t].append(r)

# ── PART A: token Jaccard matching ─────────────────────────────────────────
print("\n[2] Part A — token Jaccard matching for 49 naming duplicates")

def top_yaml(cat_rid, n=5):
    _, cat_tok = norm(cat_rid)
    cands = {}
    for t in cat_tok:
        for r in yaml_by_tok.get(t, []):
            cands[r["yaml_rule_id"]] = r
    scored = [(jac(cat_tok, norm(rid)[1]), r) for rid, r in cands.items()]
    scored.sort(key=lambda x: -x[0])
    return scored[:n]

def top_ciem(cat_rid, cat_comp, n=5):
    _, cat_tok = norm(cat_rid)
    scored = []
    for c in ciem_recs:
        t = jac(cat_tok, c["_tok"])
        cj = jac(cat_comp, c["_comp"])
        sh = len(cat_comp & c["_comp"])
        score = 0.5*t + 0.3*cj + (0.2 if sh>=1 else 0)
        if score > 0.1:
            scored.append((score, t, cj, c))
    scored.sort(key=lambda x: -x[0])
    return scored[:n]

a_rows = []
for r in cat_A:
    rid  = r["catalog_rule_id"]
    comp = parse_comp(r["catalog_compliance_ids"])
    ym   = top_yaml(rid, 5)
    cm   = top_ciem(rid, comp, 5)

    yaml_ids  = ";".join(x[1]["yaml_rule_id"] for x in ym if x[0]>=0.4)
    yaml_best = round(ym[0][0],3) if ym else 0
    ciem_ids  = ";".join(x[3]["rule_id"] for x in cm if x[0]>=0.2)
    ciem_ttls = ";".join(x[3].get("title","")[:60] for x in cm if x[0]>=0.2)

    a_rows.append({
        "catalog_rule_id":       rid,
        "service":               r["service"],
        "catalog_compliance_ids":r["catalog_compliance_ids"][:200],
        "best_yaml_jaccard":     yaml_best,
        "yaml_config_rules":     yaml_ids,
        "yaml_top1":             ym[0][1]["yaml_rule_id"] if ym else "",
        "yaml_top1_catalog_map": ym[0][1].get("catalog_orig_rule_id","") if ym else "",
        "yaml_top1_conf":        ym[0][1].get("catalog_confidence","") if ym else "",
        "ciem_rules":            ciem_ids,
        "ciem_titles":           ciem_ttls,
        "verdict":               ("mapped" if yaml_ids or ciem_ids else "still_gap"),
    })
    flag = "✓" if yaml_ids else "?"
    print(f"  {flag} [{r['service']:15s}] {rid[:55]:55s}  j={yaml_best}  ciem={len([x for x in cm if x[0]>=0.2])}")

with OUT_A.open("w",newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(a_rows[0].keys()))
    w.writeheader(); w.writerows(a_rows)
mapped_a = sum(1 for r in a_rows if r["verdict"]=="mapped")
print(f"\n  → {mapped_a}/{len(a_rows)} mapped  |  output: {OUT_A.name}")

# ── PART C: AI matching ─────────────────────────────────────────────────────
print("\n[3] Part C — AI matching for 23 true gaps")

SYSTEM = """\
You are a cloud security architect mapping compliance catalog rules to implementation rules for a CSPM platform.
Config rules check static asset configuration. CIEM rules detect security events via logs.
Find the BEST available rule(s) — one config rule, one CIEM rule, or both — that implement the same security check.
Only return rules from the provided candidates. If nothing matches, return empty strings."""

def prompt_C(cat_row, yaml_cands, ciem_cands):
    rid  = cat_row["catalog_rule_id"]
    comp = cat_row["catalog_compliance_ids"][:200]
    svc  = cat_row["service"]
    lines = [
        f"CATALOG RULE TO MAP:",
        f"  rule_id:    {rid}",
        f"  service:    {svc}",
        f"  compliance: {comp}",
        "",
        f"TOP CONFIG (YAML) CANDIDATES:",
    ]
    for i,(s,r) in enumerate(yaml_cands,1):
        lines.append(f"  {i}. {r['yaml_rule_id']}  (jaccard={s:.2f})  maps_to={r.get('catalog_orig_rule_id','')[:50]}")
    lines += ["", "TOP CIEM CANDIDATES:"]
    for i,(s,_,_,c) in enumerate(ciem_cands,1):
        lines.append(f"  {i}. {c['rule_id']}  score={s:.2f}  threat={c.get('threat_category','')}")
        lines.append(f"     title: {c.get('title','')[:80]}")
    lines += ["",
        'Return ONLY valid JSON (no markdown):',
        '{"config_rule_id":"<yaml rule_id or empty>","config_confidence":"high|medium|low|none",',
        ' "ciem_rule_ids":["<id1>","<id2>"],"ciem_confidence":"high|medium|low|none","reasoning":"<1 sentence>"}']
    return "\n".join(lines)

def call_ai(client, cat_row, yaml_cands, ciem_cands):
    p = prompt_C(cat_row, yaml_cands, ciem_cands)
    for attempt in range(3):
        try:
            resp = client.chat.completions.create(
                model=MODEL,
                messages=[{"role":"system","content":SYSTEM},{"role":"user","content":p}],
                temperature=0.1, max_tokens=300,
            )
            raw = resp.choices[0].message.content.strip()
            if raw.startswith("```"): raw = raw.split("```")[1]; raw = raw[4:] if raw.startswith("json") else raw
            return json.loads(raw)
        except Exception as e:
            if attempt<2: time.sleep(2**attempt)
            else: return {"config_rule_id":"","config_confidence":"none","ciem_rule_ids":[],"ciem_confidence":"none","reasoning":str(e)[:100]}

def run_part_C(client):
    ckpt = json.loads(CKPT_C.read_text()) if CKPT_C.exists() else {}
    todo = [r for r in cat_C if r["catalog_rule_id"] not in ckpt]
    print(f"   {len(ckpt)} already done, {len(todo)} to process")

    def process(row):
        rid  = row["catalog_rule_id"]
        comp = parse_comp(row["catalog_compliance_ids"])
        ym   = top_yaml(rid, 8)
        cm   = top_ciem(rid, comp, 8)
        res  = call_ai(client, row, ym, cm)
        return rid, res

    with ThreadPoolExecutor(max_workers=CONCURRENCY) as ex:
        futs = {ex.submit(process, r): r for r in todo}
        for fut in as_completed(futs):
            rid, res = fut.result()
            ckpt[rid] = res
            CKPT_C.write_text(json.dumps(ckpt, indent=2))
            cfg = res.get("config_rule_id","")
            ciem = ",".join(res.get("ciem_rule_ids",[]))
            conf = res.get("config_confidence","?")
            cc   = res.get("ciem_confidence","?")
            print(f"   {rid[:50]:50s}  cfg={conf}  ciem_conf={cc}")
            if cfg:  print(f"     config → {cfg}")
            if ciem: print(f"     ciem   → {ciem}")
    return ckpt

def write_C(ckpt):
    out = []
    for r in cat_C:
        rid = r["catalog_rule_id"]
        res = ckpt.get(rid,{})
        out.append({
            "catalog_rule_id":       rid,
            "service":               r["service"],
            "catalog_compliance_ids":r["catalog_compliance_ids"][:200],
            "config_rule_id":        res.get("config_rule_id",""),
            "config_confidence":     res.get("config_confidence",""),
            "ciem_rule_ids":         ";".join(res.get("ciem_rule_ids",[]) or []),
            "ciem_confidence":       res.get("ciem_confidence",""),
            "reasoning":             res.get("reasoning","")[:300],
        })
    with OUT_C.open("w",newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys()))
        w.writeheader(); w.writerows(out)
    return out

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    api_key = (os.getenv("DEEPSEEK_API_KEY") or "").strip()
    if not api_key and not args.dry_run:
        print("ERROR: DEEPSEEK_API_KEY not set"); sys.exit(2)

    if args.dry_run:
        print("\n[DRY RUN Part C] First 2 prompts:")
        client_stub = None
        for row in cat_C[:2]:
            comp = parse_comp(row["catalog_compliance_ids"])
            ym = top_yaml(row["catalog_rule_id"], 8)
            cm = top_ciem(row["catalog_rule_id"], comp, 8)
            print(f"\n=== {row['catalog_rule_id']} ===")
            print(prompt_C(row, ym, cm)[:600])
    else:
        client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
        ckpt = run_part_C(client)
        c_out = write_C(ckpt)
        matched_C = sum(1 for r in c_out if r["config_rule_id"] or r["ciem_rule_ids"])
        print(f"\n  → {matched_C}/{len(c_out)} matched  |  output: {OUT_C.name}")

    print("\nDone.")
