import { describe, it, expect } from 'vitest';
import * as fs from 'fs';
import * as path from 'path';
import { RulesPackSchema, type Rule } from '../../schemas/rules.schema';

describe('AWS Core Coverage Gold Tests', () => {
  let rulesPack: any;
  
  beforeAll(() => {
    const rulesPath = path.join(__dirname, '../../out/aws_rules.json');
    if (fs.existsSync(rulesPath)) {
      rulesPack = JSON.parse(fs.readFileSync(rulesPath, 'utf8'));
    }
  });
  
  it('should have valid rules pack structure', () => {
    expect(rulesPack).toBeDefined();
    const validated = RulesPackSchema.parse(rulesPack);
    expect(validated.provider).toBe('aws');
    expect(validated.coverage).toBe('core');
    expect(validated.rule_count).toBeGreaterThan(0);
  });
  
  it('should include encryption_at_rest rules for core services', () => {
    const encryptionRules = rulesPack.rules.filter((rule: Rule) => 
      rule.assertion_id.startsWith('crypto_data_protection.encryption_at_rest')
    );
    
    expect(encryptionRules.length).toBeGreaterThanOrEqual(3);
    
    const services = new Set(encryptionRules.map((rule: Rule) => rule.service));
    expect(services.has('s3')).toBe(true);
    expect(services.has('ec2-ebs')).toBe(true);
    expect(services.has('rds')).toBe(true);
  });
  
  it('should include firewall_rules for core services', () => {
    const firewallRules = rulesPack.rules.filter((rule: Rule) => 
      rule.assertion_id.startsWith('network_perimeter.firewall_rules')
    );
    
    expect(firewallRules.length).toBeGreaterThan(0);
    
    const services = new Set(firewallRules.map((rule: Rule) => rule.service));
    expect(services.has('vpc-sg')).toBe(true);
    expect(services.has('nacl')).toBe(true);
  });
  
  it('should include MFA rules for IAM', () => {
    const mfaRules = rulesPack.rules.filter((rule: Rule) => 
      rule.assertion_id.startsWith('identity_access.mfa')
    );
    
    expect(mfaRules.length).toBeGreaterThan(0);
    
    const services = new Set(mfaRules.map((rule: Rule) => rule.service));
    expect(services.has('iam')).toBe(true);
  });
  
  it('should have valid rule_id format', () => {
    const ruleIdRegex = /^aws\.[a-z0-9-]+\.[a-z0-9_.-]+$/;
    
    for (const rule of rulesPack.rules) {
      expect(rule.rule_id).toMatch(ruleIdRegex);
    }
  });
  
  it('should have unique rule_ids', () => {
    const ruleIds = rulesPack.rules.map((rule: Rule) => rule.rule_id);
    const uniqueRuleIds = new Set(ruleIds);
    expect(ruleIds.length).toBe(uniqueRuleIds.size);
  });
  
  it('should only include core tier rules', () => {
    const nonCoreRules = rulesPack.rules.filter((rule: Rule) => rule.coverage_tier !== 'core');
    expect(nonCoreRules.length).toBe(0);
  });
  
  it('should have appropriate severity levels', () => {
    const severities = new Set(rulesPack.rules.map((rule: Rule) => rule.severity));
    expect(severities.has('low')).toBe(true);
    expect(severities.has('medium')).toBe(true);
    expect(severities.has('high')).toBe(true);
  });
  
  it('should have evidence types', () => {
    const evidenceTypes = new Set(rulesPack.rules.map((rule: Rule) => rule.evidence_type));
    expect(evidenceTypes.has('config_read')).toBe(true);
  });
  
  it('should have pass conditions', () => {
    for (const rule of rulesPack.rules) {
      expect(rule.pass_condition).toBeDefined();
      expect(rule.pass_condition).not.toBe('');
    }
  });
});



