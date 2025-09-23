#!/usr/bin/env ts-node

import { program } from 'commander';
import * as fs from 'fs';
import { z } from 'zod';
import { AssertionsPackSchema } from '../schemas/assertions.schema';
import { RulesPackSchema, type Rule } from '../schemas/rules.schema';
import { MatrixSchema } from '../schemas/matrix.schema';
import { GenerationProfileSchema } from '../schemas/profile.schema';

interface ValidationResult {
  valid: boolean;
  errors: string[];
  warnings: string[];
}

function validateRulesPack(rulesPack: any): ValidationResult {
  const result: ValidationResult = { valid: true, errors: [], warnings: [] };
  
  try {
    // Validate against schema
    const validatedRulesPack = RulesPackSchema.parse(rulesPack);
    
    // Additional validations
    const rules = validatedRulesPack.rules;
    
    // Check for unique rule_ids
    const ruleIds = rules.map((rule: Rule) => rule.rule_id);
    const uniqueRuleIds = new Set(ruleIds);
    if (ruleIds.length !== uniqueRuleIds.size) {
      result.valid = false;
      result.errors.push('Duplicate rule_ids found');
    }
    
    // Check rule_id format
    const ruleIdRegex = /^aws\.[a-z0-9-]+\.[a-z0-9_.-]+$/;
    const invalidRuleIds = rules.filter((rule: Rule) => !ruleIdRegex.test(rule.rule_id));
    if (invalidRuleIds.length > 0) {
      result.valid = false;
      result.errors.push(`Invalid rule_id format: ${invalidRuleIds.map(r => r.rule_id).join(', ')}`);
    }
    
    // Check for duplicate services in same assertion family
    const assertionFamilies = new Map<string, Set<string>>();
    for (const rule of rules) {
      const family = rule.assertion_id.split('.').slice(0, 2).join('.');
      if (!assertionFamilies.has(family)) {
        assertionFamilies.set(family, new Set());
      }
      assertionFamilies.get(family)!.add(rule.service);
    }
    
    // Check coverage distribution
    const tierCounts = rules.reduce((acc, rule) => {
      acc[rule.coverage_tier] = (acc[rule.coverage_tier] || 0) + 1;
      return acc;
    }, {} as Record<string, number>);
    
    if (rulesPack.coverage === 'core' && tierCounts.extended > 0) {
      result.warnings.push('Core coverage includes extended tier rules');
    }
    
    if (rulesPack.coverage === 'extended' && tierCounts.exhaustive > 0) {
      result.warnings.push('Extended coverage includes exhaustive tier rules');
    }
    
    // Check for services that should be present
    const expectedServices = {
      'crypto_data_protection.encryption_at_rest': ['s3', 'ec2-ebs', 'rds'],
      'network_perimeter.firewall_rules': ['vpc-sg', 'nacl'],
      'identity_access.mfa': ['iam']
    };
    
    for (const [family, expected] of Object.entries(expectedServices)) {
      const familyRules = rules.filter(r => r.assertion_id.startsWith(family));
      const familyServices = new Set(familyRules.map(r => r.service));
      const missing = expected.filter(s => !familyServices.has(s));
      if (missing.length > 0) {
        result.warnings.push(`Missing expected services for ${family}: ${missing.join(', ')}`);
      }
    }
    
  } catch (error) {
    result.valid = false;
    if (error instanceof z.ZodError) {
      result.errors.push(`Schema validation failed: ${error.errors.map(e => e.message).join(', ')}`);
    } else {
      result.errors.push(`Validation error: ${error}`);
    }
  }
  
  return result;
}

function validateInputs(assertionsPath: string, matrixPath: string, profilePath: string): ValidationResult {
  const result: ValidationResult = { valid: true, errors: [], warnings: [] };
  
  try {
    // Validate assertions pack
    if (fs.existsSync(assertionsPath)) {
      const assertionsData = JSON.parse(fs.readFileSync(assertionsPath, 'utf8'));
      AssertionsPackSchema.parse(assertionsData);
    } else {
      result.errors.push(`Assertions pack not found: ${assertionsPath}`);
    }
    
    // Validate matrix
    if (fs.existsSync(matrixPath)) {
      const matrixData = JSON.parse(fs.readFileSync(matrixPath, 'utf8'));
      MatrixSchema.parse(matrixData);
    } else {
      result.errors.push(`Matrix file not found: ${matrixPath}`);
    }
    
    // Validate profile
    if (fs.existsSync(profilePath)) {
      const profileData = JSON.parse(fs.readFileSync(profilePath, 'utf8'));
      GenerationProfileSchema.parse(profileData);
    } else {
      result.errors.push(`Profile file not found: ${profilePath}`);
    }
    
  } catch (error) {
    result.valid = false;
    if (error instanceof z.ZodError) {
      result.errors.push(`Input validation failed: ${error.errors.map(e => e.message).join(', ')}`);
    } else {
      result.errors.push(`Input validation error: ${error}`);
    }
  }
  
  return result;
}

async function main() {
  program
    .argument('<rules-file>', 'Path to rules JSON file to validate')
    .option('-a, --assertions <path>', 'Path to assertions pack JSON file', '../assertions_pack_2025-01-09.json')
    .option('-m, --matrix <path>', 'Path to AWS matrix JSON file', 'matrices/aws.json')
    .option('-p, --profile <path>', 'Path to generation profile JSON file', 'profiles/aws.core.json')
    .option('--validate-inputs', 'Also validate input files')
    .parse();

  const options = program.opts();
  const rulesFile = program.args[0];
  
  try {
    console.log('🔍 Starting validation...');
    
    // Validate inputs if requested
    if (options.validateInputs) {
      console.log('📖 Validating input files...');
      const inputResult = validateInputs(options.assertions, options.matrix, options.profile);
      if (!inputResult.valid) {
        console.error('❌ Input validation failed:');
        inputResult.errors.forEach(error => console.error(`  - ${error}`));
        process.exit(1);
      }
      console.log('✅ Input files valid');
    }
    
    // Load and validate rules pack
    console.log(`📖 Loading rules pack: ${rulesFile}`);
    if (!fs.existsSync(rulesFile)) {
      console.error(`❌ Rules file not found: ${rulesFile}`);
      process.exit(1);
    }
    
    const rulesData = JSON.parse(fs.readFileSync(rulesFile, 'utf8'));
    const result = validateRulesPack(rulesData);
    
    if (result.valid) {
      console.log('✅ Rules pack validation passed');
      
      if (result.warnings.length > 0) {
        console.log('\n⚠️  Warnings:');
        result.warnings.forEach(warning => console.log(`  - ${warning}`));
      }
      
      // Print summary
      const rules = rulesData.rules;
      const tierCounts = rules.reduce((acc: Record<string, number>, rule: Rule) => {
        acc[rule.coverage_tier] = (acc[rule.coverage_tier] || 0) + 1;
        return acc;
      }, {});
      
      console.log('\n📊 Rules Summary:');
      console.log(`  Total rules: ${rules.length}`);
      console.log(`  Coverage: ${rulesData.coverage}`);
      Object.entries(tierCounts).forEach(([tier, count]) => {
        console.log(`  ${tier}: ${count} rules`);
      });
      
    } else {
      console.error('❌ Rules pack validation failed:');
      result.errors.forEach(error => console.error(`  - ${error}`));
      process.exit(1);
    }
    
  } catch (error) {
    console.error('❌ Validation error:', error);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}
