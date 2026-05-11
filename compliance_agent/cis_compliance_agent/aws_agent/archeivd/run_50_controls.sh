#!/bin/bash

echo "╔════════════════════════════════════════════════════════════════════════════════╗"
echo "║               🚀 AWS FULL PIPELINE - 50 CONTROLS FOR REVIEW                   ║"
echo "╚════════════════════════════════════════════════════════════════════════════════╝"
echo ""

STEP1_DIR="output_step1_20251027_213132"

# Step 2: Review
echo "📍 STEP 2: Review & Validation (GPT-4o)"
python agent_step2_review.py --input-dir $STEP1_DIR --output-dir output_step2_review
STEP2_DIR="output_step2_review"

# Step 3: Final Decision
echo ""
echo "📍 STEP 3: Final Decision (GPT-4o)"
python agent_step3_final.py --input-dir $STEP2_DIR --output-dir output_step3_final
STEP3_DIR="output_step3_final"

# Step 4: CSV Generation
echo ""
echo "📍 STEP 4: CSV Generation"
python agent_step4_csv.py --input-dir $STEP3_DIR --original-csv aws_controls.csv --output-dir output_final_50

# Quality Check
echo ""
echo "📍 QUALITY CHECK"
python quality_check.py --input-dir $STEP3_DIR --output-file quality_report_50.md

echo ""
echo "╔════════════════════════════════════════════════════════════════════════════════╗"
echo "║                              ✅ ALL STEPS COMPLETE!                            ║"
echo "╚════════════════════════════════════════════════════════════════════════════════╝"
echo ""
echo "📊 Results:"
echo "   - Final CSV: output_final_50/"
echo "   - Quality Report: quality_report_50.md"
echo ""
