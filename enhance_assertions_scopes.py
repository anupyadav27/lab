#!/usr/bin/env python3
import json
from pathlib import Path

def enhance_assertions_with_scope_coverage():
    """Enhance assertions pack with improved scope coverage and Azure-specific mappings"""
    
    # Load existing assertions
    assertions_path = "/Users/apple/Desktop/compliance_Database/rule-generator-engine/step-2-common-assercian-id/assertions_pack_final_2025-09-11T18-41-14.json"
    with open(assertions_path, 'r') as f:
        assertions_data = json.load(f)
    
    # Enhanced scope allowlist with Azure-specific mappings
    enhanced_scope_allowlist = [
        # Identity & Access
        "identity.user",
        "identity.role", 
        "identity.tenant",
        "identity.service_account",
        "identity.group",
        "identity.application",
        "identity.policy",
        
        # RBAC & Authorization
        "rbac.role",
        "rbac.group", 
        "rbac.policy",
        
        # Secrets & Key Management
        "secrets.store",
        "secrets.secret",
        "crypto.kms",
        "crypto.kms.key",
        "crypto.certificate",
        "keyvault.vault",
        
        # Storage & Data
        "storage.bucket",
        "storage.object",
        "storage.fileshare",
        "storage.queue",
        "storage.table",
        "storage.snapshot",
        "storage.volume",
        
        # Database
        "db.instance",
        "db.cluster",
        "db.user",
        
        # Compute
        "compute.vm",
        "compute.image",
        "compute.disk",
        "compute.instance_group",
        
        # Networking
        "network.vpc",
        "network.subnet",
        "network.security_group",
        "network.firewall",
        "network.load_balancer",
        "network.gateway",
        "network.endpoint",
        "network.route_table",
        "network.connection",
        "network.ddos_plan",
        "network.waf",
        
        # DNS
        "dns.zone",
        "dns.hosted_zone",
        "dns.resolver",
        
        # Edge & CDN
        "edge.waf",
        "edge.cdn",
        
        # Kubernetes
        "k8s.cluster",
        "k8s.node_pool",
        "k8s.namespace",
        "k8s.workload",
        "k8s.admission",
        "k8s.network_policy",
        
        # Serverless & PaaS
        "serverless.function",
        "paas.app",
        
        # Registry & Supply Chain
        "registry.repo",
        "registry.policy",
        "repository",
        
        # Logging & Monitoring
        "logging.sink",
        "logging.store",
        "logging.trail",
        "log_group",
        "monitoring.alert",
        "monitoring.metric",
        "alarm",
        "flow_log",
        
        # Platform & Control
        "platform.control_plane",
        "platform.api_endpoint",
        
        # Backup & Recovery
        "backup.plan",
        "backup.vault",
        "backup.item",
        "dr.plan",
        "replication_configuration",
        
        # Governance & Compliance
        "governance.org",
        "governance.project",
        "standards",
        "assessment",
        "findings",
        "report",
        
        # Data & Analytics
        "data.catalog",
        
        # Patch & Maintenance
        "patch_baseline",
        "patch_group",
        "maintenance_window",
        
        # Network Segmentation
        "peering",
        "route_table"
    ]
    
    # Update the assertions data
    assertions_data["scope_allowlist"] = enhanced_scope_allowlist
    
    # Add scope prefix mappings for better organization
    assertions_data["scope_prefixes"] = {
        "identity": ["identity.user", "identity.role", "identity.tenant", "identity.service_account", "identity.group", "identity.application", "identity.policy"],
        "rbac": ["rbac.role", "rbac.group", "rbac.policy"],
        "secrets": ["secrets.store", "secrets.secret"],
        "crypto": ["crypto.kms", "crypto.kms.key", "crypto.certificate", "keyvault.vault"],
        "storage": ["storage.bucket", "storage.object", "storage.fileshare", "storage.queue", "storage.table", "storage.snapshot", "storage.volume"],
        "database": ["db.instance", "db.cluster", "db.user"],
        "compute": ["compute.vm", "compute.image", "compute.disk", "compute.instance_group"],
        "network": ["network.vpc", "network.subnet", "network.security_group", "network.firewall", "network.load_balancer", "network.gateway", "network.endpoint", "network.route_table", "network.connection", "network.ddos_plan", "network.waf", "peering", "route_table"],
        "dns": ["dns.zone", "dns.hosted_zone", "dns.resolver"],
        "edge": ["edge.waf", "edge.cdn"],
        "kubernetes": ["k8s.cluster", "k8s.node_pool", "k8s.namespace", "k8s.workload", "k8s.admission", "k8s.network_policy"],
        "serverless": ["serverless.function", "paas.app"],
        "registry": ["registry.repo", "registry.policy", "repository"],
        "logging": ["logging.sink", "logging.store", "logging.trail", "log_group"],
        "monitoring": ["monitoring.alert", "monitoring.metric", "alarm", "flow_log"],
        "platform": ["platform.control_plane", "platform.api_endpoint"],
        "backup": ["backup.plan", "backup.vault", "backup.item", "dr.plan", "replication_configuration"],
        "governance": ["governance.org", "governance.project", "standards", "assessment", "findings", "report"],
        "data": ["data.catalog"],
        "patch": ["patch_baseline", "patch_group", "maintenance_window"]
    }
    
    # Add Azure-specific scope mappings
    assertions_data["azure_scope_mappings"] = {
        "identity.user": ["azuread.users", "azuread.userPools"],
        "identity.role": ["azuread.directoryRoles", "azuread.roleDefinitions"],
        "identity.tenant": ["azuread.tenant", "azuread.organization"],
        "identity.service_account": ["azuread.servicePrincipals", "azuread.applications"],
        "identity.group": ["azuread.groups", "azuread.groupMemberships"],
        "identity.application": ["azuread.applications", "azuread.appRegistrations"],
        "identity.policy": ["azuread.policies", "azuread.conditionalAccessPolicies"],
        
        "rbac.role": ["azure.authorization.roleDefinitions", "azure.authorization.roleAssignments"],
        "rbac.group": ["azure.authorization.roleAssignments"],
        "rbac.policy": ["azure.authorization.policyDefinitions", "azure.authorization.policyAssignments"],
        
        "secrets.store": ["azure.keyvault.vaults"],
        "secrets.secret": ["azure.keyvault.secrets"],
        "crypto.kms": ["azure.keyvault.vaults"],
        "crypto.kms.key": ["azure.keyvault.keys"],
        "crypto.certificate": ["azure.keyvault.certificates"],
        "keyvault.vault": ["azure.keyvault.vaults"],
        
        "storage.bucket": ["azure.storage.storageAccounts", "azure.storage.containers"],
        "storage.object": ["azure.storage.blobs"],
        "storage.fileshare": ["azure.storage.fileShares"],
        "storage.queue": ["azure.storage.queues", "azure.servicebus.queues"],
        "storage.table": ["azure.storage.tables", "azure.cosmosdb.tables"],
        "storage.snapshot": ["azure.compute.snapshots"],
        "storage.volume": ["azure.compute.disks"],
        
        "db.instance": ["azure.sql.servers", "azure.sql.databases", "azure.cosmosdb.accounts"],
        "db.cluster": ["azure.sql.servers", "azure.cosmosdb.accounts"],
        "db.user": ["azure.sql.databaseUsers"],
        
        "compute.vm": ["azure.compute.virtualMachines"],
        "compute.image": ["azure.compute.images"],
        "compute.disk": ["azure.compute.disks"],
        "compute.instance_group": ["azure.compute.virtualMachineScaleSets"],
        
        "network.vpc": ["azure.network.virtualNetworks"],
        "network.subnet": ["azure.network.subnets"],
        "network.security_group": ["azure.network.networkSecurityGroups"],
        "network.firewall": ["azure.network.azureFirewalls"],
        "network.load_balancer": ["azure.network.loadBalancers", "azure.network.applicationGateways"],
        "network.gateway": ["azure.network.virtualNetworkGateways"],
        "network.endpoint": ["azure.network.privateEndpoints"],
        "network.route_table": ["azure.network.routeTables"],
        "network.connection": ["azure.network.connections"],
        "network.ddos_plan": ["azure.network.ddosProtectionPlans"],
        "network.waf": ["azure.network.webApplicationFirewallPolicies"],
        
        "dns.zone": ["azure.dns.zones"],
        "dns.hosted_zone": ["azure.dns.zones"],
        "dns.resolver": ["azure.dns.resolvers"],
        
        "edge.waf": ["azure.frontdoor.webApplicationFirewallPolicies"],
        "edge.cdn": ["azure.cdn.profiles"],
        
        "k8s.cluster": ["azure.containerservice.managedClusters"],
        "k8s.node_pool": ["azure.containerservice.agentPools"],
        "k8s.namespace": ["azure.containerservice.managedClusters"],
        "k8s.workload": ["azure.containerservice.managedClusters"],
        "k8s.admission": ["azure.containerservice.managedClusters"],
        "k8s.network_policy": ["azure.containerservice.managedClusters"],
        
        "serverless.function": ["azure.web.sites", "azure.web.serverFarms"],
        "paas.app": ["azure.web.sites", "azure.web.serverFarms"],
        
        "registry.repo": ["azure.containerregistry.registries"],
        "registry.policy": ["azure.containerregistry.registries"],
        "repository": ["azure.containerregistry.repositories"],
        
        "logging.sink": ["azure.insights.diagnosticSettings"],
        "logging.store": ["azure.operationalinsights.workspaces"],
        "logging.trail": ["azure.insights.activityLogs"],
        "log_group": ["azure.operationalinsights.workspaces"],
        
        "monitoring.alert": ["azure.insights.metricAlerts"],
        "monitoring.metric": ["azure.insights.metrics"],
        "alarm": ["azure.insights.metricAlerts"],
        "flow_log": ["azure.network.flowLogs"],
        
        "platform.control_plane": ["azure.containerservice.managedClusters"],
        "platform.api_endpoint": ["azure.apimanagement.services"],
        
        "backup.plan": ["azure.recoveryservices.backupPolicies"],
        "backup.vault": ["azure.recoveryservices.vaults"],
        "backup.item": ["azure.recoveryservices.backupItems"],
        "dr.plan": ["azure.recoveryservices.replicationPolicies"],
        "replication_configuration": ["azure.recoveryservices.replicationFabrics"],
        
        "governance.org": ["azure.management.managementGroups"],
        "governance.project": ["azure.resources.subscriptions"],
        "standards": ["azure.security.regulatoryCompliance"],
        "assessment": ["azure.security.assessments"],
        "findings": ["azure.security.assessments"],
        "report": ["azure.advisor.recommendations"],
        
        "data.catalog": ["azure.purview.accounts"],
        
        "patch_baseline": ["azure.automation.updateManagement"],
        "patch_group": ["azure.automation.updateManagement"],
        "maintenance_window": ["azure.maintenance.maintenanceConfigurations"]
    }
    
    # Update version info
    assertions_data["version"] = "1.1"
    assertions_data["pack_id"] = "assertions_pack_final_2025_09_11_enhanced"
    assertions_data["scope_coverage_enhanced"] = True
    assertions_data["total_scopes"] = len(enhanced_scope_allowlist)
    
    # Write enhanced assertions
    output_path = "/Users/apple/Desktop/compliance_Database/rule-generator-engine/step-2-common-assercian-id/assertions_pack_final_2025-09-11T18-41-14_enhanced.json"
    with open(output_path, 'w') as f:
        json.dump(assertions_data, f, indent=2)
    
    print(f"Enhanced assertions written to {output_path}")
    print(f"Total scopes: {len(enhanced_scope_allowlist)}")
    print(f"Scope prefixes: {len(assertions_data['scope_prefixes'])}")
    print(f"Azure mappings: {len(assertions_data['azure_scope_mappings'])}")
    
    return assertions_data

if __name__ == "__main__":
    enhance_assertions_with_scope_coverage()
