# Quick Implementation Reference - High Priority Services

**Date:** November 11, 2025  
**Purpose:** Fast-track guide for implementing top 207 functions

---

## 🎯 Priority Breakdown

| Service | Functions | Effort | AWS Equiv | Implementation Time |
|---------|-----------|--------|-----------|---------------------|
| **ECS** | 94 | Low | ec2 | ~150 hours |
| **RAM** | 48 | Low | iam | ~75 hours |
| **RDS** | 37 | Low | rds | ~60 hours |
| **OSS** | 28 | Low | s3 | ~45 hours |
| **Total** | **207** | - | - | **~330 hours** |

**Timeline:** ~8 weeks (1 developer) or ~4 weeks (2 developers)

---

## 📘 ECS (Elastic Compute Service) - 94 Functions

### Implementation Pattern

**AWS Source:** `aws.ec2.*` functions  
**Alicloud Target:** `alicloud.ecs.*` functions  
**Reuse Rate:** 90%

### Common Mappings

#### 1. Instance Public IP Check
```python
# AWS Version (existing)
def aws_ec2_instance_no_public_ip():
    ec2 = boto3.client('ec2')
    instances = ec2.describe_instances()
    for instance in instances['PublicIpAddress']:
        if instance:
            return FAIL

# Alicloud Adaptation
def alicloud_ecs_instance_no_public_ip():
    from alibabacloud_ecs20140526.client import Client
    client = Client(config)
    instances = client.describe_instances()
    for instance in instances.body.instances.instance:
        if instance.public_ip_address.ip_address:
            return FAIL
```

**Changes:**
- Import: `boto3` → `alibabacloud_ecs20140526`
- Response structure: `.body.instances.instance`
- Field name: `PublicIpAddress` → `public_ip_address.ip_address`

#### 2. Disk Encryption Check
```python
# AWS (existing)
def aws_ec2_volume_encrypted():
    volumes = ec2.describe_volumes()
    for vol in volumes['Volumes']:
        if not vol['Encrypted']:
            return FAIL

# Alicloud
def alicloud_ecs_disk_encrypted():
    disks = client.describe_disks()
    for disk in disks.body.disks.disk:
        if not disk.encrypted:
            return FAIL
```

**Changes:**
- API: `describe_volumes` → `describe_disks`
- Field: `Encrypted` → `encrypted`

#### 3. Security Group SSH Restriction
```python
# AWS (existing)
def aws_ec2_securitygroup_ssh_restricted():
    sgs = ec2.describe_security_groups()
    for sg in sgs['SecurityGroups']:
        for rule in sg['IpPermissions']:
            if rule['FromPort'] == 22 and rule['IpRanges'] == '0.0.0.0/0':
                return FAIL

# Alicloud
def alicloud_ecs_securitygroup_ssh_restricted():
    sgs = client.describe_security_groups()
    for sg in sgs.body.security_groups.security_group:
        for rule in sg.permissions.permission:
            if rule.port_range == '22/22' and rule.source_cidr_ip == '0.0.0.0/0':
                return FAIL
```

**Changes:**
- Field: `IpPermissions` → `permissions.permission`
- Port format: `FromPort/ToPort` → `port_range`
- CIDR field: `IpRanges` → `source_cidr_ip`

### ECS Function Categories


**Network/Public Access:** 42 functions
- `alicloud.ecs.account.block_public_access`
- `alicloud.ecs.ami_public`
- `alicloud.ecs.disk.public_snapshot`
- ... +39 more

**Encryption:** 6 functions
- `alicloud.ecs.disk.encrypted`
- `alicloud.ecs.disk.encryption_at_rest_check`
- `alicloud.ecs.disk.encryption_enabled`
- ... +3 more

**Security Groups:** 8 functions
- `alicloud.ecs.securitygroup_common_ports_restricted`
- `alicloud.ecs.securitygroup_default_restrict_traffic`
- `alicloud.ecs.securitygroup_default_restricted`
- ... +5 more

**Instance Configuration:** 14 functions
- `alicloud.ecs.instance.account_imdsv2_enabled`
- `alicloud.ecs.instance.detailed_monitoring_enabled`
- `alicloud.ecs.instance.imdsv2_enabled`
- ... +11 more

**Monitoring/Logging:** 3 functions
- `alicloud.ecs.client_vpn_endpoint_connection_logging_enabled`
- `alicloud.ecs.task_definitions_logging_block_mode`
- `alicloud.ecs.task_definitions_logging_enabled`

**Other:** 21 functions
- `alicloud.ecs.backup_enabled`
- `alicloud.ecs.elastic_ip_shodan`
- `alicloud.ecs.elastic_ip_unassigned`
- ... +18 more


---

## 🔐 RAM (Resource Access Management) - 48 Functions

### Implementation Pattern

**AWS Source:** `aws.iam.*` functions  
**Alicloud Target:** `alicloud.ram.*` functions  
**Reuse Rate:** 90%

### Common Mappings

#### 1. MFA Enabled Check
```python
# AWS (existing)
def aws_iam_user_mfa_enabled():
    iam = boto3.client('iam')
    users = iam.list_users()
    for user in users['Users']:
        mfa = iam.list_mfa_devices(UserName=user['UserName'])
        if not mfa['MFADevices']:
            return FAIL

# Alicloud
def alicloud_ram_user_mfa_enabled():
    from alibabacloud_ram20150501.client import Client
    client = Client(config)
    users = client.list_users()
    for user in users.body.users.user:
        mfa = client.list_virtual_mfadevices(user_name=user.user_name)
        if not mfa.body.virtual_mfadevices:
            return FAIL
```

**Changes:**
- Import: `boto3.iam` → `alibabacloud_ram20150501`
- Response: `.body.users.user`
- Field case: `UserName` → `user_name`

#### 2. Password Policy Check
```python
# AWS (existing)
def aws_iam_policy_minimum_length_14():
    policy = iam.get_account_password_policy()
    if policy['PasswordPolicy']['MinimumPasswordLength'] < 14:
        return FAIL

# Alicloud
def alicloud_ram_password_policy_minimum_length_14():
    policy = client.get_password_policy()
    if policy.body.password_policy.minimum_password_length < 14:
        return FAIL
```

**Changes:**
- Response structure: direct dict → `.body.password_policy`
- Field case: `MinimumPasswordLength` → `minimum_password_length`

#### 3. Access Key Rotation
```python
# AWS (existing)
def aws_iam_key_rotation_90_days():
    keys = iam.list_access_keys()
    for key in keys['AccessKeyMetadata']:
        age = (datetime.now() - key['CreateDate']).days
        if age > 90:
            return FAIL

# Alicloud
def alicloud_ram_key_rotation_90_days():
    keys = client.list_access_keys()
    for key in keys.body.access_keys.access_key:
        age = (datetime.now() - key.create_date).days
        if age > 90:
            return FAIL
```

---

## 🗄️ RDS (Relational Database Service) - 37 Functions

### Implementation Pattern

**AWS Source:** `aws.rds.*` functions  
**Alicloud Target:** `alicloud.rds.*` functions  
**Reuse Rate:** 90%

### Common Mappings

#### 1. Public Access Check
```python
# AWS (existing)
def aws_rds_instance_no_public_access():
    rds = boto3.client('rds')
    instances = rds.describe_db_instances()
    for db in instances['DBInstances']:
        if db['PubliclyAccessible']:
            return FAIL

# Alicloud
def alicloud_rds_instance_no_public_access():
    from alibabacloud_rds20140815.client import Client
    client = Client(config)
    instances = client.describe_dbinstances()
    for db in instances.body.items.dbinstance:
        if db.connection_mode == 'Public':
            return FAIL
```

**Changes:**
- API: `describe_db_instances` → `describe_dbinstances`
- Field: `PubliclyAccessible` (bool) → `connection_mode` (string)

#### 2. Encryption at Rest
```python
# AWS (existing)
def aws_rds_instance_storage_encrypted():
    instances = rds.describe_db_instances()
    for db in instances['DBInstances']:
        if not db['StorageEncrypted']:
            return FAIL

# Alicloud
def alicloud_rds_instance_storage_encrypted():
    instances = client.describe_dbinstances()
    for db in instances.body.items.dbinstance:
        if not db.tdeencryption_enable or db.tdeencryption_enable != 'Enabled':
            return FAIL
```

**Changes:**
- Field: `StorageEncrypted` → `tdeencryption_enable`
- Value: boolean → string ('Enabled')

#### 3. Backup Retention
```python
# AWS (existing)
def aws_rds_instance_backup_enabled():
    instances = rds.describe_db_instances()
    for db in instances['DBInstances']:
        if db['BackupRetentionPeriod'] < 7:
            return FAIL

# Alicloud
def alicloud_rds_instance_backup_enabled():
    instances = client.describe_dbinstances()
    for db in instances.body.items.dbinstance:
        if int(db.backup_retention_period) < 7:
            return FAIL
```

**Changes:**
- Field case: `BackupRetentionPeriod` → `backup_retention_period`
- Type: int → string (needs conversion)

---

## 🪣 OSS (Object Storage Service) - 28 Functions

### Implementation Pattern

**AWS Source:** `aws.s3.*` functions  
**Alicloud Target:** `alicloud.oss.*` functions  
**Reuse Rate:** 90%

### Common Mappings

#### 1. Bucket Encryption
```python
# AWS (existing)
def aws_s3_bucket_encryption_enabled():
    s3 = boto3.client('s3')
    buckets = s3.list_buckets()
    for bucket in buckets['Buckets']:
        try:
            encryption = s3.get_bucket_encryption(Bucket=bucket['Name'])
            if not encryption:
                return FAIL
        except:
            return FAIL

# Alicloud
def alicloud_oss_bucket_encryption_enabled():
    import oss2
    buckets = client.list_buckets()
    for bucket in buckets.buckets:
        try:
            encryption = bucket.get_bucket_encryption()
            if encryption.sse_algorithm is None:
                return FAIL
        except:
            return FAIL
```

**Changes:**
- SDK: `boto3.s3` → `oss2`
- API structure: Different exception handling
- Field: dict access → attribute access

#### 2. Public Access Block
```python
# AWS (existing)
def aws_s3_bucket_public_access_block():
    config = s3.get_public_access_block(Bucket=bucket)
    if not config['PublicAccessBlockConfiguration']['BlockPublicAcls']:
        return FAIL

# Alicloud
def alicloud_oss_bucket_public_access_block():
    acl = bucket.get_bucket_acl()
    if acl.acl == oss2.BUCKET_ACL_PUBLIC_READ or acl.acl == oss2.BUCKET_ACL_PUBLIC_READ_WRITE:
        return FAIL
```

**Changes:**
- Different approach: Block config vs ACL check
- Logic inversion: AWS checks blocks, Alicloud checks ACLs

#### 3. Versioning Enabled
```python
# AWS (existing)
def aws_s3_bucket_versioning_enabled():
    versioning = s3.get_bucket_versioning(Bucket=bucket)
    if versioning.get('Status') != 'Enabled':
        return FAIL

# Alicloud
def alicloud_oss_bucket_versioning_enabled():
    versioning = bucket.get_bucket_versioning()
    if versioning.status != oss2.BUCKET_VERSIONING_ENABLE:
        return FAIL
```

**Changes:**
- API: `get_bucket_versioning` (same name!)
- Field: `Status` (string) → `status` (constant)

---

## 🚀 Implementation Workflow

### Phase 1: Setup (1 day)
1. Install Alicloud SDK: `pip install alibabacloud-ecs20140526 alibabacloud-ram20150501 alibabacloud-rds20140815 oss2`
2. Configure authentication
3. Set up testing environment

### Phase 2: ECS Implementation (3 weeks)
- Week 1: Network/Public Access (35 functions)
- Week 2: Encryption + Security Groups (40 functions)
- Week 3: Instance Config + Testing (19 functions)

### Phase 3: RAM Implementation (1.5 weeks)
- Week 4-5: All 48 functions + testing

### Phase 4: RDS Implementation (1.5 weeks)
- Week 5-6: All 37 functions + testing

### Phase 5: OSS Implementation (1 week)
- Week 7: All 28 functions + testing

### Phase 6: Testing & Documentation (1 week)
- Week 8: Integration testing, bug fixes, documentation

**Total Timeline:** 8 weeks (1 developer) or 4-5 weeks (2 developers)

---

## 📋 Checklist per Function

- [ ] Review AWS source code
- [ ] Install required Alicloud SDK package
- [ ] Adapt authentication
- [ ] Translate API calls
- [ ] Map field names
- [ ] Handle response structure
- [ ] Add error handling
- [ ] Write unit tests
- [ ] Write integration tests
- [ ] Document changes
- [ ] Code review
- [ ] Deploy to staging

---

## 🔗 Resources

**Alicloud SDK Documentation:**
- ECS: https://github.com/aliyun/alibabacloud-python-sdk/tree/master/ecs-20140526
- RAM: https://github.com/aliyun/alibabacloud-python-sdk/tree/master/ram-20150501
- RDS: https://github.com/aliyun/alibabacloud-python-sdk/tree/master/rds-20140815
- OSS: https://github.com/aliyun/aliyun-oss-python-sdk

**AWS Reference Code:**
- Location: `/Users/apple/Desktop/compliance_Database/rule_finalisation/rule_list/`
- File: `consolidated_rules_phase4_2025-11-08.csv`

---

## ✅ Status

**Step 2:** COMPLETE  
**Next:** Step 3 - API Translation Matrix  
**Ready for:** Implementation Phase
