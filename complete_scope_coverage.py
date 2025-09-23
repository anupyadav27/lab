#!/usr/bin/env python3
import json

def add_final_missing_scopes():
    """Add the final 2 missing scopes to complete coverage"""
    
    # Load enhanced matrix
    with open('/Users/apple/Desktop/compliance_Database/rule-generator-engine/Step3-matrices-per-cloud-provider/azure_matrix_2025-01-09_enriched_complete_enhanced.json', 'r') as f:
        matrix = json.load(f)
    
    # Add identity.policy scope
    identity_policy_mappings = [
        {
            "service": "azuread",
            "resource": "identity.policy",
            "resource_type": "identity.policy",
            "adapter": "azure.azuread.conditional_access_policy_mfa_required",
            "coverage_tier": "core",
            "not_applicable_when": "no_conditional_access",
            "signal": {
                "fields": ["policies"],
                "predicate": "policies.some(p => p.grantControls.requireMfa === true)",
                "paths_doc": ["GET /identity/conditionalAccess/policies -> grantControls"],
                "evidence_type": "config_read"
            }
        },
        {
            "service": "azuread",
            "resource": "identity.policy",
            "resource_type": "identity.policy",
            "adapter": "azure.azuread.authentication_strength_policy_configured",
            "coverage_tier": "extended",
            "not_applicable_when": "no_azure_ad_configured",
            "signal": {
                "fields": ["authenticationStrengthPolicies"],
                "predicate": "authenticationStrengthPolicies.length >= 1",
                "paths_doc": ["GET /policies/authenticationStrengthPolicies"],
                "evidence_type": "config_read"
            }
        }
    ]
    
    # Add logging.trail scope
    logging_trail_mappings = [
        {
            "service": "monitor",
            "resource": "logging.trail",
            "resource_type": "logging.trail",
            "adapter": "azure.monitor.activity_logs_enabled",
            "coverage_tier": "core",
            "not_applicable_when": "no_azure_ad_tenant",
            "signal": {
                "fields": ["activityLogs"],
                "predicate": "activityLogs.enabled === true",
                "paths_doc": ["GET /providers/Microsoft.Insights/eventTypes/management/values"],
                "evidence_type": "config_read"
            }
        },
        {
            "service": "monitor",
            "resource": "logging.trail",
            "resource_type": "logging.trail",
            "adapter": "azure.monitor.activity_logs_retention_configured",
            "coverage_tier": "extended",
            "not_applicable_when": "no_azure_ad_tenant",
            "signal": {
                "fields": ["retentionDays"],
                "predicate": "retentionDays >= 365",
                "paths_doc": ["GET /subscriptions/{subscriptionId}/providers/Microsoft.Insights/logprofiles"],
                "evidence_type": "config_read"
            }
        }
    ]
    
    # Add to appropriate assertion categories
    if "identity_access.authorization" not in matrix:
        matrix["identity_access.authorization"] = {"core": [], "extended": [], "exhaustive": []}
    
    if "logging_monitoring.audit_logging" not in matrix:
        matrix["logging_monitoring.audit_logging"] = {"core": [], "extended": [], "exhaustive": []}
    
    # Add identity.policy mappings
    for mapping in identity_policy_mappings:
        tier = mapping["coverage_tier"]
        matrix["identity_access.authorization"][tier].append(mapping)
    
    # Add logging.trail mappings
    for mapping in logging_trail_mappings:
        tier = mapping["coverage_tier"]
        matrix["logging_monitoring.audit_logging"][tier].append(mapping)
    
    # Write complete matrix
    output_path = "/Users/apple/Desktop/compliance_Database/rule-generator-engine/Step3-matrices-per-cloud-provider/azure_matrix_2025-01-09_enriched_complete_final.json"
    with open(output_path, 'w') as f:
        json.dump(matrix, f, indent=2)
    
    print(f"Complete matrix written to {output_path}")
    
    # Validate final coverage
    validate_final_coverage(matrix)

def validate_final_coverage(matrix):
    """Validate the final scope coverage"""
    
    # Load enhanced assertions
    with open('/Users/apple/Desktop/compliance_Database/rule-generator-engine/step-2-common-assercian-id/assertions_pack_final_2025-09-11T18-41-14_enhanced.json', 'r') as f:
        assertions = json.load(f)
    
    assertion_scopes = set(assertions['scope_allowlist'])
    
    matrix_scopes = set()
    for assertion_key, tiers in matrix.items():
        for tier_name, rows in tiers.items():
            for row in rows:
                if 'resource' in row:
                    matrix_scopes.add(row['resource'])
    
    missing_scopes = assertion_scopes - matrix_scopes
    covered_scopes = assertion_scopes & matrix_scopes
    coverage_percent = (len(covered_scopes) / len(assertion_scopes)) * 100
    
    print(f"\n=== FINAL COVERAGE VALIDATION ===")
    print(f"✅ Final Coverage: {len(covered_scopes)}/{len(assertion_scopes)} ({coverage_percent:.1f}%)")
    print(f"❌ Missing: {len(missing_scopes)}")
    
    if missing_scopes:
        print("Missing scopes:")
        for scope in sorted(missing_scopes):
            print(f"  - {scope}")
    else:
        print("🎉 COMPLETE SCOPE COVERAGE ACHIEVED!")

if __name__ == "__main__":
    add_final_missing_scopes()
