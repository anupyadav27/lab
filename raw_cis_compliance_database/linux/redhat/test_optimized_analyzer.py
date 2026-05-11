#!/usr/bin/env python3
"""
Test script for optimized GPT compliance analyzer
Tests with a small sample to verify functionality before full run
"""

import json
import os
from pathlib import Path
from gpt_compliance_analyzer import OptimizedGPTComplianceAnalyzer

def test_optimized_analyzer():
    """Test the optimized analyzer with a small sample"""
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("ERROR: Set OPENAI_API_KEY environment variable")
        print("export OPENAI_API_KEY='your-api-key-here'")
        return
    
    print("🧪 Testing Optimized GPT-4o Mini RedHat CIS Compliance Analyzer")
    print("=" * 60)
    
    # Find a compliance file to test with
    json_files = list(Path(".").glob("*.json"))
    if not json_files:
        print("No JSON files found for testing")
        return
    
    test_file = json_files[0]  # Use first file for testing
    print(f"Testing with: {test_file.name}")
    
    # Read the file and take only first 10 checks for testing
    with open(test_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Create a test file with only first 10 checks
    test_data = data[:10]
    test_filename = "TEST_SAMPLE.json"
    
    with open(test_filename, 'w', encoding='utf-8') as f:
        json.dump(test_data, f, indent=2)
    
    print(f"Created test file with {len(test_data)} compliance checks")
    
    # Create analyzer with smaller batch size for testing
    analyzer = OptimizedGPTComplianceAnalyzer(api_key)
    analyzer.batch_size = 3  # Smaller batches for testing
    analyzer.output_dir = Path("test_output")
    analyzer.output_dir.mkdir(exist_ok=True)
    
    print(f"Testing with batch size: {analyzer.batch_size}")
    print("Starting test analysis...")
    print("-" * 60)
    
    # Analyze the test file
    results = analyzer.analyze_compliance_file(Path(test_filename))
    
    if results:
        # Save test results
        output_filename = "TEST_SAMPLE_GPT_ANALYZED.json"
        output_path = analyzer.output_dir / output_filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results['output_data'], f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Test completed successfully!")
        print(f"📁 Test results saved to: {output_path}")
        print(f"📊 Test summary:")
        print(f"   - Total checks: {results['total_checks']}")
        print(f"   - Analyzed: {results['analyzed_checks']}")
        print(f"   - Cache hits: {len(analyzer.cache)}")
        
        # Show sample results
        print(f"\n📋 Sample results:")
        for i, item in enumerate(results['output_data'][:3]):
            print(f"   {i+1}. {item.get('id', 'Unknown')}: {item.get('function_names', ['None'])[0]}")
        
        print(f"\n🧹 Cleaning up test files...")
        os.remove(test_filename)
        
        print(f"\n🎯 Test successful! You can now run the full analysis.")
        print(f"💡 Estimated cost savings: ~80% reduction in API calls with batching")
        
    else:
        print("❌ Test failed!")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    test_optimized_analyzer()
