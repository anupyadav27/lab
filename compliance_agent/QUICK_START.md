# Quick Start Guide - AI Function Generator (One at a Time)

## 🚀 Setup (One-Time)

```bash
# 1. Install OpenAI library (if not already installed)
pip3 install openai

# 2. Set your OpenAI API key
export OPENAI_API_KEY='your-api-key-here'

# 3. Navigate to directory
cd /Users/apple/Desktop/compliance_Database/compliance_agent
```

---

## 📋 Process One Framework at a Time

### **Step 1: NIST 800-171 (Recommended First)**

```bash
python3 ai_generator_single.py nist
```

**Why first?** 
- Most requirements (50)
- Well-defined checks
- Good test case for AI

**Expected Output:**
```
================================================================================
AI-POWERED GENERATION: NIST 800-171
================================================================================
Input:  nist_800_171/NIST_800-171_R2_controls_with_checks.csv
Output: nist_800_171/NIST_800-171_R2_controls_with_checks_ENHANCED.csv
================================================================================

[1/50] 3_11_2
  🤖 Generating from 3 reference function(s)...
  ✅ Generated 3 GCP + 3 Azure functions

[2/50] 3_11_3
  🤖 Generating from 3 reference function(s)...
  ✅ Generated 3 GCP + 3 Azure functions
...

================================================================================
📊 NIST 800-171 - ENHANCEMENT SUMMARY
================================================================================
Total Requirements:       50
  ├─ Manual:              1 (no functions generated)
  ├─ Automated:           49
  │  ├─ Enhanced:         49 ✅
  │  ├─ Skipped:          0
  │  └─ Errors:           0

✅ Data Consistency: OK
📈 Coverage: 100% of automated requirements enhanced
✅ Output saved: nist_800_171/NIST_800-171_R2_controls_with_checks_ENHANCED.csv
================================================================================
```

**Review Output:**
```bash
# Check the enhanced file
head -20 nist_800_171/NIST_800-171_R2_controls_with_checks_ENHANCED.csv

# Compare with original
diff nist_800_171/NIST_800-171_R2_controls_with_checks.csv \
     nist_800_171/NIST_800-171_R2_controls_with_checks_ENHANCED.csv
```

---

### **Step 2: GDPR (Smallest - Quick Verification)**

```bash
python3 ai_generator_single.py gdpr
```

**Why second?**
- Only 3 requirements
- Quick to verify
- Tests AI on different framework style

**Expected Runtime:** ~1-2 minutes

**Review Output:**
```bash
cat gdpr/GDPR_controls_with_checks_ENHANCED.csv
```

---

### **Step 3: HIPAA (Final)**

```bash
python3 ai_generator_single.py hipaa
```

**Why last?**
- 32 requirements
- Healthcare-specific context
- Final validation before integration

**Expected Runtime:** ~5-7 minutes

---

## 🔍 What to Review After Each Run

### 1. **Check Statistics**
```
✅ Enhanced count matches automated count?
✅ No errors?
✅ Data consistency OK?
```

### 2. **Spot Check Functions**
```bash
# Look at a few requirements
grep "3_13_16" nist_800_171/NIST_800-171_R2_controls_with_checks_ENHANCED.csv
```

**Verify:**
- GCP functions start with `gcp_`
- Azure functions start with `azure_`
- Service names make sense (e.g., `logging` for CloudTrail, `storage` for S3)
- Function counts are reasonable

### 3. **Check Manual Requirements**
```bash
# Find manual requirements
grep "manual" nist_800_171/NIST_800-171_R2_controls_with_checks_ENHANCED.csv
```

**Verify:**
- GCP_Checks column is empty
- Azure_Checks column is empty

---

## ⚠️ If You Need to Re-run

```bash
# The script creates *_ENHANCED.csv files
# Original files are never modified
# To re-run, just run the command again - it will overwrite the _ENHANCED file

python3 ai_generator_single.py nist
```

---

## 🎯 Complete Workflow

```bash
# 1. NIST 800-171
python3 ai_generator_single.py nist
# Review output, verify results

# 2. GDPR  
python3 ai_generator_single.py gdpr
# Review output, verify results

# 3. HIPAA
python3 ai_generator_single.py hipaa
# Review output, verify results

# 4. All done! 
echo "✅ All frameworks enhanced!"
```

---

## 📊 Expected Totals

| Framework | Total Req | Manual | Automated | Functions Generated |
|-----------|-----------|--------|-----------|---------------------|
| NIST 800-171 | 50 | ~1 | ~49 | ~800-1000 |
| GDPR | 3 | 0 | 3 | ~50-100 |
| HIPAA | 32 | 0 | 32 | ~600-800 |
| **TOTAL** | **85** | **~1** | **~84** | **~1,450-1,900** |

---

## 🐛 Troubleshooting

### Error: "OPENAI_API_KEY not set"
```bash
export OPENAI_API_KEY='your-key'
```

### Error: "No module named 'openai'"
```bash
pip3 install openai
```

### Slow Performance
- Normal! AI generation takes time
- Each requirement: 5-10 seconds
- 50 requirements: ~5-8 minutes

### Want to Test First?
```bash
# Test with GDPR (only 3 requirements)
python3 ai_generator_single.py gdpr
```

---

## 💰 Cost Estimate

**Per Framework:**
- NIST: ~$1-2
- GDPR: ~$0.10-0.20
- HIPAA: ~$0.80-1.50

**Total: ~$2-4** for all three

---

## ✅ Success Checklist

After each framework:
- [ ] Script completed without errors
- [ ] Enhanced CSV file created
- [ ] Total_Checks column updated
- [ ] GCP_Checks populated (for automated)
- [ ] Azure_Checks populated (for automated)
- [ ] Manual requirements have empty GCP/Azure
- [ ] Function names follow `<csp>_<service>_<check>` format

---

## 🎉 You're Ready!

Start with NIST:
```bash
python3 ai_generator_single.py nist
```

