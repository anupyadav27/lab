# Archive Folder

This folder contains archived files from the AWS rule generator cleanup on 2025-09-11T06-05-35.

## Folder Structure
```
archive/
├── matrices/          # Archived matrix files
├── out/              # Archived rule files  
├── schemas/          # Archived schema files
├── scripts/          # Archived script files
├── reports/          # Archived report files
└── README.md         # This file
```

## Current Active Files

### Core Files
- `package.json` - Node.js dependencies
- `package-lock.json` - Dependency lock file
- `tsconfig.json` - TypeScript configuration
- `README.md` - Project documentation
- `assertions_pack_2025-01-09.json` - Assertions data

### Matrices
- `matrices/aws_matrix_v2_complete_fixed_v4_2025-09-11T05-50-34.json` (current)

### Out
- `out/aws_rules_exhaustive_v2.json` (current - 832 rules, 117 services)

### Schemas
- `schemas/assertions.schema.ts` - Assertions validation schema
- `schemas/matrix.schema.ts` - Matrix validation schema
- `schemas/profile.schema.ts` - Profile validation schema
- `schemas/rules.schema.ts` - Rules validation schema

### Scripts
- `scripts/generate-rules-v2.ts` - Main rule generator
- `scripts/validate-rules-v2.ts` - Main validator
- `scripts/cleanup-files.ts` - File cleanup utility
- `scripts/cleanup-all-folders.ts` - Complete cleanup utility
- `scripts/cleanup-main-folder.ts` - Main folder cleanup utility

## Cleanup Summary
- Matrices archived: 7 files
- Matrices kept: 1 file
- Out files archived: 15 files
- Out files kept: 1 file
- Schemas archived: 0 files
- Schemas kept: 4 files
- Scripts archived: 18 files
- Scripts kept: 5 files
- Reports archived: 11 files
- Files deleted: 1 files
- Core files kept: 5 files

## Archived Reports Description
- `CHATGPT_FIXES_REPORT.md` - Report of ChatGPT feedback fixes
- `coverage_analysis.json` - Coverage analysis results
- `coverage_diff_report_v3_*.json` - Coverage diff reports
- `coverage_report_v2.json` - Coverage report v2
- `current_services.txt` - List of current services
- `dry_run_report_*.json` - Dry run test results
- `missing_services.txt` - List of missing services
- `schema_lint_report_v3_*.json` - Schema validation reports
- `validation_report_v2.json` - Rule validation report

All archived files are preserved and can be restored if needed.
