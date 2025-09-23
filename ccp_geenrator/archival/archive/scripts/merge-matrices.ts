#!/usr/bin/env ts-node

import * as fs from 'fs';

// Load original matrix
const originalMatrix = JSON.parse(fs.readFileSync('matrices/aws_fixed.json', 'utf8'));

// Load new matrix with additional services
const newMatrix = JSON.parse(fs.readFileSync('matrices/aws_matrix_v2.json', 'utf8'));

console.log('Merging matrices to preserve all original mappings...');

// Start with original matrix to preserve all existing mappings
const mergedMatrix = { ...originalMatrix };

// Add new services from the expanded matrix
Object.entries(newMatrix).forEach(([assertionFamily, tiers]) => {
  if (!mergedMatrix[assertionFamily]) {
    mergedMatrix[assertionFamily] = {};
  }
  
  Object.entries(tiers as any).forEach(([tier, entries]) => {
    if (!mergedMatrix[assertionFamily][tier]) {
      mergedMatrix[assertionFamily][tier] = [];
    }
    
    // Add new entries that don't already exist
    (entries as any[]).forEach((newEntry: any) => {
      const exists = mergedMatrix[assertionFamily][tier].some((existingEntry: any) => 
        existingEntry.service === newEntry.service && 
        existingEntry.adapter === newEntry.adapter
      );
      
      if (!exists) {
        mergedMatrix[assertionFamily][tier].push(newEntry);
      }
    });
  });
});

// Save merged matrix
fs.writeFileSync('matrices/aws_matrix_v2_complete.json', JSON.stringify(mergedMatrix, null, 2));

// Count entries
let totalEntries = 0;
Object.values(mergedMatrix).forEach((family: any) => {
  Object.values(family).forEach((tier: any) => {
    totalEntries += tier.length;
  });
});

console.log(`✅ Merged matrices successfully`);
console.log(`📊 Original assertion families: ${Object.keys(originalMatrix).length}`);
console.log(`📊 New assertion families: ${Object.keys(newMatrix).length}`);
console.log(`📊 Merged assertion families: ${Object.keys(mergedMatrix).length}`);
console.log(`📊 Total entries: ${totalEntries}`);
console.log(`📁 Saved to matrices/aws_matrix_v2_complete.json`);
