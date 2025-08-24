Create the metdata file for a program which checks the threat under a CSPM tools . The formate used would be etl-job_mapping _final_fn_name_generator/fn_list_finalisation/aws/metadata/metdata_formate.yml. Below are few sample and rpwler threat check function also can be taken as reference.


sample 1:

CheckID: AWS_IAM_ROOT_MFA_ENABLED
CheckTitle: Root account has MFA enabled
ServiceName: iam
SubServiceName: ""
Provider: aws
Severity: critical
Type: identity
ResourceType: account
Description: >
  Ensures that the AWS root account has multi-factor authentication (MFA) 
  enabled to protect against unauthorized access.
Risk: >
  If MFA is not enabled on the root account, attackers who compromise the root 
  credentials can gain unrestricted access, risking total account compromise.
Remediation: >
  Enable MFA on the AWS root account from the IAM console under "Security Credentials".
RelatedChecks:
  - AWS_IAM_NO_INLINE_POLICIES
  - AWS_IAM_USER_MFA_ENABLED
References:
  - https://docs.aws.amazon.com/IAM/latest/UserGuide/id_root-user.html#id_root-user_manage_mfa
  - https://docs.aws.amazon.com/whitepapers/latest/security-best-practices/security-best-practices.pdf


Sample 2: 

# metadata/aws/iam/AWS_IAM_ROOT_MFA_ENABLED.yaml
CheckID: AWS_IAM_ROOT_MFA_ENABLED
CheckTitle: Root account has MFA enabled
ServiceName: iam
SubServiceName: ""
Provider: aws
Severity: high
Type: identity
ResourceType: account
Description: >
  Checks whether the AWS account root user has an MFA device enabled.
Risk: >
  Without MFA on the root user, compromise of the root credentials may result in full
  account takeover and irreversible actions.
Remediation: >
  Enable a hardware or virtual MFA device for the root user in the IAM console.
RelatedChecks:
  - AWS_IAM_NO_ROOT_ACCESS_KEY
  - AWS_IAM_PASSWORD_POLICY_STRONG
References:
  - https://docs.aws.amazon.com/IAM/latest/UserGuide/id_root-user.html
  - https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_mfa_enable_virtual.html
Compliance:
  - Framework: NIST-800-53-Rev5
    ControlID: AC-2(1)
    Section: Automated System Account Management
  - Framework: CIS-AWS
    ControlID: 1.13
  - Framework: ISO-27001:2022
    ControlID: A.5.17
Execution:
  Engine: python
  CheckFile: checks/aws/iam/AWS_IAM_ROOT_MFA_ENABLED.yaml
  RuntimeHints:
    TimeoutMs: 8000
    MemoryMB: 256
Tags:
  - identity
  - mfa
  - root
