import { describe, it, expect } from 'vitest';
import { z } from 'zod';
import { AssertionsPackSchema } from '../../schemas/assertions.schema';
import { RulesPackSchema } from '../../schemas/rules.schema';
import { MatrixSchema } from '../../schemas/matrix.schema';
import { GenerationProfileSchema } from '../../schemas/profile.schema';

describe('Schema Smoke Tests', () => {
  describe('AssertionsPackSchema', () => {
    it('should validate a minimal assertions pack', () => {
      const minimalPack = {
        version: '1.0',
        mode: 'assertions',
        scope_allowlist: ['identity.user'],
        input_subcategories: [{ domain_key: 'identity_access', subcat_id: 'authentication' }],
        assertions: [{
          assertion_id: 'identity_access.authentication.test',
          title: 'Test assertion',
          scope: 'identity.user',
          params: null,
          evidence_type: 'config_read'
        }]
      };
      
      expect(() => AssertionsPackSchema.parse(minimalPack)).not.toThrow();
    });
    
    it('should reject invalid mode', () => {
      const invalidPack = {
        version: '1.0',
        mode: 'invalid',
        scope_allowlist: ['identity.user'],
        input_subcategories: [],
        assertions: []
      };
      
      expect(() => AssertionsPackSchema.parse(invalidPack)).toThrow();
    });
  });
  
  describe('RulesPackSchema', () => {
    it('should validate a minimal rules pack', () => {
      const minimalPack = {
        version: '1.0',
        provider: 'aws',
        coverage: 'core',
        rule_count: 1,
        rules: [{
          rule_id: 'aws.s3.test_rule',
          assertion_id: 'crypto_data_protection.encryption_at_rest.test',
          provider: 'aws',
          service: 's3',
          resource_type: 'bucket',
          adapter: 'aws.s3.encryption',
          pass_condition: 'bucket_encryption.enabled == true',
          severity: 'medium',
          coverage_tier: 'core',
          evidence_type: 'config_read'
        }]
      };
      
      expect(() => RulesPackSchema.parse(minimalPack)).not.toThrow();
    });
    
    it('should reject invalid rule_id format', () => {
      const invalidPack = {
        version: '1.0',
        provider: 'aws',
        coverage: 'core',
        rule_count: 1,
        rules: [{
          rule_id: 'invalid-rule-id',
          assertion_id: 'crypto_data_protection.encryption_at_rest.test',
          provider: 'aws',
          service: 's3',
          resource_type: 'bucket',
          adapter: 'aws.s3.encryption',
          pass_condition: 'bucket_encryption.enabled == true',
          severity: 'medium',
          coverage_tier: 'core',
          evidence_type: 'config_read'
        }]
      };
      
      expect(() => RulesPackSchema.parse(invalidPack)).toThrow();
    });
  });
  
  describe('MatrixSchema', () => {
    it('should validate a minimal matrix', () => {
      const minimalMatrix = {
        'identity_access.authentication': {
          core: [{ service: 'iam', resource: 'user', adapter: 'aws.iam.user' }],
          extended: [],
          exhaustive: []
        }
      };
      
      expect(() => MatrixSchema.parse(minimalMatrix)).not.toThrow();
    });
    
    it('should reject invalid coverage tier', () => {
      const invalidMatrix = {
        'identity_access.authentication': {
          core: [{ service: 'iam', resource: 'user', adapter: 'aws.iam.user' }],
          invalid: [],
          exhaustive: []
        }
      };
      
      expect(() => MatrixSchema.parse(invalidMatrix)).toThrow();
    });
  });
  
  describe('GenerationProfileSchema', () => {
    it('should validate a minimal profile', () => {
      const minimalProfile = {
        generation_profile: {
          provider: 'aws',
          coverage: 'core'
        }
      };
      
      expect(() => GenerationProfileSchema.parse(minimalProfile)).not.toThrow();
    });
    
    it('should validate profile with include/exclude services', () => {
      const profileWithServices = {
        generation_profile: {
          provider: 'aws',
          coverage: 'extended',
          include_services: ['s3', 'rds'],
          exclude_services: ['dynamodb']
        }
      };
      
      expect(() => GenerationProfileSchema.parse(profileWithServices)).not.toThrow();
    });
    
    it('should reject invalid provider', () => {
      const invalidProfile = {
        generation_profile: {
          provider: 'azure',
          coverage: 'core'
        }
      };
      
      expect(() => GenerationProfileSchema.parse(invalidProfile)).toThrow();
    });
  });
});



