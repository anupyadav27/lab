Create the metdata file for a program which checks the threat under a CSPM tools . The formate used would be etl-job_mapping _final_fn_name_generator/fn_list_finalisation/aws/metadata/metdata_formate.yml. Below are few sample and rpwler threat check function also can be taken as reference.


sample 1:

CheckID: AZURE_SQL_DB_AUDITING_ENABLED
CheckTitle: Azure SQL databases should have auditing enabled
ServiceName: sql
SubServiceName: database
Provider: azure
Severity: high
Type: governance
ResourceType: database
Description: >
  Ensures that auditing is enabled for all Azure SQL Databases 
  to capture security-relevant events.
Risk: >
  Without auditing, suspicious or unauthorized activities might go undetected, 
  leading to security blind spots.
Remediation: >
  Enable auditing in the Azure Portal under SQL Database -> Auditing settings.
References:
  - https://learn.microsoft.com/azure/azure-sql/database/auditing-overview
