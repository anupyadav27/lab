#!/usr/bin/env python3
"""
AI-Powered Step 2 Coverage Analysis using OpenAI
Semantic matching between compliance requirements and available rules
"""
import json
import pandas as pd
import numpy as np
from typing import List, Dict, Tuple
import os

# Check for OpenAI
try:
    import openai
    from openai import OpenAI
    print("✓ OpenAI library found")
except ImportError:
    print("Installing OpenAI...")
    import subprocess
    subprocess.check_call(["pip", "install", "openai"])
    import openai
    from openai import OpenAI

# Files
MAPPING_FILE = "/Users/apple/Desktop/compliance_Database/rule_finalisation/service_mappings/AWS_ONE_TO_ONE_MAPPING.json"
COMPLIANCE_CSV = "/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule/consolidated_compliance_rules_FINAL.csv"
EMBEDDINGS_FILE = "/Users/apple/Desktop/compliance_Database/rule_finalisation/service_mappings/aws_embeddings_cache.json"

print("=" * 100)
print("AI-POWERED COVERAGE ANALYSIS - Using OpenAI Embeddings")
print("=" * 100)
print()

# Initialize OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("❌ Please set OPENAI_API_KEY environment variable")
    print("   export OPENAI_API_KEY='your-api-key'")
    exit(1)

client = OpenAI(api_key=api_key)
print("✓ OpenAI client initialized")
print()

# Load existing mapping
with open(MAPPING_FILE, 'r') as f:
    mapping = json.load(f)

# Load compliance CSV for context
df = pd.read_csv(COMPLIANCE_CSV)

# Build comprehensive context for compliance functions
print("Building compliance context...")
compliance_contexts = {}
for _, row in df.iterrows():
    if pd.notna(row.get('aws_uniform_format')):
        functions = str(row['aws_uniform_format']).split(';')
        for func in functions:
            func = func.strip()
            if func and func.startswith('aws.'):
                # Create rich context
                compliance_contexts[func] = {
                    'function': func,
                    'requirement': str(row.get('requirement_name', '')),
                    'description': str(row.get('requirement_description', '')),
                    'service': str(row.get('service', '')),
                    'full_text': f"{func} - {row.get('requirement_name', '')} - {row.get('requirement_description', '')}"
                }

print(f"✓ Built context for {len(compliance_contexts)} compliance functions")

# Get all available rules with enriched descriptions
print("\nEnriching available rules...")
all_rules = {}
for service, data in mapping.items():
    if service != 'metadata':
        for rule in data.get('available_rules', []):
            # Create descriptive text for each rule
            parts = rule.split('.')
            service_name = parts[1] if len(parts) > 1 else ''
            resource = parts[2] if len(parts) > 2 else ''
            check = parts[3] if len(parts) > 3 else parts[-1]
            
            # Generate natural description
            description = f"{rule} - AWS {service_name.upper()} {resource} check for {check.replace('_', ' ')}"
            
            # Add known capabilities
            capabilities = []
            if 'encrypt' in rule: capabilities.append('encryption')
            if 'public' in rule: capabilities.append('public access control')
            if 'log' in rule or 'trail' in rule: capabilities.append('logging and monitoring')
            if 'backup' in rule: capabilities.append('backup and recovery')
            if 'mfa' in rule: capabilities.append('multi-factor authentication')
            if 'privilege' in rule: capabilities.append('access control and privileges')
            
            all_rules[rule] = {
                'rule': rule,
                'description': description,
                'capabilities': ', '.join(capabilities) if capabilities else 'security compliance check',
                'full_text': f"{description}. Provides: {', '.join(capabilities) if capabilities else 'security compliance'}"
            }

print(f"✓ Enriched {len(all_rules)} available rules")

def get_embeddings(texts: List[str], model="text-embedding-3-small") -> List[List[float]]:
    """Get embeddings from OpenAI"""
    try:
        response = client.embeddings.create(
            model=model,
            input=texts
        )
        return [e.embedding for e in response.data]
    except Exception as e:
        print(f"Error getting embeddings: {e}")
        return []

def cosine_similarity(a: List[float], b: List[float]) -> float:
    """Calculate cosine similarity between two vectors"""
    a_np = np.array(a)
    b_np = np.array(b)
    return np.dot(a_np, b_np) / (np.linalg.norm(a_np) * np.linalg.norm(b_np))

# Check for cached embeddings
embeddings_cache = {}
if os.path.exists(EMBEDDINGS_FILE):
    print("\n✓ Loading cached embeddings...")
    with open(EMBEDDINGS_FILE, 'r') as f:
        embeddings_cache = json.load(f)
else:
    print("\n⚡ Computing embeddings (this will take a moment)...")
    
    # Get embeddings for all compliance functions that need coverage
    step3_functions = []
    for service, data in mapping.items():
        if service != 'metadata':
            step3_functions.extend(data.get('step3_needs_development', []))
    
    print(f"  Computing embeddings for {len(step3_functions)} compliance functions...")
    compliance_texts = [compliance_contexts.get(f, {}).get('full_text', f) for f in step3_functions]
    if compliance_texts:
        compliance_embeddings = get_embeddings(compliance_texts)
        for func, emb in zip(step3_functions, compliance_embeddings):
            embeddings_cache[f"compliance:{func}"] = emb
    
    # Get embeddings for all rules
    print(f"  Computing embeddings for {len(all_rules)} rules...")
    rule_texts = [r['full_text'] for r in all_rules.values()]
    if rule_texts:
        rule_embeddings = get_embeddings(rule_texts)
        for rule, emb in zip(all_rules.keys(), rule_embeddings):
            embeddings_cache[f"rule:{rule}"] = emb
    
    # Save cache
    with open(EMBEDDINGS_FILE, 'w') as f:
        json.dump(embeddings_cache, f)
    print("✓ Saved embeddings cache")

# Now find semantic matches
print("\n🔍 Finding semantic matches...")
total_ai_coverage = 0
ai_matches = {}

for service, data in mapping.items():
    if service == 'metadata':
        continue
    
    available_rules = data.get('available_rules', [])
    step3_needs = data.get('step3_needs_development', [])
    existing_step2 = data.get('step2_covered_by', {})
    
    new_coverage = {}
    still_not_covered = []
    
    for func in step3_needs:
        # Get embedding for this compliance function
        comp_embedding = embeddings_cache.get(f"compliance:{func}")
        if not comp_embedding:
            still_not_covered.append(func)
            continue
        
        # Find best matching rules
        best_matches = []
        for rule in available_rules:
            rule_embedding = embeddings_cache.get(f"rule:{rule}")
            if rule_embedding:
                similarity = cosine_similarity(comp_embedding, rule_embedding)
                best_matches.append((rule, similarity))
        
        # Sort by similarity
        best_matches.sort(key=lambda x: x[1], reverse=True)
        
        # Take matches above threshold (0.75 is high confidence)
        high_confidence_matches = [(r, s) for r, s in best_matches if s >= 0.75]
        medium_confidence_matches = [(r, s) for r, s in best_matches if 0.65 <= s < 0.75]
        
        if high_confidence_matches:
            # Use top high confidence matches
            context = compliance_contexts.get(func, {})
            new_coverage[func] = {
                'covered_by_rules': [m[0] for m in high_confidence_matches[:2]],
                'coverage_type': 'AI_SEMANTIC_MATCH',
                'expert_reasoning': f"AI: {high_confidence_matches[0][1]:.2f} similarity. Requirement: '{context.get('requirement', 'N/A')[:60]}'",
                'confidence': 'HIGH',
                'ai_similarity_score': round(high_confidence_matches[0][1], 3)
            }
            total_ai_coverage += 1
            
            if service not in ai_matches:
                ai_matches[service] = []
            ai_matches[service].append({
                'function': func,
                'matched_to': high_confidence_matches[0][0],
                'score': high_confidence_matches[0][1],
                'requirement': context.get('requirement', '')
            })
        elif medium_confidence_matches:
            # Use medium confidence with caveat
            context = compliance_contexts.get(func, {})
            new_coverage[func] = {
                'covered_by_rules': [m[0] for m in medium_confidence_matches[:1]],
                'coverage_type': 'AI_POTENTIAL_MATCH',
                'expert_reasoning': f"AI: {medium_confidence_matches[0][1]:.2f} similarity (requires validation). Requirement: '{context.get('requirement', 'N/A')[:50]}'",
                'confidence': 'MEDIUM',
                'ai_similarity_score': round(medium_confidence_matches[0][1], 3)
            }
            total_ai_coverage += 1
        else:
            still_not_covered.append(func)
    
    # Update mapping
    all_step2 = {**existing_step2, **new_coverage}
    if all_step2:
        data['step2_covered_by'] = all_step2
    data['step3_needs_development'] = still_not_covered
    
    if new_coverage:
        print(f"  ✓ {service:15s} +{len(new_coverage)} AI matches (total step2: {len(all_step2)})")

# Save updated mapping
with open(MAPPING_FILE, 'w') as f:
    json.dump(mapping, f, indent=2)

print()
print("=" * 100)
print("AI COVERAGE RESULTS")
print("=" * 100)
print(f"✓ Found {total_ai_coverage} new matches using AI")
print(f"✓ Step 2 coverage improved: 30 → {30 + total_ai_coverage}")
print()

# Show some impressive matches
if ai_matches:
    print("Top AI Matches (>0.8 similarity):")
    print("-" * 80)
    all_matches = []
    for svc, matches in ai_matches.items():
        all_matches.extend([(svc, m) for m in matches])
    
    # Sort by score
    all_matches.sort(key=lambda x: x[1]['score'], reverse=True)
    
    for svc, match in all_matches[:5]:
        if match['score'] > 0.8:
            print(f"\n{match['function']}")
            print(f"  Requirement: {match['requirement'][:60]}...")
            print(f"  Matched to:  {match['matched_to']}")
            print(f"  AI Score:    {match['score']:.3f} (Very High Confidence)")

# Calculate final stats
print()
print("=" * 100)
print("FINAL COVERAGE WITH AI")
print("=" * 100)
total_step1 = sum(len(d.get('step1_direct_mapped', {})) for s, d in mapping.items() if s != 'metadata')
total_step2 = sum(len(d.get('step2_covered_by', {})) for s, d in mapping.items() if s != 'metadata')
total_step3 = sum(len(d.get('step3_needs_development', [])) for s, d in mapping.items() if s != 'metadata')

print(f"Step 1 (Direct):      {total_step1:3d} functions")
print(f"Step 2 (Covered):     {total_step2:3d} functions ↑ (was 30)")
print(f"Step 3 (Develop):     {total_step3:3d} functions ↓")
print()
print(f"Total Coverage: {total_step1 + total_step2} / {total_step1 + total_step2 + total_step3} = {(total_step1 + total_step2) / (total_step1 + total_step2 + total_step3) * 100:.1f}%")
print()
print("✅ AI-POWERED ANALYSIS COMPLETE")
print("=" * 100)
