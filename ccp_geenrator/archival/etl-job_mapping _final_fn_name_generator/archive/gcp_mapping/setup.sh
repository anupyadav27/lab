#!/bin/bash
# GCP Compliance Mapper Setup Script

echo "🚀 Setting up GCP Compliance Mapper"
echo "=================================="

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is required but not installed"
    exit 1
fi

echo "✅ pip3 found: $(pip3 --version)"

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Check if required files exist
echo "📋 Checking required files..."

if [ ! -f "gcp_simplified_function_names.json" ]; then
    echo "❌ gcp_simplified_function_names.json not found"
    echo "   Please ensure this file exists in the current directory"
    exit 1
fi

if [ ! -f "CIS_GOOGLE_CLOUD_PLATFORM_FOUNDATION_BENCHMARK_V4.0.0.json" ]; then
    echo "❌ CIS_GOOGLE_CLOUD_PLATFORM_FOUNDATION_BENCHMARK_V4.0.0.json not found"
    echo "   Please ensure this file exists in the current directory"
    exit 1
fi

echo "✅ All required files found"

# Create output directories
echo "📁 Creating output directories..."
mkdir -p output/updated_compliance
mkdir -p output/new_functions
mkdir -p output/updated_functions

echo "✅ Output directories created"

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Set your OpenAI API key in gcp_compliance_mapper.py"
echo "2. Test the mapper: python test_gcp_mapper.py"
echo "3. Or test manually: python gcp_compliance_mapper.py gcp_simplified_function_names.json CIS_GOOGLE_CLOUD_PLATFORM_FOUNDATION_BENCHMARK_V4.0.0.json --test 15"
echo ""
echo "For production use:"
echo "python gcp_compliance_mapper.py gcp_simplified_function_names.json CIS_GOOGLE_CLOUD_PLATFORM_FOUNDATION_BENCHMARK_V4.0.0.json"
