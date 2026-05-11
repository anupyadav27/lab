#!/usr/bin/env python3
"""
Optimized GPT-4o Mini Powered RedHat CIS Compliance Function Analyzer
- Processes all CIS compliance JSON files in RedHat folder
- Cost-optimized with batch processing and caching
- Creates organized output structure
- Maintains high quality output
"""

import json
import openai
import time
import os
import glob
from pathlib import Path
from typing import Dict, List, Set
import hashlib

class OptimizedGPTComplianceAnalyzer:
    def __init__(self, api_key: str):
        self.client = openai.OpenAI(api_key=api_key)
        self.model = "gpt-4o-mini"
        self.temperature = 0  # Maximum reliability
        self.analysis_results = {}
        self.cache = {}  # Simple in-memory cache
        self.batch_size = 5  # Process multiple checks in one API call
        self.output_dir = Path("output")
        
        # Create output directory
        self.output_dir.mkdir(exist_ok=True)
        
    def _create_batch_prompt(self, compliance_batch: List[Dict]) -> str:
        """
        Create a batch prompt for multiple compliance checks to reduce API calls.
        """
        prompt = """
You are a cybersecurity compliance expert. Analyze these RedHat CIS compliance checks and provide optimal function names.

ANALYZE EACH COMPLIANCE CHECK AND PROVIDE:
1. Best function name for implementation
2. Confidence level (1-100)
3. Brief reasoning

COMPLIANCE CHECKS:
"""
        
        for i, item in enumerate(compliance_batch):
            prompt += f"""
{i+1}. ID: {item.get('id', 'Unknown')}
    Title: {item.get('title', 'No title')}
    Description: {item.get('description', '')[:200]}...
    Audit: {item.get('audit', '')[:100]}...
    Existing Functions: {item.get('function_names', [])}
"""
        
        prompt += """
OUTPUT FORMAT (JSON only):
{
    "results": [
        {
            "compliance_id": "string",
            "function_name": "string - best function name",
            "confidence": "number 1-100",
            "reasoning": "string - why this name is best",
            "compliance_type": "string - type of check"
        }
    ]
}

Provide ONLY the JSON response.
"""
        return prompt
    
    def _get_compliance_hash(self, compliance_item: Dict) -> str:
        """
        Create a hash of compliance item for caching.
        """
        content = f"{compliance_item.get('id')}{compliance_item.get('title')}{compliance_item.get('description')}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def _analyze_batch(self, compliance_batch: List[Dict]) -> List[Dict]:
        """
        Analyze a batch of compliance checks in one API call.
        """
        try:
            prompt = self._create_batch_prompt(compliance_batch)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a cybersecurity compliance expert. Provide only JSON responses."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=800
            )
            
            gpt_response = response.choices[0].message.content.strip()
            
            # Clean response
            if gpt_response.startswith('```json'):
                gpt_response = gpt_response[7:]
            if gpt_response.endswith('```'):
                gpt_response = gpt_response[:-3]
            
            batch_results = json.loads(gpt_response)
            return batch_results.get('results', [])
            
        except Exception as e:
            print(f"Error analyzing batch: {e}")
            # Return fallback results
            fallback_results = []
            for item in compliance_batch:
                fallback_results.append({
                    'compliance_id': item.get('id'),
                    'function_name': 'check_compliance_fallback',
                    'confidence': 50,
                    'reasoning': 'Fallback due to analysis failure',
                    'compliance_type': 'unknown'
                })
            return fallback_results
    
    def analyze_compliance_file(self, input_file: Path) -> Dict:
        """
        Analyze a single compliance file and return results.
        """
        print(f"\nAnalyzing: {input_file.name}")
        
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            print(f"Error reading {input_file}: {e}")
            return {}
        
        print(f"Found {len(data)} compliance checks")
        
        results = []
        total_batches = (len(data) + self.batch_size - 1) // self.batch_size
        
        for i in range(0, len(data), self.batch_size):
            batch_num = (i // self.batch_size) + 1
            batch = data[i:i + self.batch_size]
            
            print(f"Processing batch {batch_num}/{total_batches} ({len(batch)} checks)")
            
            # Check cache for each item in batch
            batch_to_process = []
            for item in batch:
                item_hash = self._get_compliance_hash(item)
                if item_hash in self.cache:
                    results.append(self.cache[item_hash])
                else:
                    batch_to_process.append(item)
            
            # Process uncached items
            if batch_to_process:
                batch_results = self._analyze_batch(batch_to_process)
                
                # Cache results and add to results list
                for j, item in enumerate(batch_to_process):
                    if j < len(batch_results):
                        result = batch_results[j]
                        item_hash = self._get_compliance_hash(item)
                        self.cache[item_hash] = result
                        results.append(result)
                    else:
                        # Fallback if batch result is incomplete
                        fallback = {
                            'compliance_id': item.get('id'),
                            'function_name': 'check_compliance_fallback',
                            'confidence': 50,
                            'reasoning': 'Incomplete batch result',
                            'compliance_type': 'unknown'
                        }
                        results.append(fallback)
                
                # Rate limiting between batches
                time.sleep(2)
        
        # Create output structure
        output_data = []
        for i, item in enumerate(data):
            if i < len(results):
                result = results[i]
                output_item = item.copy()
                output_item['function_names'] = [result['function_name']]
                output_item['gpt_analysis'] = {
                    'confidence': result['confidence'],
                    'reasoning': result['reasoning'],
                    'compliance_type': result['compliance_type']
                }
                output_data.append(output_item)
            else:
                # Fallback for any missing results
                output_item = item.copy()
                output_item['function_names'] = ['check_compliance_fallback']
                output_item['gpt_analysis'] = {
                    'confidence': 50,
                    'reasoning': 'Missing analysis result',
                    'compliance_type': 'unknown'
                }
                output_data.append(output_item)
        
        return {
            'input_file': input_file.name,
            'total_checks': len(data),
            'analyzed_checks': len(results),
            'output_data': output_data
        }
    
    def process_all_compliance_files(self):
        """
        Process all CIS compliance JSON files in the RedHat folder.
        """
        redhat_dir = Path(".")
        json_files = list(redhat_dir.glob("*.json"))
        
        if not json_files:
            print("No JSON files found in RedHat directory")
            return
        
        print(f"Found {len(json_files)} compliance files to process")
        print("=" * 60)
        
        for json_file in json_files:
            if "ARCHIVE" in json_file.name or "BENCHMARK" in json_file.name:
                print(f"\nProcessing: {json_file.name}")
                
                # Analyze the file
                results = self.analyze_compliance_file(json_file)
                
                if results:
                    # Create output filename
                    output_filename = json_file.stem + "_GPT_ANALYZED.json"
                    output_path = self.output_dir / output_filename
                    
                    # Save updated compliance file
                    with open(output_path, 'w', encoding='utf-8') as f:
                        json.dump(results['output_data'], f, indent=2, ensure_ascii=False)
                    
                    print(f"✓ Saved: {output_path}")
                    print(f"  - Total checks: {results['total_checks']}")
                    print(f"  - Analyzed: {results['analyzed_checks']}")
                    
                    # Store results for summary
                    self.analysis_results[json_file.name] = results
                
                print("-" * 60)
        
        # Generate summary report
        self._generate_summary_report()
    
    def _generate_summary_report(self):
        """
        Generate a summary report of all analyses.
        """
        if not self.analysis_results:
            return
        
        summary = {
            'analysis_summary': {
                'total_files_processed': len(self.analysis_results),
                'total_compliance_checks': sum(r['total_checks'] for r in self.analysis_results.values()),
                'total_analyzed': sum(r['analyzed_checks'] for r in self.analysis_results.values()),
                'cache_hits': len(self.cache),
                'api_calls_estimated': len(self.analysis_results) * 2  # Rough estimate
            },
            'file_results': {}
        }
        
        for filename, results in self.analysis_results.items():
            summary['file_results'][filename] = {
                'total_checks': results['total_checks'],
                'analyzed_checks': results['analyzed_checks'],
                'output_file': results['input_file'].replace('.json', '_GPT_ANALYZED.json')
            }
        
        # Save summary
        summary_path = self.output_dir / "analysis_summary.json"
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        print(f"\n📊 Analysis Summary saved to: {summary_path}")
        print(f"📁 All updated compliance files saved to: {self.output_dir}/")
        
        # Display summary
        print(f"\nSUMMARY:")
        print(f"Files processed: {summary['analysis_summary']['total_files_processed']}")
        print(f"Total compliance checks: {summary['analysis_summary']['total_compliance_checks']}")
        print(f"Successfully analyzed: {summary['analysis_summary']['total_analyzed']}")
        print(f"Estimated API calls: {summary['analysis_summary']['api_calls_estimated']}")

def main():
    """
    Main function to run the optimized compliance analysis.
    """
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("ERROR: Set OPENAI_API_KEY environment variable")
        print("export OPENAI_API_KEY='your-api-key-here'")
        return
    
    print("🚀 Optimized GPT-4o Mini RedHat CIS Compliance Analyzer")
    print("=" * 60)
    print("Features:")
    print("✓ Batch processing (5 checks per API call)")
    print("✓ Intelligent caching to reduce API calls")
    print("✓ Organized output structure")
    print("✓ High quality with temperature=0")
    print("✓ Cost optimization without quality compromise")
    print()
    
    analyzer = OptimizedGPTComplianceAnalyzer(api_key)
    analyzer.process_all_compliance_files()
    
    print("\n🎉 Analysis complete! Check the 'output' folder for results.")

if __name__ == "__main__":
    main()
