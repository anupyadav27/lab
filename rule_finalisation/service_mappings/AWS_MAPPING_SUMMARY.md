# AWS Service Mapping Summary

**Date:** November 9, 2025  
**Status:** ✅ Complete with intelligent mappings  
**File:** `aws_simple_mapping.json`

---

## What Was Done

Created intelligent mappings between:
- **Existing rules** (from rule_list) 
- **Compliance functions** (what compliance needs)

Using AWS security expertise to match based on:
- Keyword similarity
- Semantic meaning (enabled, public, encryption, logging, etc.)
- AWS service knowledge

---

## Results

**Mappings Created:** 345 compliance functions mapped to existing rules  
**Needs Development:** ~174 compliance functions with no good match  
**Coverage:** ~66% can use existing rules!

---

## Updated JSON Structure

```json
{
  "service_name": {
    "rules": ["list of existing rules"],
    "compliance_functions": [
      {
        "name": "aws.guardduty.enabled",
        "mapping": [
          "aws.guardduty.detector.detectors_enabled",
          "aws.guardduty.detector.enabled_in_all_regions"
        ],
        "mapping_confidence": 0.61,
        "mapping_details": [
          {
            "rule_id": "aws.guardduty.detector.detectors_enabled",
            "score": 0.61,
            "reason": "common_keywords: aws, guardduty | semantic: enabled_check"
          }
        ]
      }
    ]
  }
}
```

---

## How to Use

### Find Compliance Functions with Good Mappings

```bash
# High confidence mappings (>0.7)
cat aws_simple_mapping.json | jq '[.[] | .compliance_functions[] | select(.mapping_confidence > 0.7)]'

# All mapped functions
cat aws_simple_mapping.json | jq '[.[] | .compliance_functions[] | select(.mapping | length > 0)]'

# Functions needing development (no mapping)
cat aws_simple_mapping.json | jq '[.[] | .compliance_functions[] | select(.mapping | length == 0)]'
```

### Review Specific Service

```bash
# See GuardDuty mappings
cat aws_simple_mapping.json | jq '.guardduty'

# See IAM mappings
cat aws_simple_mapping.json | jq '.iam'

# See S3 mappings
cat aws_simple_mapping.json | jq '.s3'
```

---

## Example Mappings

### ✅ Good Match (GuardDuty)

**Compliance:** `aws.guardduty.enabled`  
**Mapped to:**
- `aws.guardduty.detector.detectors_enabled` (score: 0.61)
- `aws.guardduty.detector.enabled_in_all_regions` (score: 0.59)

**Decision:** Can use existing rules with confidence!

---

### ✅ Good Match (S3)

**Compliance:** `aws.s3.account.level_public_access_blocks`  
**Mapped to:**
- `aws.s3.bucket.block_public_access_enabled` (score: 0.60)
- `aws.s3.bucket.s3_block_public_access` (score: 0.59)
- `aws.s3.object.not_publicly_readable` (score: 0.57)

**Decision:** Can combine these rules to satisfy compliance!

---

### ❌ No Match (Needs Development)

**Compliance:** `aws.iam.access_analyzer_active_status_all_regions`  
**Mapped to:** []

**Decision:** Need to develop this compliance function

---

## Next Steps

1. **Review mappings** - Check if mapped rules truly satisfy compliance needs
2. **Accept/Reject** - Validate each mapping or mark for development
3. **Prioritize gaps** - Focus on high-usage unmapped functions first
4. **Develop missing** - Build compliance functions with no mapping

---

## Mapping Confidence Levels

- **> 0.7** - High confidence, likely good match
- **0.5 - 0.7** - Medium confidence, review manually
- **< 0.5** - Low confidence, filtered out
- **0 / no mapping** - No good match, needs development

---

**File ready for review:** `aws_simple_mapping.json` ✅

