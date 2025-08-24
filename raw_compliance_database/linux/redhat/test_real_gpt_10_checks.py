#!/usr/bin/env python3
"""
Real GPT-4o Mini Analysis of 10 RedHat CIS Compliance Checks
This script uses the actual OpenAI API to analyze compliance checks
"""

import json
import openai
import os
from pathlib import Path

def analyze_10_compliance_checks():
    """Analyze exactly 10 compliance checks using GPT-4o Mini"""
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("ERROR: OpenAI API key not set")
        return
    
    print("🚀 Real GPT-4o Mini Analysis of 10 RedHat CIS Compliance Checks")
    print("=" * 70)
    print("Using actual OpenAI API for real analysis")
    print("Focus: Professional function names without unnecessary prefixes")
    print()
    
    # Initialize OpenAI client
    client = openai.OpenAI(api_key=api_key)
    
    # Find a compliance file to work with
    json_files = list(Path(".").glob("*.json"))
    if not json_files:
        print("No JSON files found")
        return
    
    # Use the RHEL 6 file for analysis
    analysis_file = None
    for file in json_files:
        if "RHEL_6" in file.name and "ARCHIVE" in file.name:
            analysis_file = file
            break
    
    if not analysis_file:
        analysis_file = json_files[0]
    
    print(f"📁 Analyzing file: {analysis_file.name}")
    
    # Read the file and take first 10 compliance checks
    with open(analysis_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    compliance_checks = data[:10]
    print(f"📊 Selected {len(compliance_checks)} compliance checks for analysis")
    print()
    
    # Show what we're analyzing
    print("🔍 COMPLIANCE CHECKS TO BE ANALYZED:")
    print("-" * 60)
    for i, item in enumerate(compliance_checks, 1):
        print(f"{i:2d}. {item.get('id', 'Unknown')}: {item.get('title', 'No title')[:70]}...")
    print()
    
    # Analyze each compliance check individually for maximum quality
    results = []
    
    for i, check in enumerate(compliance_checks, 1):
        print(f"🤖 Analyzing {i}/10: {check.get('id', 'Unknown')}")
        
        # Create enhanced prompt for better function names and confidence
        prompt = f"""
You are a cybersecurity compliance expert specializing in RedHat Enterprise Linux. Analyze this compliance check and provide the optimal function name.

COMPLIANCE CHECK:
- ID: {check.get('id', 'Unknown')}
- Title: {check.get('title', 'No title')}
- Description: {check.get('description', '')[:300]}...
- Audit Command: {check.get('audit', '')[:200]}...
- Existing Functions: {check.get('function_names', [])}

REQUIREMENTS:
1. Generate a PROFESSIONAL function name WITHOUT "check_" prefix
2. Use descriptive, action-oriented naming (e.g., "verify_", "ensure_", "validate_", "audit_")
3. Be specific about what is being verified
4. Follow consistent naming conventions
5. Consider if this requires manual verification

FUNCTION NAMING EXAMPLES:
- Good: "verify_kernel_module_disabled", "ensure_tmp_partition_separate", "audit_file_permissions"
- Avoid: "check_something", "test_function", generic names

CONFIDENCE SCORING:
- 95-100%: Clear, unambiguous compliance requirement with standard verification
- 85-94%: Clear requirement but some complexity in verification
- 75-84%: Moderate complexity or multiple verification steps
- 60-74%: Complex requirement or potential manual verification needed
- <60%: Requires manual review or unclear requirements

OUTPUT FORMAT (JSON only):
{{
    "function_name": "string - professional function name without 'check_' prefix",
    "confidence": "number 1-100",
    "reasoning": "string explaining the confidence level and naming choice",
    "compliance_type": "string describing the type of check",
    "verification_method": "automated|semi_automated|manual",
    "complexity": "simple|moderate|complex"
}}

Provide ONLY the JSON response.
"""
        
        try:
            # Get GPT analysis
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a cybersecurity compliance expert. Provide only JSON responses with professional function names."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0,  # Maximum reliability
                max_tokens=400
            )
            
            gpt_response = response.choices[0].message.content.strip()
            
            # Clean response
            if gpt_response.startswith('```json'):
                gpt_response = gpt_response[7:]
            if gpt_response.endswith('```'):
                gpt_response = gpt_response[:-3]
            
            # Parse JSON response
            analysis = json.loads(gpt_response)
            
            # Create result
            result = {
                'compliance_id': check.get('id'),
                'title': check.get('title'),
                'gpt_analysis': analysis,
                'final_function_name': analysis['function_name'],
                'confidence': analysis['confidence'],
                'verification_method': analysis.get('verification_method', 'automated'),
                'complexity': analysis.get('complexity', 'simple')
            }
            
            results.append(result)
            
            # Display result with verification method
            confidence_emoji = "🟢" if analysis['confidence'] >= 90 else "🟡" if analysis['confidence'] >= 75 else "🔴"
            method_emoji = "🤖" if analysis['verification_method'] == 'automated' else "🔄" if analysis['verification_method'] == 'semi_automated' else "👤"
            
            print(f"   {confidence_emoji} {analysis['function_name']} (Confidence: {analysis['confidence']}%)")
            print(f"   {method_emoji} {analysis['verification_method'].upper()} | {analysis['compliance_type']}")
            print(f"   📊 Complexity: {analysis['complexity']}")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            # Create fallback result
            fallback = {
                'compliance_id': check.get('id'),
                'title': check.get('title'),
                'gpt_analysis': {
                    'function_name': 'manual_review_required',
                    'confidence': 50,
                    'reasoning': 'Analysis failed - requires manual review',
                    'compliance_type': 'manual_review',
                    'verification_method': 'manual',
                    'complexity': 'complex'
                },
                'final_function_name': 'manual_review_required',
                'confidence': 50,
                'verification_method': 'manual',
                'complexity': 'complex'
            }
            results.append(fallback)
        
        print()
    
    # Create enhanced output
    enhanced_output = []
    for i, check in enumerate(compliance_checks):
        if i < len(results):
            result = results[i]
            output_item = check.copy()
            output_item['function_names'] = [result['final_function_name']]
            output_item['gpt_analysis'] = result['gpt_analysis']
            enhanced_output.append(output_item)
        else:
            # Fallback for any missing results
            output_item = check.copy()
            output_item['function_names'] = ['manual_review_required']
            output_item['gpt_analysis'] = {
                'function_name': 'manual_review_required',
                'confidence': 50,
                'reasoning': 'Missing analysis result - requires manual review',
                'compliance_type': 'manual_review',
                'verification_method': 'manual',
                'complexity': 'complex'
            }
            enhanced_output.append(output_item)
    
    # Save results
    output_file = "REAL_GPT_ANALYSIS_10_CHECKS_IMPROVED.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(enhanced_output, f, indent=2, ensure_ascii=False)
    
    # Generate detailed summary
    print("📊 DETAILED ANALYSIS SUMMARY:")
    print("-" * 60)
    print(f"Total checks analyzed: {len(results)}")
    print(f"🟢 High confidence (90-100%): {sum(1 for r in results if r['confidence'] >= 90)}")
    print(f"🟡 Medium confidence (75-89%): {sum(1 for r in results if 75 <= r['confidence'] < 90)}")
    print(f"🔴 Low confidence (<75%): {sum(1 for r in results if r['confidence'] < 75)}")
    print()
    
    # Verification method breakdown
    automated = sum(1 for r in results if r['verification_method'] == 'automated')
    semi_automated = sum(1 for r in results if r['verification_method'] == 'semi_automated')
    manual = sum(1 for r in results if r['verification_method'] == 'manual')
    
    print("🔍 VERIFICATION METHOD BREAKDOWN:")
    print("-" * 60)
    print(f"🤖 Automated: {automated}")
    print(f"🔄 Semi-automated: {semi_automated}")
    print(f"👤 Manual review required: {manual}")
    print()
    
    # Show top recommendations
    print("🏆 TOP RECOMMENDATIONS (High Confidence):")
    print("-" * 60)
    high_confidence_results = [r for r in results if r['confidence'] >= 90]
    for i, result in enumerate(high_confidence_results[:5], 1):
        method_emoji = "🤖" if result['verification_method'] == 'automated' else "🔄" if result['verification_method'] == 'semi_automated' else "👤"
        print(f"{i}. {result['compliance_id']}: {result['final_function_name']}")
        print(f"   {method_emoji} {result['verification_method'].upper()} | Confidence: {result['confidence']}%")
        print()
    
    # Show manual review items
    manual_items = [r for r in results if r['verification_method'] == 'manual']
    if manual_items:
        print("⚠️  MANUAL REVIEW REQUIRED:")
        print("-" * 60)
        for item in manual_items:
            print(f"• {item['compliance_id']}: {item['final_function_name']}")
            print(f"  Reason: {item['gpt_analysis']['reasoning']}")
        print()
    
    print(f"💾 Full results saved to: {output_file}")
    print("🎯 Improved GPT analysis complete!")
    print()
    print("💡 IMPROVEMENTS MADE:")
    print("• Removed unnecessary 'check_' prefixes")
    print("• Enhanced confidence scoring methodology")
    print("• Added verification method classification")
    print("• Identified manual review requirements")
    print("• More professional function naming")

if __name__ == "__main__":
    analyze_10_compliance_checks()
