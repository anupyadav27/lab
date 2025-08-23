#!/usr/bin/env python3
"""
Simple test runner for GCP Compliance Mapper

This script simply runs the main mapper in test mode to validate functionality.
"""

import os
import sys
import subprocess

def main():
    """Main function"""
    print("🧪 GCP Compliance Mapper Test Runner")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("gcp_compliance_mapper.py"):
        print("❌ Please run this script from the gcp_mapping directory")
        print("   cd etl-job/gcp_mapping")
        sys.exit(1)
    
    # Check if required files exist
    gcp_file = "gcp_simplified_function_names.json"
    compliance_file = "CIS_GOOGLE_CLOUD_PLATFORM_FOUNDATION_BENCHMARK_V4.0.0.json"
    
    if not os.path.exists(gcp_file):
        print(f"❌ GCP functions file not found: {gcp_file}")
        sys.exit(1)
    
    if not os.path.exists(compliance_file):
        print(f"❌ Compliance file not found: {compliance_file}")
        sys.exit(1)
    
    print(f"✅ Found required files:")
    print(f"   - {gcp_file}")
    print(f"   - {compliance_file}")
    
    print(f"\n🚀 Running GCP compliance mapper in test mode...")
    print(f"   This will process the first 15 compliance items for validation")
    
    # Run the main mapper in test mode
    try:
        cmd = [sys.executable, "gcp_compliance_mapper.py", gcp_file, compliance_file, "--test", "15"]
        result = subprocess.run(cmd, check=True)
        
        print(f"\n✅ Test completed successfully!")
        print(f"\n📋 Next steps:")
        print(f"   1. Review the mapping results in output/ directory")
        print(f"   2. Validate function suggestions and naming quality")
        print(f"   3. If satisfied, run production mode:")
        print(f"      python gcp_compliance_mapper.py {gcp_file} {compliance_file}")
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Test failed with exit code: {e.returncode}")
        print(f"   Check the logs for error details")
        sys.exit(1)
    except FileNotFoundError:
        print(f"\n❌ Python executable not found")
        sys.exit(1)

if __name__ == "__main__":
    main()
