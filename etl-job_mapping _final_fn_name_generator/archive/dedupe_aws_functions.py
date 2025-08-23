import os
import json
import re
from typing import Dict, List, Set, Tuple

# Tunable stopwords and normalizations
STOPWORDS: Set[str] = set(
	[
		"enabled", "disabled", "required", "configured", "active", "available",
		"present", "exists", "existing", "set", "applied", "enforced", "enforce",
		"allowed", "denied", "blocked", "restricted", "limited", "prohibited",
		"logged", "logging", "logs", "monitor", "monitored", "monitoring",
		"alert", "alerts", "alerting", "alarmed", "notification", "notifications",
		"created", "updated", "recent", "recently", "current", "minimum", "maximum",
		"min", "max", "daily", "weekly", "monthly", "continuous", "auto", "automatic",
		"automated", "retention", "policy", "policies", "rule", "rules",
		"review", "reviewed", "regularly", "consistently", "periodic", "scheduled",
		"window", "frequency", "version", "versions", "latest", "supported",
		"exists", "defined", "specified", "validated", "verified", "secure",
		"security", "protection", "protection", "compliance", "compliant",
		"centralized", "siem", "integration", "integrated", "export", "exported",
		"import", "assigned", "attached", "associated", "associates", "assumed",
		"granular", "granularity", "least", "privilege", "privileges",
	]
)

# Keep important nouns even if they appear with suffixes
KEEP_TOKENS: Set[str] = set(
	[
		"s3", "bucket", "account", "object", "versioning", "encryption", "kms",
		"tls", "https", "ssl", "policy", "role", "user", "group", "root",
		"iam", "endpoint", "privatelink", "private", "dns", "subnet", "route",
		"table", "nacl", "security", "group", "security_group", "flow", "log",
		"flow_log", "peering", "internet", "gateway", "nat", "vpc",
		"ec2", "instance", "ami", "network", "interface", "tag", "tags",
		"ecr", "repository", "scan", "vulnerability",
		"ecs", "service", "cluster", "task", "definition",
		"eks", "cluster", "pod", "deployment", "rbac", "api", "control", "plane",
		"cloudtrail", "trail", "cloudwatch", "alarm", "metric", "dashboard", "events",
		"config", "aggregator", "recorder", "rule", "snapshot",
		"rds", "aurora", "proxy", "instance",
		"dynamodb", "table", "stream", "streams",
		"docdb", "documentdb", "neptune", "keyspaces",
		"elasticsearch", "opensearch", "domain",
		"elasticache", "replication", "memorydb",
		"ebs", "volume", "snapshot",
		"efs", "file", "system", "access", "point", "mount", "target",
		"fsx", "cache",
		"cloudfront", "distribution",
	]
)

# Synonym mapping to unify tokens
SYNONYMS: Dict[str, str] = {
	"ssl": "tls",
	"https": "tls",
	"kms_key": "kms",
	"keys": "key",
	"privatelink": "endpoint",
	"private_link": "endpoint",
	"endpoint": "endpoint",
	"flow_logs": "flow_log",
	"logs": "log",
	"logging": "log",
	"policy": "policy",
	"policies": "policy",
}

TOKEN_SPLIT_RE = re.compile(r"[^a-z0-9]+")
NUM_RE = re.compile(r"^\d+$")


def canonicalize(fn: str) -> str:
	l = fn.lower()
	# common replacements
	l = l.replace("min_tls_", "tls_")
	l = l.replace("tls_min_", "tls_")
	l = l.replace("sse_s3", "sse")
	l = l.replace("sse_kms", "kms")
	# tokenize
	tokens = [t for t in TOKEN_SPLIT_RE.split(l) if t]
	canon: List[str] = []
	for t in tokens:
		if NUM_RE.match(t):
			continue
		if t in SYNONYMS:
			t = SYNONYMS[t]
		# drop trivial tokens unless explicitly kept
		if t in STOPWORDS and t not in KEEP_TOKENS:
			continue
		canon.append(t)
	# de-dup and sort for stable grouping
	uniq = sorted(set(canon))
	return "_".join(uniq)


def build_duplicates(by_service: Dict[str, List[str]]) -> Dict[str, List[Dict[str, List[str]]]]:
	result: Dict[str, List[Dict[str, List[str]]]] = {}
	for service, fns in by_service.items():
		key_to_fns: Dict[str, List[str]] = {}
		for fn in fns:
			key = canonicalize(fn)
			key_to_fns.setdefault(key, []).append(fn)
		# keep only keys with multiple functions
		dups = []
		for key, group in key_to_fns.items():
			if len(group) > 1:
				dups.append({"key": key, "functions": sorted(group)})
		if dups:
			# sort by size desc, then key
			dups.sort(key=lambda x: (-len(x["functions"]), x["key"]))
			result[service] = dups
	return result


def main() -> int:
	etl_dir = os.path.dirname(os.path.abspath(__file__))
	in_json = os.path.join(etl_dir, 'aws_functions_by_service.json')
	out_json = os.path.join(etl_dir, 'aws_duplicates_by_category.json')
	if not os.path.exists(in_json):
		print(f"Input not found: {in_json}")
		return 1
	with open(in_json, 'r', encoding='utf-8') as f:
		by_service = json.load(f)
	dups = build_duplicates(by_service)
	with open(out_json, 'w', encoding='utf-8') as f:
		json.dump(dups, f, indent=2, sort_keys=True)
	print(f"Wrote duplicate clusters to {out_json}")
	return 0


if __name__ == '__main__':
	exit(main()) 