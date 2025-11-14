# AWS Function Mapping Analysis

**Generated**: 2025-11-13 19:37:16
**Source**: consolidated_compliance_rules_FINAL.csv

## Summary

- **Total AWS Functions** (from compliance CSV): 716
- **Mapped Functions** (in aws_mapped_functions): 94 (13.1%)
- **Unmapped Functions** (needs mapping): 622 (86.9%)
- **Mapped Functions Needing Compliance ID Update**: 94

## Actions Required

### 1. Update Compliance IDs for Mapped Functions
- **Count**: 94 functions
- **File**: `aws_mapped_functions_compliance_update_list.json`
- **Action**: Update `aws_mapped_compliance_ids` column in consolidated CSV

### 2. Map Unmapped Functions
- **Count**: 622 functions
- **File**: `aws_unmapped_functions_needs_mapping.json`
- **Action**: Map these functions to existing engine rules

## Files Generated

### `aws_unmapped_functions_needs_mapping.json`
Functions that appear in compliance CSV but not yet in `aws_mapped_functions` column.

**Structure**:
```json
{
  "aws.iam.user.some_check": {
    "function": "aws.iam.user.some_check",
    "compliance_ids": ["compliance_id_1", "compliance_id_2", ...],
    "compliance_count": 15,
    "mapping_status": "NEEDS_MAPPING"
  }
}
```

### `aws_mapped_functions_compliance_update_list.json`
Functions already mapped, but need compliance ID updates.

**Structure**:
```json
{
  "aws.iam.user.accesskey_unused": {
    "function": "aws.iam.user.accesskey_unused",
    "updated_compliance_ids": ["new_id_1", "new_id_2", ...],
    "compliance_count": 52,
    "action_needed": "UPDATE_COMPLIANCE_IDS"
  }
}
```

## Next Steps

1. **For Unmapped Functions**:
   - Review `aws_unmapped_functions_needs_mapping.json`
   - Map each function to an existing engine rule
   - Update `aws_mapped_functions` column in consolidated CSV

2. **For Mapped Functions**:
   - Review `aws_mapped_functions_compliance_update_list.json`
   - Update `aws_mapped_compliance_ids` column with new comprehensive list
   - Ensures all compliance IDs are captured for each function

## Priority

Focus on unmapped functions first, as they represent gaps in compliance coverage.
Then update compliance IDs for already-mapped functions to ensure complete traceability.
