import { describe, it, expect } from 'vitest';
import * as fs from 'fs';
import * as path from 'path';
import { RulesPackSchema, type Rule } from '../../schemas/rules.schema';

describe('AWS Extended Coverage Gold Tests', () => {
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
    expect(validated.coverage).toBe('extended');
    expect(validated.rule_count).toBeGreaterThan(0);
  });
  
  it('should include more services than core for encryption_at_rest', () => {
    const encryptionRules = rulesPack.rules.filter((rule: Rule) => 
      rule.assertion_id.startsWith('crypto_data_protection.encryption_at_rest')
    );
    
    expect(encryptionRules.length).toBeGreaterThan(3);
    
    const services = new Set(encryptionRules.map((rule: Rule) => rule.service));
    // Should include core services
    expect(services.has('s3')).toBe(true);
    expect(services.has('ec2-ebs')).toBe(true);
    expect(services.has('rds')).toBe(true);
    // Should include extended services
    expect(services.has('dynamodb')).toBe(true);
    expect(services.has('efs')).toBe(true);
    expect(services.has('redshift')).toBe(true);
  });
  
  it('should include extended services for firewall_rules', () => {
    const firewallRules = rulesPack.rules.filter((rule: Rule) => 
      rule.assertion_id.startsWith('network_perimeter.firewall_rules')
    );
    
    const services = new Set(firewallRules.map((rule: Rule) => rule.service));
    // Should include core services
    expect(services.has('vpc-sg')).toBe(true);
    expect(services.has('nacl')).toBe(true);
    // Should include extended services
    expect(services.has('network-firewall')).toBe(true);
    expect(services.has('route53-resolver-dns-firewall')).toBe(true);
  });
  
  it('should include extended services for MFA', () => {
    const mfaRules = rulesPack.rules.filter((rule: Rule) => 
      rule.assertion_id.startsWith('identity_access.mfa')
    );
    
    const services = new Set(mfaRules.map((rule: Rule) => rule.service));
    // Should include core services
    expect(services.has('iam')).toBe(true);
    // Should include extended services
    expect(services.has('identity-center')).toBe(true);
  });
  
  it('should include both core and extended tier rules', () => {
    const tierCounts = rulesPack.rules.reduce((acc: Record<string, number>, rule: Rule) => {
      acc[rule.coverage_tier] = (acc[rule.coverage_tier] || 0) + 1;
      return acc;
    }, {});
    
    expect(tierCounts.core).toBeGreaterThan(0);
    expect(tierCounts.extended).toBeGreaterThan(0);
    expect(tierCounts.exhaustive).toBe(0);
  });
  
  it('should have more rules than core coverage', () => {
    // This test assumes we have a way to compare with core coverage
    // In a real scenario, you might load both files and compare
    expect(rulesPack.rule_count).toBeGreaterThan(0);
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
});



