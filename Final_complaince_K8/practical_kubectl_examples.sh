#!/bin/bash
# Practical kubectl examples for K8s security functions

echo "🔐 Kubernetes Security Functions - Practical kubectl Examples"
echo "============================================================="

# Function 1: Check cluster-admin role bindings
echo "1. k8s_rbac_cluster_admin_role_bound"
echo "   Checking cluster-admin role bindings..."
echo "   Command: kubectl get clusterrolebindings -o wide | grep cluster-admin"
echo "   Example output:"
echo "   cluster-admin   ClusterRole/cluster-admin   2d   system:masters"
echo ""

# Function 2: Detect wildcard permissions
echo "2. k8s_rbac_wildcard_access_detected"
echo "   Checking for wildcard permissions..."
echo "   Command: kubectl get clusterroles -o jsonpath='{range .items[*]}{.metadata.name}{\"\\n\"}{range .rules[*]}{.verbs}{\"\\t\"}{.resources}{\"\\n\"}{end}{end}' | grep -E \"\\*|all\""
echo "   Example output:"
echo "   admin-role     *     *"
echo "   power-user     get,list,watch     *"
echo ""

# Function 3: Check system user bindings
echo "3. k8s_rbac_binding_to_system_users_detected"
echo "   Checking for system user bindings..."
echo "   Command: kubectl get clusterrolebindings -o jsonpath='{range .items[*]}{.metadata.name}{\"\\t\"}{.subjects[*].name}{\"\\n\"}{end}' | grep \"system:\""
echo "   Example output:"
echo "   system:controller:deployment-controller    system:serviceaccount:kube-system:deployment-controller"
echo "   system:controller:node-controller          system:serviceaccount:kube-system:node-controller"
echo ""

# Function 4: Check least privilege enforcement
echo "4. k8s_rbac_least_privilege_enforcement"
echo "   Checking for excessive permissions..."
echo "   Command: kubectl get clusterroles -o jsonpath='{range .items[*]}{.metadata.name}{\"\\n\"}{range .rules[*]}{.verbs}{\"\\n\"}{end}{end}' | grep \"bind\""
echo "   Example output:"
echo "   cluster-admin"
echo "   bind"
echo "   escalate"
echo ""

# Function 5: Check network policies
echo "5. k8s_network_policy_missing"
echo "   Checking for missing network policies..."
echo "   Command: kubectl get networkpolicies --all-namespaces"
echo "   Example output:"
echo "   NAMESPACE   NAME           POD-SELECTOR   AGE"
echo "   default     deny-all       <none>         1d"
echo "   production  web-policy     app=web        2d"
echo ""

# Function 6: Check privileged pods
echo "6. k8s_pod_privileged_enabled"
echo "   Checking for privileged pods..."
echo "   Command: kubectl get pods --all-namespaces -o jsonpath='{range .items[*]}{.metadata.namespace}{\"\\t\"}{.metadata.name}{\"\\t\"}{.spec.securityContext.privileged}{\"\\n\"}{end}' | grep \"true\""
echo "   Example output:"
echo "   kube-system   privileged-pod   true"
echo ""

# Function 7: Check service account usage
echo "7. k8s_service_account_default_usage_check"
echo "   Checking for default service account usage..."
echo "   Command: kubectl get pods --all-namespaces -o jsonpath='{range .items[*]}{.metadata.namespace}{\"\\t\"}{.metadata.name}{\"\\t\"}{.spec.serviceAccountName}{\"\\n\"}{end}' | grep \"default\""
echo "   Example output:"
echo "   default       web-pod          default"
echo "   production    api-pod          default"
echo ""

# Function 8: Check audit configuration
echo "8. k8s_audit_policy_missing"
echo "   Checking for audit policy..."
echo "   Command: kubectl get configmap -n kube-system audit-policy -o yaml"
echo "   Example output:"
echo "   apiVersion: v1"
echo "   kind: ConfigMap"
echo "   metadata:"
echo "     name: audit-policy"
echo "     namespace: kube-system"
echo ""

echo "🚀 Complete Security Check Script"
echo "================================="
echo "Here's a complete script that runs all checks:"
echo ""

cat << 'EOF'
#!/bin/bash
# Complete K8s security assessment

echo "🔐 Starting Kubernetes Security Assessment..."
echo "============================================="

# 1. RBAC Security Checks
echo "1. RBAC Security Checks"
echo "-----------------------"

echo "Checking cluster-admin bindings..."
kubectl get clusterrolebindings -o wide | grep cluster-admin

echo "Checking for wildcard permissions..."
kubectl get clusterroles -o jsonpath='{range .items[*]}{.metadata.name}{"\n"}{range .rules[*]}{.verbs}{"\t"}{.resources}{"\n"}{end}{end}' | grep -E "\*|all"

echo "Checking for bind/escalate permissions..."
kubectl get clusterroles -o jsonpath='{range .items[*]}{.metadata.name}{"\n"}{range .rules[*]}{.verbs}{"\n"}{end}{end}' | grep -E "bind|escalate"

# 2. Network Security Checks
echo "2. Network Security Checks"
echo "--------------------------"

echo "Checking for network policies..."
kubectl get networkpolicies --all-namespaces

echo "Namespaces without network policies:"
for ns in $(kubectl get namespaces -o jsonpath='{.items[*].metadata.name}'); do
  if ! kubectl get networkpolicies -n $ns >/dev/null 2>&1; then
    echo "  - $ns"
  fi
done

# 3. Pod Security Checks
echo "3. Pod Security Checks"
echo "----------------------"

echo "Checking for privileged pods..."
kubectl get pods --all-namespaces -o jsonpath='{range .items[*]}{.metadata.namespace}{"\t"}{.metadata.name}{"\t"}{.spec.securityContext.privileged}{"\n"}{end}' | grep "true"

echo "Checking for default service account usage..."
kubectl get pods --all-namespaces -o jsonpath='{range .items[*]}{.metadata.namespace}{"\t"}{.metadata.name}{"\t"}{.spec.serviceAccountName}{"\n"}{end}' | grep "default"

# 4. Audit Configuration
echo "4. Audit Configuration"
echo "----------------------"

echo "Checking audit policy..."
kubectl get configmap -n kube-system audit-policy -o yaml 2>/dev/null || echo "No audit policy found"

echo "✅ Security assessment completed!"
EOF

echo ""
echo "📊 How to Use These Commands:"
echo "============================="
echo "1. Save the script above as 'k8s-security-check.sh'"
echo "2. Make it executable: chmod +x k8s-security-check.sh"
echo "3. Run it: ./k8s-security-check.sh"
echo ""
echo "4. For individual checks, use the specific kubectl commands shown above"
echo "5. Pipe output to files for analysis: kubectl get clusterrolebindings > rbac-check.txt"
echo "6. Use jq for JSON parsing: kubectl get clusterroles -o json | jq '.items[].metadata.name'"
echo ""
echo "🎯 Key Benefits:"
echo "==============="
echo "✅ All functions use standard kubectl commands"
echo "✅ No additional tools or plugins required"
echo "✅ Can be automated and scheduled"
echo "✅ Output can be parsed and analyzed"
echo "✅ Works with any Kubernetes cluster"
echo "✅ Provides real-time security assessment"
