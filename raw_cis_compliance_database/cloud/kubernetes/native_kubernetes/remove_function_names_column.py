#!/usr/bin/env python3
"""
Remove the function_names column from the CSV file
"""

import csv
import os

def remove_function_names_column(input_file, output_file):
    """Remove function_names column from CSV file"""
    
    print(f"Reading input file: {input_file}")
    
    # Read the original CSV
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        
        # Remove function_names column if it exists
        if 'function_names' in fieldnames:
            fieldnames.remove('function_names')
            print(f"Removed 'function_names' column from fieldnames")
        else:
            print(f"'function_names' column not found in input file")
            return
        
        # Read all rows
        rows = list(reader)
        print(f"Read {len(rows)} rows")
    
    # Write the cleaned CSV
    print(f"Writing output file: {output_file}")
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for row in rows:
            # Remove function_names from each row
            if 'function_names' in row:
                del row['function_names']
            writer.writerow(row)
    
    print(f"Successfully removed 'function_names' column")
    print(f"Output saved to: {output_file}")
    
    # Show the new fieldnames
    print(f"\nNew fieldnames: {fieldnames}")

def main():
    input_file = '/Users/apple/Desktop/compliance_Database/raw_compliance_database/cloud/kubernetes/native_kubernetes/combined_kubernetes_compliance.csv'
    output_file = '/Users/apple/Desktop/compliance_Database/raw_compliance_database/cloud/kubernetes/native_kubernetes/combined_kubernetes_compliance_cleaned.csv'
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file {input_file} not found")
        return
    
    # Remove function_names column
    remove_function_names_column(input_file, output_file)
    
    # Replace original file with cleaned version
    print(f"\nReplacing original file with cleaned version...")
    os.replace(output_file, input_file)
    print(f"Original file updated successfully!")

if __name__ == "__main__":
    main()

