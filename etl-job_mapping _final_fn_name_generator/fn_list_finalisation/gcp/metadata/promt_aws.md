Create the metdata file for a program which checks the threat under a CSPM tools . The formate used would be etl-job_mapping _final_fn_name_generator/fn_list_finalisation/aws/metadata/metdata_formate.yml. Below are few sample and rpwler threat check function also can be taken as reference.

sample 1:

CheckID: GCP_STORAGE_BUCKET_VERSIONING_ENABLED
CheckTitle: GCP Storage buckets should have versioning enabled
ServiceName: storage
SubServiceName: buckets
Provider: gcp
Severity: medium
Type: config
ResourceType: bucket
Description: >
  Checks that versioning is enabled on GCP storage buckets to prevent 
  accidental data loss.
Risk: >
  Without bucket versioning, accidental overwrites or deletions of objects 
  cannot be easily recovered.
Remediation: >
  Enable versioning on the affected GCP buckets via the console or gcloud command.
References:
  - https://cloud.google.com/storage/docs/object-versioning
