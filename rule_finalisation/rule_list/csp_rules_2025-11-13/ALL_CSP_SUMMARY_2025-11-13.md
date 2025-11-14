# CSP Rule Lists - Generation Summary

**Generated**: 2025-11-13
**Source**: consolidated_compliance_rules_FINAL.csv

## Overview

| CSP | Total Functions | Total Services | Top 5 Services |
|-----|----------------|----------------|----------------|
| **ALICLOUD** | 904 | 134 | ecs(113), ram(68), rds(46), oss(39), cloudmonitor(36) |
| **AWS** | 716 | 128 | ec2(92), iam(61), cloudtrail(34), cloudwatch(32), rds(30) |
| **AZURE** | 888 | 102 | storage(105), monitor(88), entra(57), vm(55), defender(46) |
| **GCP** | 654 | 73 | compute(101), iam(71), logging(63), sql(49), gke(48) |
| **IBM** | 959 | 134 | vsi(96), openshift(77), iam(73), monitoring(36), cos(35) |
| **K8S** | 526 | 39 | rbac(79), audit(70), admission(53), networkpolicy(49), api(48) |
| **ORACLE** | 1175 | 136 | compute(186), identity(85), monitoring(52), database(48), object(42) |

## Files Generated

For each CSP, 4 JSON files created:

1. **`<csp>_rules_simple_<date>.json`**
   - Service → List of functions
   - Quick reference

2. **`<csp>_rules_by_service_<date>.json`**
   - Detailed structure with metadata
   - Service → Rules with details

3. **`<csp>_rules_unique_<date>.json`**
   - Flat sorted list of all unique functions

4. **`<csp>_services_summary_<date>.json`**
   - Service → Function count
   - Summary statistics

## Service Breakdown

### ALICLOUD

- **ecs**: 113 functions
- **ram**: 68 functions
- **rds**: 46 functions
- **oss**: 39 functions
- **cloudmonitor**: 36 functions
- **actiontrail**: 27 functions
- **ack**: 27 functions
- **defender**: 24 functions
- **vpc**: 18 functions
- **entra**: 17 functions

### AWS

- **ec2**: 92 functions
- **iam**: 61 functions
- **cloudtrail**: 34 functions
- **cloudwatch**: 32 functions
- **rds**: 30 functions
- **s3**: 24 functions
- **vpc**: 17 functions
- **lambda**: 16 functions
- **log**: 15 functions
- **elbv2**: 12 functions

### AZURE

- **storage**: 105 functions
- **monitor**: 88 functions
- **entra**: 57 functions
- **vm**: 55 functions
- **defender**: 46 functions
- **sql**: 44 functions
- **app**: 35 functions
- **network**: 32 functions
- **ad**: 27 functions
- **keyvault**: 24 functions

### GCP

- **compute**: 101 functions
- **iam**: 71 functions
- **logging**: 63 functions
- **sql**: 49 functions
- **gke**: 48 functions
- **storage**: 38 functions
- **cloud**: 36 functions
- **bigquery**: 23 functions
- **monitoring**: 18 functions
- **cloudsql**: 16 functions

### IBM

- **vsi**: 96 functions
- **openshift**: 77 functions
- **iam**: 73 functions
- **monitoring**: 36 functions
- **cos**: 35 functions
- **vpc**: 35 functions
- **database**: 30 functions
- **activity**: 26 functions
- **defender**: 24 functions
- **compute**: 18 functions

### K8S

- **rbac**: 79 functions
- **audit**: 70 functions
- **admission**: 53 functions
- **networkpolicy**: 49 functions
- **api**: 48 functions
- **pod**: 41 functions
- **apiserver**: 29 functions
- **etcd**: 24 functions
- **secret**: 19 functions
- **node**: 17 functions

### ORACLE

- **compute**: 186 functions
- **identity**: 85 functions
- **monitoring**: 52 functions
- **database**: 48 functions
- **object**: 42 functions
- **iam**: 37 functions
- **audit**: 35 functions
- **defender**: 33 functions
- **monitor**: 27 functions
- **cloud**: 23 functions
