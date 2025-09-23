#!/usr/bin/env python3
import json
from pathlib import Path

def enhance_azure_matrix_with_missing_scopes():
    """Enhance Azure matrix with missing scopes and Azure-specific mappings"""
    
    # Load the existing enriched matrix
    matrix_path = "/Users/apple/Desktop/compliance_Database/rule-generator-engine/Step3-matrices-per-cloud-provider/azure_matrix_2025-01-09_enriched_complete.json"
    with open(matrix_path, 'r') as f:
        existing_matrix = json.load(f)
    
    # Define additional mappings for missing scopes
    missing_scope_enhancements = {
        # Database & Data scopes
        "db.cluster": {
            "azure_mappings": [
                {
                    "service": "sql",
                    "resource": "db.cluster",
                    "resource_type": "db.cluster",
                    "adapter": "azure.sql.server_encryption_at_rest",
                    "coverage_tier": "core",
                    "not_applicable_when": "no_sql_servers",
                    "signal": {
                        "fields": ["transparentDataEncryption"],
                        "predicate": "transparentDataEncryption.state === 'Enabled'",
                        "paths_doc": ["properties.transparentDataEncryption"],
                        "evidence_type": "config_read"
                    }
                },
                {
                    "service": "cosmosdb",
                    "resource": "db.cluster",
                    "resource_type": "db.cluster",
                    "adapter": "azure.cosmosdb.account_encryption_at_rest",
                    "coverage_tier": "core",
                    "not_applicable_when": "no_cosmosdb_accounts",
                    "signal": {
                        "fields": ["encryption"],
                        "predicate": "encryption.keyVaultKeyUri !== null",
                        "paths_doc": ["properties.encryption"],
                        "evidence_type": "config_read"
                    }
                }
            ]
        },
        "db.user": {
            "azure_mappings": [
                {
                    "service": "sql",
                    "resource": "db.user",
                    "resource_type": "db.user",
                    "adapter": "azure.sql.database_users_managed_identity",
                    "coverage_tier": "core",
                    "not_applicable_when": "no_sql_databases",
                    "signal": {
                        "fields": ["users"],
                        "predicate": "users.every(u => u.type === 'ExternalUser' || u.authenticationType === 'AzureAD')",
                        "paths_doc": ["GET /sqlServers/{server}/databases/{db}/users"],
                        "evidence_type": "config_read"
                    }
                }
            ]
        },
        "secrets.store": {
            "azure_mappings": [
                {
                    "service": "keyvault",
                    "resource": "secrets.store",
                    "resource_type": "secrets.store",
                    "adapter": "azure.keyvault.vault_soft_delete_enabled",
                    "coverage_tier": "core",
                    "not_applicable_when": "no_key_vault",
                    "signal": {
                        "fields": ["enableSoftDelete"],
                        "predicate": "enableSoftDelete === true",
                        "paths_doc": ["properties.enableSoftDelete"],
                        "evidence_type": "config_read"
                    }
                },
                {
                    "service": "keyvault",
                    "resource": "secrets.store",
                    "resource_type": "secrets.store",
                    "adapter": "azure.keyvault.vault_purge_protection_enabled",
                    "coverage_tier": "extended",
                    "not_applicable_when": "no_key_vault",
                    "signal": {
                        "fields": ["enablePurgeProtection"],
                        "predicate": "enablePurgeProtection === true",
                        "paths_doc": ["properties.enablePurgeProtection"],
                        "evidence_type": "config_read"
                    }
                }
            ]
        },
        
        # Kubernetes scopes
        "k8s.admission": {
            "azure_mappings": [
                {
                    "service": "aks",
                    "resource": "k8s.admission",
                    "resource_type": "k8s.admission",
                    "adapter": "azure.aks.admission_webhooks_enabled",
                    "coverage_tier": "extended",
                    "not_applicable_when": "no_aks_clusters",
                    "signal": {
                        "fields": ["admissionControllers"],
                        "predicate": "admissionControllers.includes('ValidatingAdmissionWebhook') && admissionControllers.includes('MutatingAdmissionWebhook')",
                        "paths_doc": ["GET /managedClusters/{cluster}/admissionControllers"],
                        "evidence_type": "config_read"
                    }
                }
            ]
        },
        "k8s.namespace": {
            "azure_mappings": [
                {
                    "service": "aks",
                    "resource": "k8s.namespace",
                    "resource_type": "k8s.namespace",
                    "adapter": "azure.aks.namespace_network_policies_enabled",
                    "coverage_tier": "extended",
                    "not_applicable_when": "no_aks_clusters",
                    "signal": {
                        "fields": ["networkPolicies"],
                        "predicate": "networkPolicies.some(np => np.namespace !== 'kube-system' && np.enabled === true)",
                        "paths_doc": ["GET /managedClusters/{cluster}/namespaces/{ns}/networkPolicies"],
                        "evidence_type": "config_read"
                    }
                }
            ]
        },
        "k8s.network_policy": {
            "azure_mappings": [
                {
                    "service": "aks",
                    "resource": "k8s.network_policy",
                    "resource_type": "k8s.network_policy",
                    "adapter": "azure.aks.network_policy_enforcement",
                    "coverage_tier": "core",
                    "not_applicable_when": "no_aks_clusters",
                    "signal": {
                        "fields": ["networkPolicy"],
                        "predicate": "networkPolicy === 'azure' || networkPolicy === 'calico'",
                        "paths_doc": ["properties.networkProfile.networkPolicy"],
                        "evidence_type": "config_read"
                    }
                }
            ]
        },
        "k8s.workload": {
            "azure_mappings": [
                {
                    "service": "aks",
                    "resource": "k8s.workload",
                    "resource_type": "k8s.workload",
                    "adapter": "azure.aks.pod_security_policies_enabled",
                    "coverage_tier": "extended",
                    "not_applicable_when": "no_aks_clusters",
                    "signal": {
                        "fields": ["podSecurityPolicies"],
                        "predicate": "podSecurityPolicies.enabled === true",
                        "paths_doc": ["GET /managedClusters/{cluster}/podSecurityPolicies"],
                        "evidence_type": "config_read"
                    }
                }
            ]
        },
        
        # Identity & Access scopes
        "identity.role": {
            "azure_mappings": [
                {
                    "service": "azuread",
                    "resource": "identity.role",
                    "resource_type": "identity.role",
                    "adapter": "azure.azuread.directory_roles_assignment_limited",
                    "coverage_tier": "core",
                    "not_applicable_when": "no_azure_ad_roles",
                    "signal": {
                        "fields": ["roleAssignments"],
                        "predicate": "roleAssignments.length <= 10",
                        "paths_doc": ["GET /roleManagement/directory/roleAssignments"],
                        "evidence_type": "config_read"
                    }
                }
            ]
        },
        "identity.service_account": {
            "azure_mappings": [
                {
                    "service": "azuread",
                    "resource": "identity.service_account",
                    "resource_type": "identity.service_account",
                    "adapter": "azure.azuread.service_principal_secret_rotation",
                    "coverage_tier": "core",
                    "not_applicable_when": "no_service_principals",
                    "signal": {
                        "fields": ["secretExpiry"],
                        "predicate": "secretExpiry <= 90",
                        "paths_doc": ["GET /servicePrincipals/{id}/keyCredentials"],
                        "evidence_type": "config_read"
                    }
                }
            ]
        },
        
        # Networking scopes
        "network.vpc": {
            "azure_mappings": [
                {
                    "service": "network",
                    "resource": "network.vpc",
                    "resource_type": "network.vpc",
                    "adapter": "azure.network.vnet_ddos_protection_enabled",
                    "coverage_tier": "extended",
                    "not_applicable_when": "no_vnets",
                    "signal": {
                        "fields": ["ddosProtectionPlan"],
                        "predicate": "ddosProtectionPlan !== null",
                        "paths_doc": ["properties.ddosProtectionPlan"],
                        "evidence_type": "config_read"
                    }
                }
            ]
        },
        "dns.zone": {
            "azure_mappings": [
                {
                    "service": "dns",
                    "resource": "dns.zone",
                    "resource_type": "dns.zone",
                    "adapter": "azure.dns.zone_private_endpoints_enabled",
                    "coverage_tier": "extended",
                    "not_applicable_when": "no_dns_zones",
                    "signal": {
                        "fields": ["privateEndpoints"],
                        "predicate": "(privateEndpoints?.length || 0) > 0",
                        "paths_doc": ["properties.privateEndpoints"],
                        "evidence_type": "config_read"
                    }
                }
            ]
        },
        "edge.waf": {
            "azure_mappings": [
                {
                    "service": "frontdoor",
                    "resource": "edge.waf",
                    "resource_type": "edge.waf",
                    "adapter": "azure.frontdoor.waf_enabled",
                    "coverage_tier": "core",
                    "not_applicable_when": "no_frontdoor",
                    "signal": {
                        "fields": ["wafPolicy"],
                        "predicate": "wafPolicy !== null && wafPolicy.enabled === true",
                        "paths_doc": ["properties.frontendEndpoints.wafPolicy"],
                        "evidence_type": "config_read"
                    }
                }
            ]
        },
        
        # Platform & Governance scopes
        "platform.control_plane": {
            "azure_mappings": [
                {
                    "service": "aks",
                    "resource": "platform.control_plane",
                    "resource_type": "platform.control_plane",
                    "adapter": "azure.aks.api_server_authorized_ip_ranges",
                    "coverage_tier": "core",
                    "not_applicable_when": "no_aks_clusters",
                    "signal": {
                        "fields": ["apiServerAccessProfile"],
                        "predicate": "apiServerAccessProfile.authorizedIPRanges.length > 0",
                        "paths_doc": ["properties.apiServerAccessProfile.authorizedIPRanges"],
                        "evidence_type": "config_read"
                    }
                }
            ]
        },
        "governance.org": {
            "azure_mappings": [
                {
                    "service": "management-groups",
                    "resource": "governance.org",
                    "resource_type": "governance.org",
                    "adapter": "azure.management_groups.hierarchy_governance",
                    "coverage_tier": "core",
                    "not_applicable_when": "no_management_groups",
                    "signal": {
                        "fields": ["governancePolicies"],
                        "predicate": "governancePolicies.length >= 3",
                        "paths_doc": ["GET /providers/Microsoft.Management/managementGroups/{mg}/providers/Microsoft.Authorization/policyAssignments"],
                        "evidence_type": "config_read"
                    }
                }
            ]
        },
        "dr.plan": {
            "azure_mappings": [
                {
                    "service": "site-recovery",
                    "resource": "dr.plan",
                    "resource_type": "dr.plan",
                    "adapter": "azure.asr.replication_policies_configured",
                    "coverage_tier": "core",
                    "not_applicable_when": "no_asr_configured",
                    "signal": {
                        "fields": ["replicationPolicies"],
                        "predicate": "replicationPolicies.length >= 1 && replicationPolicies.every(p => p.recoveryPointRetentionInHours >= 24)",
                        "paths_doc": ["GET /replicationPolicies"],
                        "evidence_type": "config_read"
                    }
                }
            ]
        },
        
        # Logging & Monitoring scopes
        "logging.sink": {
            "azure_mappings": [
                {
                    "service": "monitor",
                    "resource": "logging.sink",
                    "resource_type": "logging.sink",
                    "adapter": "azure.monitor.diagnostic_settings_sink_configured",
                    "coverage_tier": "core",
                    "not_applicable_when": "no_diagnostic_settings",
                    "signal": {
                        "fields": ["diagnosticSettings"],
                        "predicate": "diagnosticSettings.some(ds => ds.logs.length > 0 || ds.metrics.length > 0)",
                        "paths_doc": ["GET /providers/Microsoft.Insights/diagnosticSettings"],
                        "evidence_type": "config_read"
                    }
                }
            ]
        },
        "logging.store": {
            "azure_mappings": [
                {
                    "service": "log-analytics",
                    "resource": "logging.store",
                    "resource_type": "logging.store",
                    "adapter": "azure.log_analytics.workspace_retention_configured",
                    "coverage_tier": "core",
                    "not_applicable_when": "no_log_analytics_workspaces",
                    "signal": {
                        "fields": ["retentionInDays"],
                        "predicate": "retentionInDays >= 90",
                        "paths_doc": ["properties.retentionInDays"],
                        "evidence_type": "config_read"
                    }
                }
            ]
        },
        "monitoring.alert": {
            "azure_mappings": [
                {
                    "service": "monitor",
                    "resource": "monitoring.alert",
                    "resource_type": "monitoring.alert",
                    "adapter": "azure.monitor.alert_rules_security_configured",
                    "coverage_tier": "core",
                    "not_applicable_when": "no_monitoring_alerts",
                    "signal": {
                        "fields": ["alertRules"],
                        "predicate": "alertRules.filter(r => r.category === 'Security').length >= 5",
                        "paths_doc": ["GET /providers/Microsoft.Insights/metricAlerts"],
                        "evidence_type": "config_read"
                    }
                }
            ]
        },
        "monitoring.metric": {
            "azure_mappings": [
                {
                    "service": "monitor",
                    "resource": "monitoring.metric",
                    "resource_type": "monitoring.metric",
                    "adapter": "azure.monitor.metrics_collection_enabled",
                    "coverage_tier": "core",
                    "not_applicable_when": "no_monitoring_configured",
                    "signal": {
                        "fields": ["metricsEnabled"],
                        "predicate": "metricsEnabled === true",
                        "paths_doc": ["properties.metrics"],
                        "evidence_type": "config_read"
                    }
                }
            ]
        },
        
        # Supply Chain scopes
        "registry.repo": {
            "azure_mappings": [
                {
                    "service": "acr",
                    "resource": "registry.repo",
                    "resource_type": "registry.repo",
                    "adapter": "azure.acr.repository_vulnerability_scanning_enabled",
                    "coverage_tier": "core",
                    "not_applicable_when": "no_acr_registries",
                    "signal": {
                        "fields": ["vulnerabilityScanning"],
                        "predicate": "vulnerabilityScanning.enabled === true",
                        "paths_doc": ["properties.policies.trustPolicy.status"],
                        "evidence_type": "config_read"
                    }
                }
            ]
        }
    }
    
    # Add the new scope mappings to existing matrix
    for scope, mappings in missing_scope_enhancements.items():
        for mapping in mappings["azure_mappings"]:
            # Determine assertion category based on scope
            assertion_category = determine_assertion_category(scope, mapping)
            
            if assertion_category not in existing_matrix:
                existing_matrix[assertion_category] = {"core": [], "extended": [], "exhaustive": []}
            
            # Add to appropriate tier
            tier = mapping["coverage_tier"]
            existing_matrix[assertion_category][tier].append(mapping)
    
    # Write enhanced matrix
    output_path = "/Users/apple/Desktop/compliance_Database/rule-generator-engine/Step3-matrices-per-cloud-provider/azure_matrix_2025-01-09_enriched_complete_enhanced.json"
    with open(output_path, 'w') as f:
        json.dump(existing_matrix, f, indent=2)
    
    print(f"Enhanced matrix written to {output_path}")
    return existing_matrix

def determine_assertion_category(scope, mapping):
    """Determine the appropriate assertion category for a scope"""
    scope_to_category = {
        "db.cluster": "crypto_data_protection.encryption_at_rest",
        "db.user": "identity_access.authentication",
        "secrets.store": "secrets_key_mgmt.secret_storage",
        "k8s.admission": "containers_kubernetes.admission_control",
        "k8s.namespace": "containers_kubernetes.network_policies",
        "k8s.network_policy": "containers_kubernetes.network_policies",
        "k8s.workload": "containers_kubernetes.runtime_security",
        "identity.role": "rbac_entitlements.role_assignment",
        "identity.service_account": "identity_access.authentication",
        "network.vpc": "network_perimeter.ddos_protection",
        "dns.zone": "network_perimeter.dns_security",
        "edge.waf": "network_perimeter.firewall_rules",
        "platform.control_plane": "containers_kubernetes.rbac_policies",
        "governance.org": "governance_compliance.resource_governance",
        "dr.plan": "resilience_recovery.disaster_recovery",
        "logging.sink": "logging_monitoring.log_collection",
        "logging.store": "logging_monitoring.log_retention",
        "monitoring.alert": "logging_monitoring.monitoring_alerting",
        "monitoring.metric": "logging_monitoring.monitoring_alerting",
        "registry.repo": "supply_chain_registries.vulnerability_scanning"
    }
    
    return scope_to_category.get(scope, "identity_access.authentication")

if __name__ == "__main__":
    enhance_azure_matrix_with_missing_scopes()
