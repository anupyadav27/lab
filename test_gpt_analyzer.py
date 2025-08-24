#!/usr/bin/env python3
"""
Test script for GPT compliance analyzer - tests with a few compliance checks first
"""

import json
import os
from gpt_compliance_analyzer import GPTComplianceAnalyzer

def test_with_sample_checks():
    """Test the GPT analyzer with just a few compliance checks"""
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("ERROR: Set OPENAI_API_KEY environment variable")
        print("export OPENAI_API_KEY='your-api-key-here'")
        return
    
    # Read the full file
    input_file = "raw_compliance_database/linux/redhat/CIS_RED_HAT_ENTERPRISE_LINUX_6_BENCHMARK_V3.0.0_ARCHIVE (1).json"
    
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Take only first 3 compliance checks for testing
    sample_data = data[:3]
    
    print("GPT-4o Mini RedHat CIS Compliance Analyzer - TEST MODE")
    print("Testing with 3 compliance checks first...")
    print("Temperature: 0 (Maximum Reliability)")
    print()
    
    analyzer = GPTComplianceAnalyzer(api_key)
    
    # Analyze sample data
    for i, item in enumerate(sample_data, 1):
        print(f"Test {i}/3:")
        result = analyzer.analyze_compliance_check(item)
        print(f"Result: {result['final_function_name']} (Confidence: {result['confidence']}%)")
        print("-" * 50)
    
    # Save test results
    test_output = "redhat_gpt_compliance_test.json"
    analyzer.save_results(test_output)
    
    print(f"\nTest complete! Results saved to: {test_output}")
    print("Review the results and run the full analysis if satisfied.")

if __name__ == "__main__":
    test_with_sample_checks()
