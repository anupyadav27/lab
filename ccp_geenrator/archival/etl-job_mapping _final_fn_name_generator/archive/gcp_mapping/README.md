# GCP Compliance Function Mapping Tool

This tool maps existing security functions from `gcp_simplified_function_names.json` to CIS GCP compliance frameworks and suggests new functions where gaps exist, following the same high-quality standards as Azure and Kubernetes mappers.

## Features

- **High-Quality Function Mapping**: Uses advanced AI prompts to accurately map existing functions to compliance requirements
- **Gap Analysis**: Identifies where new functions are needed to achieve complete compliance coverage
- **Function Optimization**: Suggests renames and consolidations for better clarity and efficiency
- **Comprehensive Coverage**: Ensures all compliance items have appropriate function coverage
- **Quality Validation**: Validates all generated functions for format and implementation feasibility

## Prerequisites

- Python 3.8+
- OpenAI API key
- GCP compliance framework file (CIS benchmark)
- GCP functions database file

## Installation

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set OpenAI API key**:
   - Edit `gcp_compliance_mapper.py`
   - Replace `"YOUR_OPENAI_API_KEY_HERE"` with your actual API key
   - Look for the line: `self.api_key = "YOUR_OPENAI_API_KEY_HERE"`

## Usage

### Basic Usage

```bash
# Map all compliance items
python gcp_compliance_mapper.py gcp_simplified_function_names.json CIS_GOOGLE_CLOUD_PLATFORM_FOUNDATION_BENCHMARK_V4.0.0.json

# Test with limited items (recommended for first run)
python gcp_compliance_mapper.py gcp_simplified_function_names.json CIS_GOOGLE_CLOUD_PLATFORM_FOUNDATION_BENCHMARK_V4.0.0.json 15
```

### Test Mode

```bash
# Run the test suite with 15 compliance items
python test_gcp_mapper.py
```

## Input Files

### 1. GCP Functions Database (`gcp_simplified_function_names.json`)
- Contains existing GCP security function names
- Should be a list of function names or structured data

### 2. Compliance Framework (`CIS_GOOGLE_CLOUD_PLATFORM_FOUNDATION_BENCHMARK_V4.0.0.json`)
- CIS GCP compliance benchmark
- Contains compliance items with IDs, titles, descriptions, and assessment types

## Output

The tool generates several output files in the `output/` directory:

### 1. Mapping Results (`updated_compliance/gcp_mapping_results_TIMESTAMP.json`)
- Complete mapping results for all compliance items
- Shows existing functions mapped, coverage assessment, and new functions needed

### 2. New Functions (`new_functions/gcp_new_functions_TIMESTAMP.json`)
- Suggested new functions to fill compliance gaps
- Includes function names, descriptions, GCP API examples, and service categories

### 3. Function Updates (`updated_functions/gcp_rename_functions_TIMESTAMP.json`)
- Suggestions for renaming existing functions for better clarity
- Includes rationale for each rename

### 4. Summary Report (`gcp_mapping_summary_TIMESTAMP.json`)
- High-level statistics and coverage metrics
- Total items processed, coverage breakdown, and function counts

## Mapping Strategy

The tool follows a strict 5-step mapping strategy:

1. **Existing Function Mapping**: Map existing functions that can cover compliance requirements
2. **Function Consolidation**: Consolidate similar functions to minimize duplication
3. **Naming Standards**: Enforce strict naming conventions (`<service><resource><requirement>[_<qualifier>]`)
4. **Consolidation Rules**: Ensure similar functions are consolidated into one
5. **Coverage Assessment**: Evaluate final coverage (complete/partial/none)

## Function Naming Standards

- **Format**: `<service><resource><requirement>[_<qualifier>]`
- **Examples**:
  - ✅ `iam_user_mfa_enabled`
  - ✅ `compute_instance_public_access_blocked`
  - ✅ `storage_bucket_public_access_restricted`
  - ❌ `gcp_compute_instance_public_access_blocked` (redundant 'gcp')

## Quality Requirements

- Function names MUST be in snake_case format
- Functions MUST be implementable with real GCP APIs (gcloud, REST API)
- Service field MUST match GCP service names (iam, compute, storage, kms, etc.)
- Be specific and conservative in suggestions
- NO over-engineering or unnecessary complexity

## Testing

The mapper has built-in testing capabilities. You can test with a subset before running the full compliance framework:

```bash
# Test mode with 15 items (recommended for first run)
python gcp_compliance_mapper.py gcp_simplified_function_names.json CIS_GOOGLE_CLOUD_PLATFORM_FOUNDATION_BENCHMARK_V4.0.0.json --test 15

# Or use the simple test runner
python test_gcp_mapper.py

# Production mode - all items
python gcp_compliance_mapper.py gcp_simplified_function_names.json CIS_GOOGLE_CLOUD_PLATFORM_FOUNDATION_BENCHMARK_V4.0.0.json
```

## Troubleshooting

### Common Issues

1. **OpenAI API Key Error**:
   - Ensure you've set your API key in the script
   - Check API key validity and quota

2. **File Not Found Errors**:
   - Verify file paths are correct
   - Ensure you're running from the right directory

3. **JSON Parsing Errors**:
   - Check input file formats
   - Ensure files are valid JSON

4. **Rate Limiting**:
   - The tool includes built-in rate limiting
   - Increase delays if you encounter 429 errors

### Logs

Check `gcp_compliance_mapping.log` for detailed execution logs and error information.

## Next Steps

After successful testing:

1. **Review Results**: Examine the generated mappings and function suggestions
2. **Validate Functions**: Ensure suggested functions are implementable
3. **Full Run**: Run on the complete compliance framework
4. **Integration**: Integrate results into your compliance management system

## Support

For issues or questions:
1. Check the logs for error details
2. Verify input file formats
3. Ensure OpenAI API key is valid
4. Test with a smaller subset first
