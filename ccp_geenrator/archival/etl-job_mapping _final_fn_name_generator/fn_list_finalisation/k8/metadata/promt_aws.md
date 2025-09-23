Create the metdata file for a program which checks the threat under a CSPM tools . The formate used would be etl-job_mapping _final_fn_name_generator/fn_list_finalisation/aws/metadata/metdata_formate.yml. Below are few sample and rpwler threat check function also can be taken as reference.

sample 1:

# checks/k8s/policy/K8S_GK_PRIVILEGED_BLOCKED.yaml
service: k8s-policy
discovery:
  - discovery_id: gatekeeper_status
    calls:
      - action: k8s_gatekeeper_installed
        fields: [{ path: installed, var: gk }]
      - action: k8s_gatekeeper_get_constraint
        with: { name: k8spspprivilegedcontainer }
        fields:
          - path: spec.enforcementAction
            var: enforcement_action
          - path: status.violations_count
            var: violations
checks:
  - check_id: K8S_GK_PRIVILEGED_BLOCKED
    calls:
      - action: get_from_discovery
        fields:
          - path: gk
            operator: equals
            expected: true
          - path: enforcement_action
            operator: in
            expected: ["deny"]
          - path: violations
            operator: equals_or_null_zero
            expected: 0
    multi_step: false
    logic: AND
    errors_as_fail: []


sample 2:

CheckID: K8S_APISERVER_AUDIT_LOG_ENABLED
CheckTitle: Kubernetes API server should have audit logging enabled
ServiceName: k8s-apiserver
SubServiceName: ""
Provider: k8s
Severity: high
Type: runtime
ResourceType: cluster
Description: >
  Validates that the Kubernetes API server is configured to log audit events 
  for monitoring and compliance.
Risk: >
  Lack of audit logging makes it difficult to identify unauthorized API calls, 
  detect privilege misuse, or investigate incidents.
Remediation: >
  Configure the API server with the --audit-log-path and related flags, 
  and provide an audit policy file.
References:
  - https://kubernetes.io/docs/tasks/debug/debug-cluster/audit/
