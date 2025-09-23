import pandas as pd
import os

# List of CSV files to combine
csv_files = [
    'azure_compliance_programs.csv',
    'gcp_compliance_programs.csv', 
    'k8s_compliance_programs.csv',
    'aws_compliance_programs.csv'
]

# Read and combine all CSV files
combined_data = []
for file in csv_files:
    if os.path.exists(file):
        df = pd.read_csv(file)
        combined_data.append(df)
        print(f"Added {len(df)} records from {file}")
    else:
        print(f"Warning: {file} not found")

# Combine all dataframes
if combined_data:
    final_df = pd.concat(combined_data, ignore_index=True)
    
    # Write combined CSV
    final_df.to_csv('combined_compliance_programs.csv', index=False)
    print(f"\nCreated combined_compliance_programs.csv with {len(final_df)} total records")
    print(f"Breakdown by provider:")
    print(final_df['provider'].value_counts())
else:
    print("No CSV files found to combine")
