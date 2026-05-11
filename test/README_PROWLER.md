# Prowler Hub Compliance Frameworks Export

## Overview
Complete export of Prowler Hub compliance frameworks for CSPM compliance mapping across multiple cloud providers and technologies.

## Data Source
- **API**: https://hub.prowler.com/api/compliance
- **Generated**: October 30, 2024
- **Total Frameworks**: 72
- **Total Requirements**: 12,721

## Files Generated

### Main Files
1. **`prowler_all_compliance.csv`** (5.6 MB)
   - Combined dataset of all compliance frameworks
   - All technologies and frameworks in one file

2. **`prowler_final.py`**
   - Python script to generate CSV files from API data
   - Can be re-run to refresh data

3. **`prowler_frameworks_raw.json`** (237K lines)
   - Complete raw API response data
   - Source data for all CSV files

### Technology-Specific CSV Files

| Technology | File | Requirements | Size |
|------------|------|--------------|------|
| **AWS** | `prowler_aws_compliance.csv` | 4,928 | 2.3 MB |
| **Azure** | `prowler_azure_compliance.csv` | 2,793 | 1.2 MB |
| **GCP** | `prowler_gcp_compliance.csv` | 2,426 | 1.1 MB |
| **Kubernetes** | `prowler_kubernetes_compliance.csv` | 2,072 | 882 KB |
| **M365** | `prowler_m365_compliance.csv` | 235 | 91 KB |
| **GitHub** | `prowler_github_compliance.csv` | 121 | 34 KB |
| **NHN** | `prowler_nhn_compliance.csv` | 92 | 31 KB |
| **OCI** | `prowler_oci_compliance.csv` | 54 | 14 KB |

## CSV Structure

Each CSV contains the following columns:

| Column | Description |
|--------|-------------|
| **Technology** | Cloud provider/platform (AWS, Azure, GCP, etc.) |
| **Compliance Framework** | Framework name (CIS, PCI, ISO27001, etc.) |
| **Framework ID** | Unique framework identifier |
| **Framework Version** | Version number of the framework |
| **Requirement ID** | Unique requirement identifier |
| **Requirement Name** | Name/title of the requirement |
| **Requirement Description** | Detailed description (truncated to 200 chars) |
| **Section** | Section/category within the framework |
| **Service** | Cloud service the requirement applies to |
| **Total Checks** | Number of automated checks for this requirement |
| **Check Names** | Comma-separated list of check function names |
| **Framework Description** | Overview of the compliance framework |

## Compliance Frameworks Included

### AWS (38 frameworks)
- CIS AWS Foundations Benchmark (multiple versions)
- AWS Foundational Security Best Practices
- NIST 800-53 Rev 4 & 5
- NIST 800-171 Rev 2
- PCI DSS v3.2.1 & v4.0
- ISO27001
- HIPAA
- FedRAMP (Low, Moderate)
- SOC2
- GDPR
- And many more...

### Azure (11 frameworks)
- CIS Microsoft Azure Foundations Benchmark
- PCI DSS
- ISO27001
- NIS2
- ENS
- SOC2
- CCC
- And more...

### GCP (11 frameworks)
- CIS Google Cloud Platform Benchmark
- PCI DSS
- ISO27001
- NIS2
- ENS
- SOC2
- And more...

### Kubernetes (5 frameworks)
- CIS Kubernetes Benchmark
- PCI DSS
- ISO27001

### Others
- M365 (Microsoft 365): 3 frameworks
- GitHub: 1 framework (CIS)
- NHN: 1 framework
- OCI (Oracle Cloud): 1 framework

## Usage for CSPM Platform

1. **Compliance Mapping**: Map your controls to industry standards using the requirement IDs
2. **Check Implementation**: Use the check names to implement automated compliance checks
3. **Multi-Cloud Coverage**: Support AWS, Azure, GCP, and Kubernetes compliance
4. **Reporting**: Generate compliance reports by technology and framework

## Example Records

```csv
Technology,Compliance Framework,Framework ID,Requirement ID,Service,Total Checks
AWS,CIS,cis_v2.0.0_aws,1.1,IAM,2
AWS,PCI DSS,pci_3.2.1_aws,1.1,Network,5
Azure,ISO27001,iso27001_2013_azure,A.9.1,Identity,3
```

## Statistics

- **Frameworks**: 72 total
- **Requirements**: 12,721 total
- **AWS**: 4,928 requirements (38.7%)
- **Azure**: 2,793 requirements (22.0%)
- **GCP**: 2,426 requirements (19.1%)
- **Kubernetes**: 2,072 requirements (16.3%)
- **Others**: 502 requirements (3.9%)

## Refresh Data

To refresh the data with latest Prowler Hub compliance frameworks:

```bash
# Fetch latest data
curl -o prowler_frameworks_raw.json https://hub.prowler.com/api/compliance

# Regenerate CSV files
python3 prowler_final.py
```

## Related Files
- AWS Security Hub controls: `aws_security_hub_controls_final.csv` (440 controls)
- AWS scraper: `aws_scraper_final.py`

## Notes
- Some frameworks have 0 checks defined (manual compliance requirements)
- Check names correspond to Prowler check functions
- Descriptions are truncated to 200 characters in CSVs
- Full descriptions available in the raw JSON file

---
Generated: October 30, 2024
Source: [Prowler Hub](https://hub.prowler.com/compliance)
