# CIS AWS Foundations Benchmark - Section Hierarchy (Final)

**Date**: February 14, 2026
**Status**: ✅ Complete - Proper parent-child relationships established
**Versions**: v4.0.1, v5.0.0

---

## ✅ PROPER HIERARCHICAL STRUCTURE

The CIS benchmark now has a **clear parent-child section hierarchy** that shows the relationship between main categories and subcategories.

---

## 📊 COMPLETE SECTION HIERARCHY

### CIS AWS Foundations Benchmark v4.0.1 (61 controls)

```
Section 1: Identity and Access Management (19 controls)
  └─ Direct controls: 1.2, 1.3, 1.4, 1.5, ... (19 total)

Section 2: Storage (9 controls)
  ├─ Section 2.1: Simple Storage Service (S3) (4 controls)
  ├─ Section 2.2: Relational Database Service (RDS) (4 controls)
  └─ Section 2.3: Elastic File System (EFS) (1 control)

Section 3: Logging (9 controls)
  └─ Direct controls: 3.1, 3.2, 3.3, 3.4, ... (9 total)

Section 4: Monitoring (16 controls)
  └─ Direct controls: 4.1, 4.2, 4.3, 4.4, ... (16 total)

Section 5: Networking (8 controls)
  ├─ Direct controls: 5.2, 5.3, 5.4, 5.5, 5.6, 5.7 (6 total)
  └─ Section 5.1: Elastic Compute Cloud (EC2) (2 controls)
```

---

## 🔍 KEY INSIGHTS

### Parent-Only Sections
**Section 2 (Storage)** has NO direct controls - only subsections:
- All 9 controls are under 2.1 (S3), 2.2 (RDS), or 2.3 (EFS)
- This is a **parent-only category** for organizing storage services

### Mixed Sections
**Section 5 (Networking)** has BOTH:
- Direct controls (5.2 - 5.7) at the networking level
- Subsection 5.1 for EC2-specific networking controls

### Direct-Only Sections
**Sections 1, 3, 4** have only direct controls (no subsections)

---

## 📋 NEW FIELDS ADDED

Each control now has these hierarchy fields:

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| **section_number** | string | Section/subsection number | `"1"`, `"2.1"`, `"5.1"` |
| **section_title** | string | Section title | `"Simple Storage Service (S3)"` |
| **section_level** | integer | Hierarchy level (1 or 2) | `1` (parent), `2` (child) |
| **section_path** | string | Full hierarchical path | `"Storage > Simple Storage Service (S3)"` |
| **parent_section_number** | string | Parent section (level 2 only) | `"2"`, `"5"` |
| **parent_section_title** | string | Parent title (level 2 only) | `"Storage"`, `"Networking"` |

---

## 📄 EXAMPLE: Level 1 (Parent Section)

**Control 1.2** - Identity and Access Management

```json
{
  "id": "1.2",
  "title": "Ensure security contact information is registered",
  "section_number": "1",
  "section_title": "Identity and Access Management",
  "section_level": 1,
  "section_path": "Identity and Access Management"
}
```

**Note**: No `parent_section_number` or `parent_section_title` (this IS the parent)

---

## 📄 EXAMPLE: Level 2 (Child Section)

**Control 2.1.1** - S3 under Storage

```json
{
  "id": "2.1.1",
  "title": "Ensure S3 Bucket Policy is set to deny HTTP requests",
  "section_number": "2.1",
  "section_title": "Simple Storage Service (S3)",
  "section_level": 2,
  "section_path": "Storage > Simple Storage Service (S3)",
  "parent_section_number": "2",
  "parent_section_title": "Storage"
}
```

**Note**: Has `parent_section_number` and `parent_section_title` showing relationship to Section 2

---

## 🎯 USE CASES

### 1. Query All Storage Controls (Including Subsections)

```python
import json

with open('CIS_Amazon_Web_Services_Foundations_Benchmark_v4.0.1.json') as f:
    data = json.load(f)

# Get all Storage controls (section 2 + subsections 2.1, 2.2, 2.3)
storage_controls = [
    c for c in data
    if c.get('section_number', '').startswith('2')
    or c.get('parent_section_number') == '2'
]

print(f"Total Storage controls: {len(storage_controls)}")
# Output: Total Storage controls: 9
```

### 2. Query S3-Specific Controls Only

```python
# Get only S3 controls (section 2.1)
s3_controls = [
    c for c in data
    if c.get('section_number') == '2.1'
]

print(f"S3-specific controls: {len(s3_controls)}")
# Output: S3-specific controls: 4
```

### 3. Build Hierarchical Navigation

```python
from collections import defaultdict

# Build hierarchy for navigation
hierarchy = defaultdict(lambda: {'title': '', 'controls': [], 'children': {}})

for control in data:
    section_num = control.get('section_number')
    section_level = control.get('section_level')
    parent_num = control.get('parent_section_number')

    if section_level == 1:
        # Top-level section
        if section_num not in hierarchy:
            hierarchy[section_num]['title'] = control['section_title']
        hierarchy[section_num]['controls'].append(control)

    elif section_level == 2 and parent_num:
        # Child section
        if parent_num not in hierarchy:
            hierarchy[parent_num]['title'] = control['parent_section_title']

        if section_num not in hierarchy[parent_num]['children']:
            hierarchy[parent_num]['children'][section_num] = {
                'title': control['section_title'],
                'controls': []
            }

        hierarchy[parent_num]['children'][section_num]['controls'].append(control)

# Display navigation
for section_num in sorted(hierarchy.keys(), key=lambda x: int(x)):
    section = hierarchy[section_num]
    print(f"Section {section_num}: {section['title']}")
    print(f"  Direct controls: {len(section['controls'])}")

    for child_num, child in sorted(section['children'].items()):
        print(f"  └─ Section {child_num}: {child['title']} ({len(child['controls'])} controls)")
```

**Output**:
```
Section 1: Identity and Access Management
  Direct controls: 19
Section 2: Storage
  Direct controls: 0
  └─ Section 2.1: Simple Storage Service (S3) (4 controls)
  └─ Section 2.2: Relational Database Service (RDS) (4 controls)
  └─ Section 2.3: Elastic File System (EFS) (1 controls)
Section 3: Logging
  Direct controls: 9
Section 4: Monitoring
  Direct controls: 16
Section 5: Networking
  Direct controls: 6
  └─ Section 5.1: Elastic Compute Cloud (EC2) (2 controls)
```

### 4. Generate Breadcrumb Navigation

```python
def get_breadcrumb(control):
    """Generate breadcrumb for a control."""
    if control.get('section_level') == 1:
        return control['section_title']
    else:
        parent = control.get('parent_section_title', '')
        current = control.get('section_title', '')
        return f"{parent} > {current}"

# Example
control = next(c for c in data if c['id'] == '2.1.1')
print(get_breadcrumb(control))
# Output: "Storage > Simple Storage Service (S3)"
```

---

## 📊 SECTION BREAKDOWN

### Level 1 Sections (Parents)

| Section | Title | Direct Controls | Subsections | Total Controls |
|---------|-------|----------------|-------------|----------------|
| 1 | Identity and Access Management | 19 | 0 | 19 |
| 2 | Storage | 0 | 3 (2.1, 2.2, 2.3) | 9 |
| 3 | Logging | 9 | 0 | 9 |
| 4 | Monitoring | 16 | 0 | 16 |
| 5 | Networking | 6 | 1 (5.1) | 8 |

### Level 2 Sections (Children)

| Section | Title | Parent | Controls |
|---------|-------|--------|----------|
| 2.1 | Simple Storage Service (S3) | Storage (2) | 4 |
| 2.2 | Relational Database Service (RDS) | Storage (2) | 4 |
| 2.3 | Elastic File System (EFS) | Storage (2) | 1 |
| 5.1 | Elastic Compute Cloud (EC2) | Networking (5) | 2 |

---

## 🔗 MAPPING TO CSPM CATALOG

You can now easily map CIS sections to your CSPM catalog categories:

| CIS Section | CSPM Category |
|------------|---------------|
| 1 - Identity and Access Management | `identity_access` |
| 2 - Storage (parent) | `data_protection_storage` |
| 2.1 - S3 | `data_protection_storage` |
| 2.2 - RDS | `db` |
| 2.3 - EFS | `data_protection_storage` |
| 3 - Logging | `logging_audit` |
| 4 - Monitoring | `security_monitoring` |
| 5 - Networking | `network_security` |
| 5.1 - EC2 | `compute_host_security` |

---

## 📁 FILES UPDATED

### Main Files
1. ✅ `CIS_Amazon_Web_Services_Foundations_Benchmark_v4.0.1.json` (61 controls)
2. ✅ `CIS_Amazon_Web_Services_Foundations_Benchmark_v5.0.0.json` (60 controls)

### Backups
3. ✅ `CIS_Amazon_Web_Services_Foundations_Benchmark_v4.0.1_before_reorganize.json`
4. ✅ `CIS_Amazon_Web_Services_Foundations_Benchmark_v5.0.0_before_reorganize.json`
5. ✅ `CIS_Amazon_Web_Services_Foundations_Benchmark_v4.0.1.json.backup` (original)
6. ✅ `CIS_Amazon_Web_Services_Foundations_Benchmark_v5.0.0.json.backup` (original)

### Scripts
7. ✅ `reorganize_sections.py` - Script to reorganize hierarchy
8. ✅ `add_section_titles.py` - Initial section title addition

### Documentation
9. ✅ `SECTION_HIERARCHY_FINAL.md` - This document
10. ✅ `SECTION_TITLES_ADDED.md` - Initial documentation

---

## ✅ VALIDATION

### Hierarchy Correctness ✅
- ✅ Section 2 properly shows as parent of 2.1, 2.2, 2.3
- ✅ Section 5 properly shows as parent of 5.1
- ✅ All child sections have `parent_section_number` and `parent_section_title`
- ✅ All parent sections (level 1) do NOT have parent fields
- ✅ `section_path` shows full breadcrumb (e.g., "Storage > S3")

### Data Completeness ✅
- ✅ All 61 controls (v4.0.1) have hierarchy fields
- ✅ All 60 controls (v5.0.0) have hierarchy fields
- ✅ No missing or null values
- ✅ Proper parent-child relationships

---

## 🎉 SUMMARY

**Status**: ✅ **Complete**

**What was accomplished**:
1. ✅ Added section hierarchy to CIS JSON files
2. ✅ Established proper parent-child relationships
3. ✅ Added navigation breadcrumbs (`section_path`)
4. ✅ Made structure queryable and filterable
5. ✅ Ready for integration with CSPM catalog

**Key improvements**:
- Clear section organization (parent → child)
- Easy to query by category or service
- Breadcrumb navigation for UI
- Ready for compliance mapping

🎯 **CIS benchmarks now have full hierarchical section structure with proper parent-child relationships!**
