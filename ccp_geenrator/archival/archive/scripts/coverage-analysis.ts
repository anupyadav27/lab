#!/usr/bin/env ts-node

import * as fs from 'fs';

// Load current services from rules
const currentServices = fs.readFileSync('current_services.txt', 'utf8').trim().split('\n');

// Load all services from function list
const functionServices = fs.readFileSync('/Users/apple/Desktop/compliance_Database/Final_Compliance_aws/function_services.txt', 'utf8').trim().split('\n');

// Filter out non-AWS services and normalize names
const awsServices = functionServices.filter(service => 
  !['N/A', 'account', 'awareness_training', 'awsbackup', 'awscli', 'awslambda', 
    'disaster_recovery', 'edr', 'personnel_security', 'unmapped'].includes(service)
);

// Find missing services
const missingServices = awsServices.filter(service => !currentServices.includes(service));

// Priority services mentioned by ChatGPT
const priorityServices = [
  'accessanalyzer', 'detective', 'inspector2', 'securityhub', 'shield', 
  'wafv2', 'networkfirewall', 'elbv2', 'directconnect', 'cloudformation', 
  'stepfunctions', 'ecs', 'eks', 'emr', 'glue', 'kinesis', 'firehose', 
  'sagemaker', 'neptune', 'timestream'
];

// Categorize missing services
const priorityMissing = missingServices.filter(service => priorityServices.includes(service));
const otherMissing = missingServices.filter(service => !priorityServices.includes(service));

console.log('=== AWS Service Coverage Analysis ===\n');

console.log(`Current services in rules: ${currentServices.length}`);
console.log(`Total AWS services in function list: ${awsServices.length}`);
console.log(`Missing services: ${missingServices.length}\n`);

console.log('=== Priority Missing Services ===');
priorityMissing.forEach(service => {
  console.log(`✅ ${service}`);
});

console.log('\n=== Other Missing Services ===');
otherMissing.forEach(service => {
  console.log(`📋 ${service}`);
});

// Create coverage report
const coverageReport = {
  analysis_date: new Date().toISOString(),
  current_services_count: currentServices.length,
  total_aws_services_count: awsServices.length,
  missing_services_count: missingServices.length,
  coverage_percentage: Math.round((currentServices.length / awsServices.length) * 100),
  priority_missing_services: priorityMissing,
  other_missing_services: otherMissing,
  current_services: currentServices.sort(),
  all_aws_services: awsServices.sort()
};

fs.writeFileSync('coverage_analysis.json', JSON.stringify(coverageReport, null, 2));

console.log(`\n📊 Coverage: ${coverageReport.coverage_percentage}%`);
console.log(`📁 Detailed report saved to coverage_analysis.json`);

// Export missing services for next step
fs.writeFileSync('missing_services.txt', missingServices.join('\n'));
console.log(`📁 Missing services list saved to missing_services.txt`);
