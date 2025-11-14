# Azure Function Mapping Analysis

**Generated**: 2025-11-13
**Source**: consolidated_rules_phase4_2025-11-08.csv

## Summary

- **Total Azure Functions**: 888
- **Single Mappings** (one-to-one): 527 (59.3%)
- **Duplicate Mappings** (needs resolution): 361 (40.7%)

## Analysis Results

### One-to-One Mappings (527 functions)
These functions already have a clean one-to-one mapping between compliance function and rule_id.
- **Status**: ✓ Ready to use
- **File**: `azure_recommended_one_to_one_mapping.json`
- **Confidence**: HIGH

### Duplicate Mappings (361 functions)
These functions are mapped to multiple rule_ids and need resolution to create one-to-one mapping.
- **Status**: ⚠️ Deduplicated (primary rule_id selected)
- **File**: `azure_duplicate_mappings_resolution.json`
- **Confidence**: MEDIUM
- **Action**: Review and confirm primary rule_id selection

## Top Functions with Most Rule IDs

| Function | Rule Count |
|----------|------------|
| `azure.ad.user.password.policy.minimum.length.14` | 81 |
| `azure.security.center.enabled` | 79 |
| `azure.monitor.multi.region.enabled` | 77 |
| `azure.monitor.logging.enabled` | 71 |
| `azure.hdinsight.cluster.master.nodes.no.public.ip` | 65 |
| `azure.compute.disk.public.snapshot` | 61 |
| `azure.compute.instance.public.ip` | 61 |
| `azure.monitor.storage.read.events.enabled` | 61 |
| `azure.monitor.storage.write.events.enabled` | 61 |
| `azure.load.balancer.ssl.listeners` | 56 |

## Files Generated

### 1. `azure_recommended_one_to_one_mapping.json`
**Purpose**: Complete one-to-one mapping for all Azure functions

**Structure**:
```json
{
  "metadata": {
    "total_mappings": 888,
    "single_mappings": 527,
    "deduplicated_mappings": 361
  },
  "mappings": {
    "function_name": {
      "compliance_function": "azure.xxx.yyy",
      "engine_rule": "azure.xxx.yyy",
      "compliance_ids": "primary_rule_id",
      "mapping_type": "SINGLE|DEDUPLICATED",
      "confidence": "HIGH|MEDIUM"
    }
  }
}
```

### 2. `azure_duplicate_mappings_resolution.json`
**Purpose**: Detailed view of functions with multiple rule_id mappings

**Structure**:
```json
{
  "metadata": {
    "total_functions_with_duplicates": 361
  },
  "duplicates": {
    "function_name": {
      "compliance_function": "azure.xxx.yyy",
      "all_rule_ids": ["rule1", "rule2", ...],
      "rule_count": 5,
      "primary_rule_id": "rule1",
      "status": "NEEDS_REVIEW"
    }
  }
}
```

## Deduplication Strategy

For functions mapped to multiple rule_ids:
1. **Primary Selection**: First rule_id selected as primary (can be refined based on:
   - Framework priority (e.g., CIS > NIST > ISO)
   - Semantic similarity between function and rule description
   - Service alignment
   
2. **Confidence Levels**:
   - **HIGH**: Single mapping, no ambiguity
   - **MEDIUM**: Multiple mappings, primary selected automatically
   - **LOW**: Complex cases needing manual review

## Next Steps

1. ✓ **Generated Files**: Created one-to-one mapping and duplicate resolution files
2. **Review Duplicates**: Examine `azure_duplicate_mappings_resolution.json` for high-count functions
3. **Refine Selection**: Update primary_rule_id where needed based on semantic matching
4. **Validation**: Verify mapping coverage and accuracy
5. **Integration**: Use `azure_recommended_one_to_one_mapping.json` for engine implementation

## Comparison with AWS

| Metric | AWS | Azure |
|--------|-----|-------|
| Total Functions | 716 | 888 |
| Single Mappings | 94 (13.1%) | 527 (59.3%) |
| Duplicate Mappings | 622 (86.9%) | 361 (40.7%) |

**Observation**: Azure has significantly better initial one-to-one mapping ratio than AWS.

## Notes

- Each Azure function now has exactly ONE primary rule_id
- Original multi-mappings preserved in `all_compliance_ids` field
- Engine can implement using the primary rule_id per function
- Reduces duplication and ensures clean function-to-rule coverage

