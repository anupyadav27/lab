#!/usr/bin/env python3
"""
Flexible GCP Function Database Update Script

This script automatically finds the latest output files and updates the gcp_simplified_function_names.json file by:
1. Adding new functions from the latest new_functions output
2. Applying rename suggestions from the latest updated_functions output
3. Creating a backup of the original file
4. Generating an updated database with all changes

The script automatically detects the latest output files based on timestamps.
"""

import json
import os
import sys
import glob
from datetime import datetime
from pathlib import Path
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def find_latest_file(pattern: str) -> str:
    """Find the latest file matching a pattern"""
    files = glob.glob(pattern)
    if not files:
        return None
    
    # Sort by modification time (newest first)
    files.sort(key=os.path.getmtime, reverse=True)
    return files[0]

def load_json_file(file_path: str) -> list:
    """Load a JSON file and return the data"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return []
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing JSON file {file_path}: {e}")
        return []

def save_json_file(data: list, file_path: str):
    """Save data to a JSON file"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logger.info(f"Successfully saved to: {file_path}")
    except Exception as e:
        logger.error(f"Error saving file {file_path}: {e}")

def create_backup(original_file: str) -> str:
    """Create a backup of the original file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"{original_file}.backup_{timestamp}"
    
    try:
        with open(original_file, 'r', encoding='utf-8') as src:
            with open(backup_file, 'w', encoding='utf-8') as dst:
                dst.write(src.read())
        logger.info(f"Backup created: {backup_file}")
        return backup_file
    except Exception as e:
        logger.error(f"Error creating backup: {e}")
        return None

def apply_rename_suggestions(original_data: list, rename_suggestions: list) -> list:
    """Apply rename suggestions to the original data"""
    # Create a mapping of old names to new names
    rename_map = {}
    for suggestion in rename_suggestions:
        old_name = suggestion.get('old_name')
        new_name = suggestion.get('new_name')
        if old_name and new_name:
            rename_map[old_name] = new_name
    
    # Apply renames to the data
    updated_data = []
    renamed_count = 0
    
    for item in original_data:
        function_name = item.get('function_name')
        if function_name in rename_map:
            # Create a copy of the item with the new function name
            updated_item = item.copy()
            updated_item['function_name'] = rename_map[function_name]
            updated_data.append(updated_item)
            renamed_count += 1
            logger.info(f"Renamed: {function_name} -> {rename_map[function_name]}")
        else:
            updated_data.append(item)
    
    logger.info(f"Applied {renamed_count} rename suggestions")
    return updated_data

def add_new_functions(original_data: list, new_functions: list) -> list:
    """Add new functions to the original data"""
    # Get existing function names to avoid duplicates
    existing_names = set()
    for item in original_data:
        function_name = item.get('function_name')
        if function_name:
            existing_names.add(function_name)
    
    # Add new functions that don't already exist
    added_count = 0
    updated_data = original_data.copy()
    
    for new_func in new_functions:
        function_name = new_func.get('function_name')
        if function_name and function_name not in existing_names:
            # Convert new function format to match original format
            converted_func = {
                "sheet": "CIS_GKE",  # Default sheet for new functions
                "rule_id": f"CIS_GKE_{added_count + 1}",  # Generate rule ID
                "description": new_func.get('description', ''),
                "function_name": function_name,
                "service_category": new_func.get('service_category', ''),
                "confidence": 7,  # Default confidence for new functions
                "gcp_sdk_example": new_func.get('gcp_api_example', '')
            }
            updated_data.append(converted_func)
            existing_names.add(function_name)
            added_count += 1
            logger.info(f"Added new function: {function_name}")
    
    logger.info(f"Added {added_count} new functions")
    return updated_data

def main():
    """Main function to update the GCP function database"""
    print("🔄 Flexible GCP Function Database Update Script")
    print("=" * 60)
    
    # File paths
    original_file = "gcp_simplified_function_names.json"
    
    # Find latest output files
    print("🔍 Finding latest output files...")
    
    new_functions_pattern = "output/new_functions/gcp_new_functions_*.json"
    rename_functions_pattern = "output/updated_functions/gcp_rename_functions_*.json"
    
    new_functions_file = find_latest_file(new_functions_pattern)
    rename_functions_file = find_latest_file(rename_functions_pattern)
    
    if not new_functions_file:
        print(f"❌ No new functions files found matching: {new_functions_pattern}")
        sys.exit(1)
    
    if not rename_functions_file:
        print(f"❌ No rename functions files found matching: {rename_functions_pattern}")
        sys.exit(1)
    
    print(f"✅ Found new functions file: {new_functions_file}")
    print(f"✅ Found rename functions file: {rename_functions_file}")
    
    # Check if original file exists
    if not os.path.exists(original_file):
        print(f"❌ Original file not found: {original_file}")
        sys.exit(1)
    
    print("📁 Loading files...")
    
    # Load original data
    original_data = load_json_file(original_file)
    if not original_data:
        print("❌ Failed to load original data")
        sys.exit(1)
    
    print(f"✅ Loaded {len(original_data)} original functions")
    
    # Load new functions
    new_functions = load_json_file(new_functions_file)
    if not new_functions:
        print("❌ Failed to load new functions")
        sys.exit(1)
    
    print(f"✅ Loaded {len(new_functions)} new functions")
    
    # Load rename suggestions
    rename_suggestions = load_json_file(rename_functions_file)
    if not rename_suggestions:
        print("❌ Failed to load rename suggestions")
        sys.exit(1)
    
    print(f"✅ Loaded {len(rename_suggestions)} rename suggestions")
    
    # Create backup
    print("💾 Creating backup...")
    backup_file = create_backup(original_file)
    if not backup_file:
        print("❌ Failed to create backup")
        sys.exit(1)
    
    # Apply updates
    print("🔄 Applying updates...")
    
    # Step 1: Apply rename suggestions
    updated_data = apply_rename_suggestions(original_data, rename_suggestions)
    
    # Step 2: Add new functions
    final_data = add_new_functions(updated_data, new_functions)
    
    # Generate updated file name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    updated_file = f"gcp_simplified_function_names_updated_{timestamp}.json"
    
    # Save updated data
    print("💾 Saving updated database...")
    save_json_file(final_data, updated_file)
    
    # Also save as the original filename (replacing it)
    save_json_file(final_data, original_file)
    
    # Print summary
    print("\n" + "=" * 60)
    print("✅ GCP Function Database Update Complete!")
    print("=" * 60)
    print(f"Original functions: {len(original_data)}")
    print(f"New functions added: {len(new_functions)}")
    print(f"Functions renamed: {len(rename_suggestions)}")
    print(f"Total functions in updated database: {len(final_data)}")
    print(f"Backup created: {backup_file}")
    print(f"Updated database: {updated_file}")
    print(f"Original file updated: {original_file}")
    print("=" * 60)
    
    # Show file sizes
    original_size = os.path.getsize(original_file)
    backup_size = os.path.getsize(backup_file)
    print(f"\n📊 File Sizes:")
    print(f"Original (updated): {original_size:,} bytes")
    print(f"Backup: {backup_size:,} bytes")
    print(f"Size difference: {original_size - backup_size:,} bytes")

if __name__ == "__main__":
    main()
