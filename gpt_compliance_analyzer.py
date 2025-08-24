#!/usr/bin/env python3
"""
GPT-4o Mini Powered RedHat CIS Compliance Function Analyzer
"""

import json
import openai
import time
import os

class GPTComplianceAnalyzer:
    def __init__(self, api_key: str):
        self.client = openai.OpenAI(api_key=api_key)
        self.model = "gpt-4o-mini"
        self.temperature = 0  # Maximum reliability
        self.analysis_results = []
        
    def analyze_compliance_check(self, compliance_item: Dict) -> Dict:
        compliance_id = compliance_item.get('id', 'Unknown')
        title = compliance_item.get('title', 'No title')
        description = compliance_item.get('description', '')
        audit = compliance_item.get('audit', '')
        existing_functions = compliance_item.get('function_names', [])
        
        print(f"\nAnalyzing: {compliance_id} - {title}")
        
        prompt = f"""
You are a cybersecurity compliance expert. Analyze this RedHat CIS compliance check and provide the optimal function name.

COMPLIANCE CHECK:
- ID: {compliance_id}
- Title: {title}
- Description: {description}
- Audit Command: {audit}
- Existing Functions: {existing_functions}

Generate the BEST SINGLE function name that will:
- Clearly indicate what is being checked
- Follow consistent naming conventions
- Be specific enough for implementation
- Be generic enough for reuse

OUTPUT FORMAT (JSON only):
{{
    "analysis": {{
        "compliance_type": "string describing the type of check",
        "check_target": "string describing what is being checked",
        "expected_state": "string describing the expected result"
    }},
    "function_name": {{
        "recommended": "string - the best function name",
        "confidence": "number 1-100",
        "reasoning": "string explaining why this name is best"
    }},
    "implementation_notes": "string with key implementation details"
}}

Provide ONLY the JSON response.
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a cybersecurity compliance expert. Provide only JSON responses."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=500
            )
            
            gpt_response = response.choices[0].message.content.strip()
            gpt_analysis = json.loads(gpt_response)
            
            result = {
                'compliance_id': compliance_id,
                'title': title,
                'gpt_analysis': gpt_analysis,
                'final_function_name': gpt_analysis['function_name']['recommended'],
                'confidence': gpt_analysis['function_name']['confidence']
            }
            
            self.analysis_results.append(result)
            print(f"Recommended: {result['final_function_name']} (Confidence: {result['confidence']}%)")
            
            return result
            
        except Exception as e:
            print(f"Error analyzing {compliance_id}: {e}")
            fallback = {
                'compliance_id': compliance_id,
                'title': title,
                'final_function_name': 'check_compliance_fallback',
                'confidence': 50
            }
            self.analysis_results.append(fallback)
            return fallback
    
    def analyze_file(self, input_file: str):
        print(f"Reading: {input_file}")
        
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"Found {len(data)} compliance checks")
        
        for i, item in enumerate(data, 1):
            print(f"Progress: {i}/{len(data)}")
            self.analyze_compliance_check(item)
            time.sleep(1)  # Rate limiting
    
    def save_results(self, output_file: str):
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.analysis_results, f, indent=2)
        print(f"Results saved to: {output_file}")

def main():
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("ERROR: Set OPENAI_API_KEY environment variable")
        return
    
    input_file = "raw_compliance_database/linux/redhat/CIS_RED_HAT_ENTERPRISE_LINUX_6_BENCHMARK_V3.0.0_ARCHIVE (1).json"
    
    print("GPT-4o Mini RedHat CIS Compliance Analyzer")
    print("Temperature: 0 (Maximum Reliability)")
    
    analyzer = GPTComplianceAnalyzer(api_key)
    analyzer.analyze_file(input_file)
    
    output_file = "redhat_gpt_compliance_analysis.json"
    analyzer.save_results(output_file)
    
    print(f"Analysis complete! Results saved to: {output_file}")

if __name__ == "__main__":
    main()
