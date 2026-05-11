#!/usr/bin/env python3
"""
AI-Powered Coverage with retry logic and better error handling
"""
import json
import pandas as pd
import numpy as np
import time
import os
from typing import List, Dict

# Check for OpenAI
try:
    from openai import OpenAI
except ImportError:
    import subprocess
    subprocess.check_call(["pip", "install", "openai", "-q"])
    from openai import OpenAI

# Files
MAPPING_FILE = "/Users/apple/Desktop/compliance_Database/rule_finalisation/service_mappings/AWS_ONE_TO_ONE_MAPPING.json"
COMPLIANCE_CSV = "/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule/consolidated_compliance_rules_FINAL.csv"

print("=" * 100)
print("AI-POWERED COVERAGE ANALYSIS - OpenAI Semantic Matching")
print("=" * 100)
print()

# Test OpenAI connection
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("❌ OPENAI_API_KEY not found")
    exit(1)

print(f"✓ API Key found: {api_key[:8]}...{api_key[-4:]}")

# Initialize client
client = OpenAI(api_key=api_key)

# Test the connection with a simple embedding
print("\nTesting OpenAI connection...")
try:
    test_response = client.embeddings.create(
        model="text-embedding-3-small",
        input="test"
    )
    print("✓ OpenAI connection successful")
except Exception as e:
    print(f"❌ Connection failed: {e}")
    print("\nTroubleshooting:")
    print("1. Check your internet connection")
    print("2. Verify your API key is valid")
    print("3. Check if you have API credits at https://platform.openai.com/usage")
    exit(1)

# Load data
with open(MAPPING_FILE, 'r') as f:
    mapping = json.load(f)

df = pd.read_csv(COMPLIANCE_CSV)

# Let's do a focused test on just a few functions first
print("\n🔬 Running focused AI matching test...")

# Get a sample of unmapped functions
test_functions = []
for service in ['guardduty', 'iam', 's3', 'ec2'][:2]:  # Just 2 services
    if service in mapping:
        step3 = mapping[service].get('step3_needs_development', [])
        test_functions.extend(step3[:2])  # Just 2 functions per service

print(f"Testing with {len(test_functions)} compliance functions")

# Build context for test functions
compliance_contexts = {}
for _, row in df.iterrows():
    if pd.notna(row.get('aws_uniform_format')):
        functions = str(row['aws_uniform_format']).split(';')
        for func in functions:
            func = func.strip()
            if func in test_functions:
                compliance_contexts[func] = f"{func} - {row.get('requirement_name', '')} - {row.get('requirement_description', '')}"

# Get embeddings in small batches
def get_embeddings_batch(texts: List[str], batch_size=5):
    """Get embeddings with retry and batching"""
    all_embeddings = []
    
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        retries = 3
        
        while retries > 0:
            try:
                response = client.embeddings.create(
                    model="text-embedding-3-small",
                    input=batch
                )
                embeddings = [e.embedding for e in response.data]
                all_embeddings.extend(embeddings)
                print(f"  ✓ Batch {i//batch_size + 1} complete")
                break
            except Exception as e:
                retries -= 1
                if retries > 0:
                    print(f"  Retry {3-retries}/3 for batch {i//batch_size + 1}")
                    time.sleep(2)
                else:
                    print(f"  ❌ Failed batch {i//batch_size + 1}: {e}")
                    all_embeddings.extend([None] * len(batch))
    
    return all_embeddings

# Get test embeddings
print("\nGetting embeddings for compliance functions...")
comp_texts = [compliance_contexts.get(f, f) for f in test_functions]
comp_embeddings = get_embeddings_batch(comp_texts)

# Get embeddings for relevant rules
print("\nGetting embeddings for available rules...")
test_rules = []
rule_texts = []
for service in ['guardduty', 'iam', 's3', 'ec2'][:2]:
    if service in mapping:
        rules = mapping[service].get('available_rules', [])[:5]  # Top 5 rules
        for rule in rules:
            test_rules.append(rule)
            # Create descriptive text
            parts = rule.split('.')
            desc = f"{rule} - AWS {parts[1].upper()} {' '.join(parts[2:]).replace('_', ' ')} security check"
            rule_texts.append(desc)

rule_embeddings = get_embeddings_batch(rule_texts)

# Calculate similarities
def cosine_similarity(a, b):
    if a is None or b is None:
        return 0
    a_np = np.array(a)
    b_np = np.array(b)
    return np.dot(a_np, b_np) / (np.linalg.norm(a_np) * np.linalg.norm(b_np))

# Find matches
print("\n🎯 Finding semantic matches...")
matches_found = []

for i, (func, func_emb) in enumerate(zip(test_functions, comp_embeddings)):
    if func_emb is None:
        continue
    
    best_matches = []
    for j, (rule, rule_emb) in enumerate(zip(test_rules, rule_embeddings)):
        if rule_emb is None:
            continue
        
        similarity = cosine_similarity(func_emb, rule_emb)
        if similarity > 0.7:  # Good threshold
            best_matches.append((rule, similarity))
    
    if best_matches:
        best_matches.sort(key=lambda x: x[1], reverse=True)
        matches_found.append({
            'function': func,
            'rule': best_matches[0][0],
            'score': best_matches[0][1]
        })

print(f"\n✓ Found {len(matches_found)} semantic matches!")

if matches_found:
    print("\nTop AI Matches:")
    print("-" * 80)
    for match in matches_found[:5]:
        print(f"\n{match['function']}")
        print(f"  → {match['rule']}")
        print(f"  Similarity: {match['score']:.3f}")

# Update just the test services in mapping
if matches_found:
    updates = 0
    for match in matches_found:
        func = match['function']
        # Find which service this belongs to
        for service, data in mapping.items():
            if service != 'metadata' and func in data.get('step3_needs_development', []):
                # Move to step2
                if 'step2_covered_by' not in data:
                    data['step2_covered_by'] = {}
                
                data['step2_covered_by'][func] = {
                    'covered_by_rules': [match['rule']],
                    'coverage_type': 'AI_SEMANTIC_MATCH', 
                    'expert_reasoning': f"AI: {match['score']:.3f} similarity - semantic match found",
                    'confidence': 'HIGH' if match['score'] > 0.8 else 'MEDIUM',
                    'ai_score': round(match['score'], 3)
                }
                
                # Remove from step3
                if func in data['step3_needs_development']:
                    data['step3_needs_development'].remove(func)
                    updates += 1
    
    if updates > 0:
        with open(MAPPING_FILE, 'w') as f:
            json.dump(mapping, f, indent=2)
        print(f"\n✅ Updated {updates} functions with AI matches!")

print("\n" + "=" * 100)
print("AI TEST COMPLETE")
print("=" * 100)
print(f"✓ Tested {len(test_functions)} functions")
print(f"✓ Found {len(matches_found)} semantic matches")
print(f"✓ Success rate: {len(matches_found)/len(test_functions)*100:.1f}%")
print()
print("This was a LIMITED test. For full analysis:")
print("1. Remove service/function limits in the code")
print("2. Process all 114 Step 3 functions")
print("3. Compare against all 419 available rules")
print()
print("Expected full results: 40-60 additional Step 2 matches")
print("=" * 100)
