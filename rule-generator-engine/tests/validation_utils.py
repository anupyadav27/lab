#!/usr/bin/env python3
"""
Schema Validation Utilities for Step 3 Rule Generation
Validates rules against enhanced schemas to ensure quality standards
"""

import re
import json
from typing import Dict, List, Any, Tuple
from datetime import datetime

class RuleSchemaValidator:
    """Validates rules against Step 3 quality standards"""
    
    def __init__(self):
        # Rule ID pattern: adapter.assertion_tail (e.g., k8s.rbac.verify_strong_authn.strong_authn_enabled)
        self.rule_id_pattern = re.compile(r'^[a-z0-9.-]+\.[a-z0-9_.-]+$')
        self.evidence_type_pattern = re.compile(r'^[a-z0-9.-]+\.[a-z0-9.-]+\[\]')
        self.validation_types = [
            'count_check', 'age_check', 'field_check', 'security_context_check',
            'annotation_check', 'network_policy_check', 'capabilities_check',
            'image_check', 'secret_type_check', 'data_check', 'resource_check',
            'generic_check'
        ]
    
    def validate_rule_id(self, rule_id: str) -> Tuple[bool, str]:
        """Validate rule ID follows pattern: adapter.assertion_tail"""
        if not self.rule_id_pattern.match(rule_id):
            return False, f"Rule ID {rule_id} does not follow pattern: adapter.assertion_tail"
        return True, "Rule ID is valid"
    
    def validate_adapter_evidence_type(self, evidence_type: str) -> Tuple[bool, str]:
        """Validate adapter evidence type is specific resource path"""
        if not self.evidence_type_pattern.match(evidence_type):
            return False, f"Evidence type {evidence_type} is not specific resource path"
        return True, "Evidence type is valid"
    
    def validate_content_specificity(self, notes: str, rationale: str, adapter: str) -> Tuple[bool, str]:
        """Validate notes and rationale are specific to the rule"""
        
        # Check minimum lengths
        if len(notes) < 20:
            return False, f"Notes too short: {len(notes)} characters (minimum 20)"
        if len(rationale) < 50:
            return False, f"Rationale too short: {len(rationale)} characters (minimum 50)"
        
        # Check for generic content
        generic_phrases = [
            "implement security best practices",
            "ensure compliance",
            "follow security guidelines",
            "apply security controls"
        ]
        
        for phrase in generic_phrases:
            if phrase.lower() in notes.lower():
                return False, f"Notes contain generic phrase: {phrase}"
            if phrase.lower() in rationale.lower():
                return False, f"Rationale contain generic phrase: {phrase}"
        
        return True, "Content is specific"
    
    def validate_enhanced_fields(self, rule: Dict[str, Any]) -> Tuple[bool, str]:
        """Validate enhanced fields meet quality standards"""
        
        required_fields = ['title', 'description', 'remediation', 'implementation_priority', 'check_frequency']
        
        for field in required_fields:
            if field not in rule:
                return False, f"Missing enhanced field: {field}"
        
        # Check minimum lengths
        if len(rule['title']) < 5:
            return False, f"Title too short: {len(rule['title'])} characters (minimum 5)"
        if len(rule['description']) < 20:
            return False, f"Description too short: {len(rule['description'])} characters (minimum 20)"
        if len(rule['remediation']) < 20:
            return False, f"Remediation too short: {len(rule['remediation'])} characters (minimum 20)"
        
        # Check enum values
        if rule['implementation_priority'] not in ['low', 'medium', 'high']:
            return False, f"Invalid implementation_priority: {rule['implementation_priority']}"
        if rule['check_frequency'] not in ['weekly', 'daily', 'hourly', 'continuous']:
            return False, f"Invalid check_frequency: {rule['check_frequency']}"
        
        return True, "Enhanced fields are valid"
    
    def validate_adapter_spec(self, adapter_spec: Dict[str, Any]) -> Tuple[bool, str]:
        """Validate adapter spec is crisp and engine-consumable"""
        
        required_fields = ['function', 'evidence_path', 'validation', 'returns']
        for field in required_fields:
            if field not in adapter_spec:
                return False, f"Missing adapter_spec field: {field}"
        
        # Validate validation type
        if adapter_spec['validation']['type'] not in self.validation_types:
            return False, f"Invalid validation type: {adapter_spec['validation']['type']}"
        
        # Validate returns structure
        required_returns = ['compliant', 'total_checked', 'compliant_count', 'violations']
        for field in required_returns:
            if field not in adapter_spec['returns']:
                return False, f"Missing returns field: {field}"
        
        return True, "Adapter spec is valid"
    
    def validate_cohesive_fields(self, rule: Dict[str, Any]) -> Tuple[bool, str]:
        """Validate all fields work together cohesively"""
        
        # Check 1: adapter_evidence_type matches adapter_spec.evidence_path
        if rule['adapter_evidence_type'] != rule['adapter_spec']['evidence_path']:
            return False, "adapter_evidence_type must match adapter_spec.evidence_path"
        
        # Check 2: adapter matches rule_id
        if rule['adapter'] != rule['rule_id']:
            return False, "adapter must match rule_id"
        
        # Check 3: params are used in validation
        if rule.get('params'):
            validation = rule['adapter_spec']['validation']
            params_used = False
            for param_key in rule['params'].keys():
                if param_key in str(validation):
                    params_used = True
                    break
            if not params_used:
                return False, "params must be used in adapter_spec.validation"
        
        return True, "Fields are cohesive"
    
    def validate_rule(self, rule: Dict[str, Any]) -> Dict[str, Any]:
        """Validate complete rule against schema"""
        
        validation_results = {
            'rule_id': rule.get('rule_id', ''),
            'valid': True,
            'errors': [],
            'warnings': []
        }
        
        # Validate rule ID
        is_valid, message = self.validate_rule_id(rule['rule_id'])
        if not is_valid:
            validation_results['valid'] = False
            validation_results['errors'].append(message)
        
        # Validate adapter evidence type
        is_valid, message = self.validate_adapter_evidence_type(rule['adapter_evidence_type'])
        if not is_valid:
            validation_results['valid'] = False
            validation_results['errors'].append(message)
        
        # Validate content specificity
        is_valid, message = self.validate_content_specificity(
            rule['notes'], rule['rationale'], rule['adapter']
        )
        if not is_valid:
            validation_results['valid'] = False
            validation_results['errors'].append(message)
        
        # Validate enhanced fields
        is_valid, message = self.validate_enhanced_fields(rule)
        if not is_valid:
            validation_results['valid'] = False
            validation_results['errors'].append(message)
        
        # Validate adapter spec
        is_valid, message = self.validate_adapter_spec(rule['adapter_spec'])
        if not is_valid:
            validation_results['valid'] = False
            validation_results['errors'].append(message)
        
        # Validate cohesive fields
        is_valid, message = self.validate_cohesive_fields(rule)
        if not is_valid:
            validation_results['valid'] = False
            validation_results['errors'].append(message)
        
        return validation_results
    
    def validate_rules_pack(self, rules_pack: Dict[str, Any]) -> Dict[str, Any]:
        """Validate complete rules pack"""
        
        validation_results = {
            'total_rules': len(rules_pack.get('rules', [])),
            'valid_rules': 0,
            'invalid_rules': 0,
            'rule_validations': [],
            'overall_valid': True,
            'errors': [],
            'warnings': []
        }
        
        # Validate each rule
        for rule in rules_pack.get('rules', []):
            rule_validation = self.validate_rule(rule)
            validation_results['rule_validations'].append(rule_validation)
            
            if rule_validation['valid']:
                validation_results['valid_rules'] += 1
            else:
                validation_results['invalid_rules'] += 1
                validation_results['overall_valid'] = False
        
        # Check for duplicate rule IDs
        rule_ids = [rule['rule_id'] for rule in rules_pack.get('rules', [])]
        unique_rule_ids = set(rule_ids)
        if len(rule_ids) != len(unique_rule_ids):
            validation_results['overall_valid'] = False
            validation_results['errors'].append(f"Found {len(rule_ids) - len(unique_rule_ids)} duplicate rule IDs")
        
        return validation_results

def validate_rules_file(file_path: str) -> Dict[str, Any]:
    """Validate rules file against schema"""
    
    with open(file_path, 'r') as f:
        rules_pack = json.load(f)
    
    validator = RuleSchemaValidator()
    return validator.validate_rules_pack(rules_pack)

def main():
    """Main function to validate rules file"""
    
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python validation_utils.py <rules_file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    print(f"🔍 Validating rules file: {file_path}")
    print("=" * 60)
    
    try:
        validation_results = validate_rules_file(file_path)
        
        print(f"📊 Validation Results:")
        print(f"  Total Rules: {validation_results['total_rules']}")
        print(f"  Valid Rules: {validation_results['valid_rules']}")
        print(f"  Invalid Rules: {validation_results['invalid_rules']}")
        print(f"  Overall Valid: {'✅' if validation_results['overall_valid'] else '❌'}")
        
        if validation_results['errors']:
            print(f"\n❌ Errors:")
            for error in validation_results['errors']:
                print(f"  - {error}")
        
        if validation_results['warnings']:
            print(f"\n⚠️  Warnings:")
            for warning in validation_results['warnings']:
                print(f"  - {warning}")
        
        # Show invalid rules
        invalid_rules = [rv for rv in validation_results['rule_validations'] if not rv['valid']]
        if invalid_rules:
            print(f"\n❌ Invalid Rules:")
            for rule_validation in invalid_rules[:5]:  # Show first 5
                print(f"  - {rule_validation['rule_id']}: {', '.join(rule_validation['errors'])}")
        
        print("=" * 60)
        
        if validation_results['overall_valid']:
            print("✅ All rules pass schema validation!")
        else:
            print("❌ Some rules failed schema validation!")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Validation failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
