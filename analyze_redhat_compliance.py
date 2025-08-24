#!/usr/bin/env python3
"""
Intelligent RedHat CIS Compliance Function Analysis Tool
This script analyzes each compliance check individually and provides intelligent recommendations
for function names based on the actual compliance requirements.
"""

import json
import re
from typing import Dict, List, Tuple, Optional

class ComplianceAnalyzer:
    def __init__(self):
        self.analysis_results = []
        
    def analyze_compliance_check(self, item: Dict) -> Dict:
        """
        Analyze a single compliance check and provide intelligent recommendations.
        """
        compliance_id = item.get('id', 'Unknown')
        title = item.get('title', 'No title')
        description = item.get('description', '')
        audit = item.get('audit', '')
        function_names = item.get('function_names', [])
        
        print(f"\n{'='*80}")
        print(f"Analyzing: {compliance_id} - {title}")
        print(f"{'='*80}")
        
        # Analyze the compliance requirement
        analysis = self._analyze_requirement(description, audit)
        
        # Review existing function names
        function_analysis = self._analyze_function_names(function_names, analysis)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(analysis, function_analysis)
        
        result = {
            'compliance_id': compliance_id,
            'title': title,
            'analysis': analysis,
            'function_analysis': function_analysis,
            'recommendations': recommendations,
            'final_function_name': recommendations['recommended_function']
        }
        
        self.analysis_results.append(result)
        return result
    
    def _analyze_requirement(self, description: str, audit: str) -> Dict:
        """
        Analyze the compliance requirement to understand what needs to be checked.
        """
        analysis = {
            'check_type': 'unknown',
            'target_system': 'unknown',
            'specific_checks': [],
            'complexity': 'simple'
        }
        
        # Determine check type
        if 'filesystem' in description.lower() or 'mount' in description.lower():
            analysis['check_type'] = 'filesystem'
        elif 'partition' in description.lower():
            analysis['check_type'] = 'partition'
        elif 'permission' in description.lower() or 'ownership' in description.lower():
            analysis['check_type'] = 'permission'
        elif 'service' in description.lower() or 'daemon' in description.lower():
            analysis['check_type'] = 'service'
        elif 'network' in description.lower() or 'port' in description.lower():
            analysis['check_type'] = 'network'
        elif 'user' in description.lower() or 'account' in description.lower():
            analysis['check_type'] = 'user'
        elif 'kernel' in description.lower() or 'module' in description.lower():
            analysis['check_type'] = 'kernel'
        
        # Determine target system
        if 'tmp' in description.lower():
            analysis['target_system'] = 'tmp_directory'
        elif 'var' in description.lower():
            analysis['target_system'] = 'var_directory'
        elif 'home' in description.lower():
            analysis['target_system'] = 'home_directory'
        elif 'root' in description.lower():
            analysis['target_system'] = 'root_directory'
        
        # Extract specific checks from audit command
        audit_checks = []
        if 'modprobe' in audit:
            audit_checks.append('kernel_module_check')
        if 'lsmod' in audit:
            audit_checks.append('loaded_modules_check')
        if 'mount' in audit:
            audit_checks.append('mount_options_check')
        if 'grep' in audit:
            audit_checks.append('configuration_check')
        if 'stat' in audit:
            audit_checks.append('file_permissions_check')
        
        analysis['specific_checks'] = audit_checks
        
        # Determine complexity
        if len(audit_checks) > 2 or '&&' in audit:
            analysis['complexity'] = 'complex'
        elif len(audit_checks) > 1:
            analysis['complexity'] = 'medium'
        
        return analysis
    
    def _analyze_function_names(self, function_names: List[str], analysis: Dict) -> Dict:
        """
        Analyze existing function names and provide insights.
        """
        if not function_names:
            return {
                'count': 0,
                'quality': 'none',
                'issues': ['No function names provided'],
                'best_candidate': None
            }
        
        function_analysis = {
            'count': len(function_names),
            'quality': 'good',
            'issues': [],
            'best_candidate': None,
            'redundant_names': [],
            'unclear_names': []
        }
        
        # Check for redundancy
        seen_patterns = set()
        for name in function_names:
            # Extract core pattern (remove common suffixes)
            core = re.sub(r'_(enabled|set|configured|restriction|enforced|protected|secure|compliant|applied)$', '', name)
            if core in seen_patterns:
                function_analysis['redundant_names'].append(name)
            seen_patterns.add(core)
        
        # Check for unclear names
        for name in function_names:
            if len(name) > 60:
                function_analysis['unclear_names'].append(name)
            if name.count('_') > 6:
                function_analysis['unclear_names'].append(name)
        
        # Determine quality
        if function_analysis['redundant_names']:
            function_analysis['quality'] = 'poor'
            function_analysis['issues'].append(f"Found {len(function_analysis['redundant_names'])} redundant names")
        
        if function_analysis['unclear_names']:
            function_analysis['quality'] = 'poor'
            function_analysis['issues'].append(f"Found {len(function_analysis['unclear_names'])} unclear names")
        
        # Select best candidate
        if function_names:
            # Prefer shorter, clearer names
            sorted_names = sorted(function_names, key=lambda x: (len(x), x.count('_')))
            function_analysis['best_candidate'] = sorted_names[0]
        
        return function_analysis
    
    def _generate_recommendations(self, analysis: Dict, function_analysis: Dict) -> Dict:
        """
        Generate intelligent recommendations for function names.
        """
        recommendations = {
            'recommended_function': '',
            'reasoning': '',
            'alternative_names': [],
            'implementation_notes': ''
        }
        
        # Generate base function name based on analysis
        base_name = self._generate_base_function_name(analysis)
        
        # Check if existing names are sufficient
        if function_analysis['count'] == 1 and function_analysis['quality'] == 'good':
            recommendations['recommended_function'] = function_analysis['best_candidate']
            recommendations['reasoning'] = "Single, high-quality function name already exists"
        elif function_analysis['count'] > 1 and function_analysis['quality'] == 'good':
            recommendations['recommended_function'] = function_analysis['best_candidate']
            recommendations['reasoning'] = f"Selected best from {function_analysis['count']} good options"
        else:
            # Generate new function name
            recommendations['recommended_function'] = base_name
            recommendations['reasoning'] = f"Generated new function name based on compliance analysis"
        
        # Generate alternative names
        recommendations['alternative_names'] = self._generate_alternative_names(analysis)
        
        # Add implementation notes
        recommendations['implementation_notes'] = self._generate_implementation_notes(analysis)
        
        return recommendations
    
    def _generate_base_function_name(self, analysis: Dict) -> str:
        """
        Generate a base function name based on the compliance analysis.
        """
        prefix = 'check_'
        
        if analysis['check_type'] == 'filesystem':
            prefix += 'filesystem_'
        elif analysis['check_type'] == 'partition':
            prefix += 'partition_'
        elif analysis['check_type'] == 'permission':
            prefix += 'permission_'
        elif analysis['check_type'] == 'service':
            prefix += 'service_'
        elif analysis['check_type'] == 'network':
            prefix += 'network_'
        elif analysis['check_type'] == 'user':
            prefix += 'user_'
        elif analysis['check_type'] == 'kernel':
            prefix += 'kernel_'
        
        if analysis['target_system'] != 'unknown':
            prefix += f"{analysis['target_system']}_"
        
        # Add specific check type
        if 'kernel_module_check' in analysis['specific_checks']:
            prefix += 'module_disabled'
        elif 'mount_options_check' in analysis['specific_checks']:
            prefix += 'mount_options'
        elif 'file_permissions_check' in analysis['specific_checks']:
            prefix += 'permissions'
        else:
            prefix += 'compliance'
        
        return prefix
    
    def _generate_alternative_names(self, analysis: Dict) -> List[str]:
        """
        Generate alternative function names for consideration.
        """
        alternatives = []
        
        # Alternative 1: More specific
        if analysis['check_type'] == 'filesystem':
            alternatives.append(f"verify_filesystem_{analysis['target_system']}_configuration")
        
        # Alternative 2: Action-oriented
        if analysis['check_type'] == 'partition':
            alternatives.append(f"ensure_partition_{analysis['target_system']}_exists")
        
        # Alternative 3: Compliance-focused
        alternatives.append(f"validate_{analysis['check_type']}_compliance")
        
        return alternatives
    
    def _generate_implementation_notes(self, analysis: Dict) -> str:
        """
        Generate implementation notes for the compliance check.
        """
        notes = []
        
        if analysis['complexity'] == 'complex':
            notes.append("This check requires multiple verification steps")
        
        if 'kernel_module_check' in analysis['specific_checks']:
            notes.append("Check both modprobe configuration and loaded modules")
        
        if 'mount_options_check' in analysis['specific_checks']:
            notes.append("Verify mount options in /etc/fstab and current mounts")
        
        if 'file_permissions_check' in analysis['specific_checks']:
            notes.append("Check file ownership, permissions, and attributes")
        
        return "; ".join(notes) if notes else "Standard compliance check implementation"
    
    def analyze_file(self, input_file: str) -> List[Dict]:
        """
        Analyze all compliance checks in the file.
        """
        print(f"Reading input file: {input_file}")
        
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            print(f"Error reading input file: {e}")
            return []
        
        print(f"Found {len(data)} compliance checks to analyze")
        print("Starting analysis...\n")
        
        for item in data:
            self.analyze_compliance_check(item)
        
        return self.analysis_results
    
    def generate_summary_report(self) -> str:
        """
        Generate a summary report of all analyses.
        """
        if not self.analysis_results:
            return "No analysis results available"
        
        total_checks = len(self.analysis_results)
        good_quality = sum(1 for r in self.analysis_results if r['function_analysis']['quality'] == 'good')
        poor_quality = sum(1 for r in self.analysis_results if r['function_analysis']['quality'] == 'poor')
        new_functions = sum(1 for r in self.analysis_results if 'Generated new function name' in r['recommendations']['reasoning'])
        
        report = f"""
COMPLIANCE ANALYSIS SUMMARY REPORT
{'='*50}
Total Compliance Checks: {total_checks}
Good Quality Function Names: {good_quality}
Poor Quality Function Names: {poor_quality}
New Function Names Generated: {new_functions}

RECOMMENDATIONS:
{'='*50}
"""
        
        # Group by check type
        check_types = {}
        for result in self.analysis_results:
            check_type = result['analysis']['check_type']
            if check_type not in check_types:
                check_types[check_type] = []
            check_types[check_type].append(result)
        
        for check_type, results in check_types.items():
            report += f"\n{check_type.upper()} CHECKS ({len(results)}):\n"
            report += "-" * (len(check_type) + 8) + "\n"
            
            for result in results[:5]:  # Show first 5 of each type
                report += f"  {result['compliance_id']}: {result['final_function_name']}\n"
            
            if len(results) > 5:
                report += f"  ... and {len(results) - 5} more\n"
        
        return report

def main():
    """
    Main function to run the compliance analysis.
    """
    input_file = "raw_compliance_database/linux/redhat/CIS_RED_HAT_ENTERPRISE_LINUX_6_BENCHMARK_V3.0.0_ARCHIVE (1).json"
    
    analyzer = ComplianceAnalyzer()
    results = analyzer.analyze_file(input_file)
    
    # Generate and display summary report
    summary = analyzer.generate_summary_report()
    print("\n" + summary)
    
    # Save detailed results
    output_file = "redhat_compliance_analysis_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\nDetailed analysis results saved to: {output_file}")

if __name__ == "__main__":
    main()
