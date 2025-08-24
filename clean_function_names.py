#!/usr/bin/env python3
import json
import sys
import os

def clean_function_names_recursive(obj):
    """
    Recursively clean function_names arrays in any nested structure
    """
    cleaned_count = 0
    
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == 'function_names' and isinstance(value, list):
                obj[key] = []
                cleaned_count += 1
            elif isinstance(value, (dict, list)):
                cleaned_count += clean_function_names_recursive(value)
    elif isinstance(obj, list):
        for item in obj:
            if isinstance(item, (dict, list)):
                cleaned_count += clean_function_names_recursive(item)
    
    return cleaned_count

def clean_function_names(input_file, output_file):
    """
    Remove function names from sections while keeping function_names arrays empty
    """
    print(f"Reading {input_file}...")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"Processing file structure...")
    
    # Clean function_names recursively
    cleaned_count = clean_function_names_recursive(data)
    
    print(f"Cleaned {cleaned_count} function_names arrays")
    
    # Write the cleaned data back
    print(f"Writing cleaned data to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print("Done!")

def process_pci_files():
    """
    Process both PCI files in the pci folder
    """
    pci_folder = "etl-job_mapping _final_fn_name_generator/pci"
    
    # List of PCI files to process
    pci_files = [
        "PCI-Secure-Software-Standard-v1_2_1.json",
        "PCI-DSS-v4_0_1 copy.json"
    ]
    
    for filename in pci_files:
        input_file = os.path.join(pci_folder, filename)
        output_file = os.path.join(pci_folder, f"{os.path.splitext(filename)[0]}_cleaned.json")
        
        if os.path.exists(input_file):
            print(f"\n{'='*50}")
            print(f"Processing: {filename}")
            print(f"{'='*50}")
            try:
                clean_function_names(input_file, output_file)
                # Replace original with cleaned version
                os.replace(output_file, input_file)
                print(f"✓ Replaced original file: {filename}")
            except Exception as e:
                print(f"✗ Error processing {filename}: {e}")
        else:
            print(f"✗ File not found: {input_file}")

if __name__ == "__main__":
    try:
        process_pci_files()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
