#!/usr/bin/env python3
import json
from pathlib import Path

def enrich_azure_matrix():
    """Enrich Azure matrix with atomic signals and predicates"""
    
    # Load the original matrix
    matrix_path = "/Users/apple/Desktop/compliance_Database/rule-generator-engine/Step3-matrices-per-cloud-provider/azure_matrix_2025-01-09.json"
    with open(matrix_path, 'r') as f:
        original_matrix = json.load(f)
    
    enriched_matrix = {}
    
    # Define enrichment patterns for different adapter types
    enrichment_patterns = {
        # Identity & Access patterns
        "azure.azuread.user_mfa_status": {
            "atomic_adapters": [
                {
                    "adapter": "azure.azuread.user_mfa_registered",
                    "signal": {
                        "fields": ["registeredMethods"],
                        "predicate": "Array.isArray(registeredMethods) && registeredMethods.length >= 1",
                        "paths_doc": ["GET /reports/authenticationMethods/userRegistrationDetails -> methodsRegistered"],
                        "evidence_type": "config_read"
                    }
                },
                {
                    "adapter": "azure.azuread.user_strong_mfa_registered",
                    "params": {"strong_methods": ["microsoftAuthenticator", "fido2", "passkey", "softwareOath"]},
                    "signal": {
                        "fields": ["registeredMethods"],
                        "predicate": "registeredMethods.some(m => params.strong_methods.includes(m))",
                        "paths_doc": ["GET /users/{id}/authentication/methods"],
                        "evidence_type": "config_read"
                    }
                }
            ]
        },
        "azure.azuread.password_policy": {
            "atomic_adapters": [
                {
                    "adapter": "azure.azuread.user_password_expiration_not_disabled",
                    "signal": {
                        "fields": ["passwordPolicies"],
                        "predicate": "!(passwordPolicies || '').includes('DisablePasswordExpiration')",
                        "paths_doc": ["GET /users/{id} -> passwordPolicies"],
                        "evidence_type": "config_read"
                    }
                },
                {
                    "adapter": "azure.azuread.user_strong_password_not_disabled",
                    "signal": {
                        "fields": ["passwordPolicies"],
                        "predicate": "!(passwordPolicies || '').includes('DisableStrongPassword')",
                        "paths_doc": ["GET /users/{id} -> passwordPolicies"],
                        "evidence_type": "config_read"
                    }
                }
            ]
        },
        "azure.azuread.security_defaults": {
            "atomic_adapters": [
                {
                    "adapter": "azure.azuread.security_defaults_enabled",
                    "signal": {
                        "fields": ["securityDefaultsEnabled"],
                        "predicate": "securityDefaultsEnabled === true",
                        "paths_doc": ["GET /policies/identitySecurityDefaultsEnforcementPolicy"],
                        "evidence_type": "config_read"
                    }
                }
            ]
        },
        "azure.azuread.legacy_authentication_blocked": {
            "atomic_adapters": [
                {
                    "adapter": "azure.azuread.legacy_authentication_blocked",
                    "signal": {
                        "fields": ["legacyAuthDisabled"],
                        "predicate": "legacyAuthDisabled === true",
                        "paths_doc": ["GET /policies/authenticationMethodsPolicy"],
                        "evidence_type": "config_read"
                    }
                }
            ]
        },
        "azure.azuread.self_service_password_reset": {
            "atomic_adapters": [
                {
                    "adapter": "azure.azuread.self_service_password_reset_enabled",
                    "signal": {
                        "fields": ["selfServicePasswordResetEnabled"],
                        "predicate": "selfServicePasswordResetEnabled === true",
                        "paths_doc": ["GET /policies/authenticationMethodsPolicy"],
                        "evidence_type": "config_read"
                    }
                }
            ]
        },
        "azure.azuread.authentication_methods": {
            "atomic_adapters": [
                {
                    "adapter": "azure.azuread.authentication_methods_available",
                    "signal": {
                        "fields": ["availableMethods"],
                        "predicate": "Array.isArray(availableMethods) && availableMethods.length >= 2",
                        "paths_doc": ["GET /policies/authenticationMethodsPolicy -> authenticationMethods"],
                        "evidence_type": "config_read"
                    }
                }
            ]
        },
        
        # Storage patterns
        "azure.storage.https_required": {
            "atomic_adapters": [
                {
                    "adapter": "azure.storage.account_https_only",
                    "signal": {
                        "fields": ["httpsOnly", "minimumTlsVersion"],
                        "predicate": "httpsOnly === true && compareTls(minimumTlsVersion, 'TLS1_2') >= 0",
                        "paths_doc": ["properties.supportsHttpsTrafficOnly", "properties.minimumTlsVersion"],
                        "evidence_type": "config_read"
                    }
                }
            ]
        },
        "azure.storage.public_access_block": {
            "atomic_adapters": [
                {
                    "adapter": "azure.storage.public_access_disabled",
                    "signal": {
                        "fields": ["publicNetworkAccess"],
                        "predicate": "publicNetworkAccess === 'Disabled'",
                        "paths_doc": ["properties.publicNetworkAccess"],
                        "evidence_type": "config_read"
                    }
                }
            ]
        },
        "azure.storage.encryption_at_rest": {
            "atomic_adapters": [
                {
                    "adapter": "azure.storage.encryption_enabled",
                    "signal": {
                        "fields": ["encryption"],
                        "predicate": "encryption.services.blob.enabled === true && encryption.services.file.enabled === true",
                        "paths_doc": ["properties.encryption"],
                        "evidence_type": "config_read"
                    }
                }
            ]
        },
        
        # Key Vault patterns
        "azure.keyvault.secret_encryption": {
            "atomic_adapters": [
                {
                    "adapter": "azure.keyvault.secret_encryption_enabled",
                    "signal": {
                        "fields": ["enabledForDiskEncryption", "enabledForTemplateDeployment"],
                        "predicate": "enabledForDiskEncryption === true",
                        "paths_doc": ["properties.enabledForDiskEncryption"],
                        "evidence_type": "config_read"
                    }
                }
            ]
        },
        "azure.keyvault.secret_access_policies": {
            "atomic_adapters": [
                {
                    "adapter": "azure.keyvault.access_policies_restrictive",
                    "signal": {
                        "fields": ["accessPolicies"],
                        "predicate": "accessPolicies.every(p => p.permissions.secrets.includes('get') && !p.permissions.secrets.includes('all'))",
                        "paths_doc": ["properties.accessPolicies"],
                        "evidence_type": "config_read"
                    }
                }
            ]
        },
        
        # Compute patterns
        "azure.compute.vm_security_baseline": {
            "atomic_adapters": [
                {
                    "adapter": "azure.compute.vm_disk_encryption_enabled",
                    "signal": {
                        "fields": ["diskEncryptionEnabled"],
                        "predicate": "diskEncryptionEnabled === true",
                        "paths_doc": ["properties.storageProfile.osDisk.encryptionSettings"],
                        "evidence_type": "config_read"
                    }
                }
            ]
        },
        
        # Network patterns
        "azure.network.nsg_rules": {
            "atomic_adapters": [
                {
                    "adapter": "azure.network.nsg_rules_restrictive",
                    "signal": {
                        "fields": ["securityRules"],
                        "predicate": "securityRules.every(r => r.destinationPortRange !== '3389' && r.destinationPortRange !== '22')",
                        "paths_doc": ["properties.securityRules"],
                        "evidence_type": "config_read"
                    }
                }
            ]
        },
        "azure.network.nsg_default_deny": {
            "atomic_adapters": [
                {
                    "adapter": "azure.network.nsg_default_deny_inbound",
                    "signal": {
                        "fields": ["defaultSecurityRules"],
                        "predicate": "defaultSecurityRules.some(r => r.name === 'DenyAllInBound' && r.access === 'Deny')",
                        "paths_doc": ["properties.defaultSecurityRules"],
                        "evidence_type": "config_read"
                    }
                }
            ]
        }
    }
    
    # Process each assertion category
    for assertion_key, tiers in original_matrix.items():
        enriched_matrix[assertion_key] = {}
        
        for tier_name, rows in tiers.items():
            enriched_rows = []
            
            for row in rows:
                adapter = row.get('adapter', '')
                
                # Check if we have enrichment patterns for this adapter
                if adapter in enrichment_patterns:
                    # Split into atomic adapters
                    for atomic_adapter in enrichment_patterns[adapter]['atomic_adapters']:
                        enriched_row = {
                            "service": row.get('service', ''),
                            "resource": row.get('resource', ''),
                            "resource_type": row.get('resource_type', ''),
                            "adapter": atomic_adapter['adapter'],
                            "coverage_tier": tier_name,
                            "not_applicable_when": row.get('not_applicable_when', ''),
                            "signal": atomic_adapter['signal']
                        }
                        
                        # Add params if they exist
                        if 'params' in atomic_adapter:
                            enriched_row['params'] = atomic_adapter['params']
                        
                        enriched_rows.append(enriched_row)
                else:
                    # Use default enrichment pattern
                    enriched_row = {
                        "service": row.get('service', ''),
                        "resource": row.get('resource', ''),
                        "resource_type": row.get('resource_type', ''),
                        "adapter": adapter,
                        "coverage_tier": tier_name,
                        "not_applicable_when": row.get('not_applicable_when', ''),
                        "signal": {
                            "fields": ["enabled", "configured"],
                            "predicate": "enabled === true && configured === true",
                            "paths_doc": [f"GET /{adapter.replace('.', '/')}"],
                            "evidence_type": "config_read"
                        }
                    }
                    enriched_rows.append(enriched_row)
            
            enriched_matrix[assertion_key][tier_name] = enriched_rows
    
    # Write the enriched matrix
    output_path = "/Users/apple/Desktop/compliance_Database/rule-generator-engine/Step3-matrices-per-cloud-provider/azure_matrix_2025-01-09_enriched_complete.json"
    with open(output_path, 'w') as f:
        json.dump(enriched_matrix, f, indent=2)
    
    print(f"Enriched matrix written to {output_path}")
    return enriched_matrix

if __name__ == "__main__":
    enrich_azure_matrix()
