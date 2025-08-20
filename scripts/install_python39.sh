#!/bin/bash

# Script to install Python 3.9 for XReason development
# This ensures compatibility with pydatalog

echo "🐍 Installing Python 3.9 for XReason development..."

# Check if Python 3.9 is already installed
if command -v python3.9 &> /dev/null; then
    echo "✅ Python 3.9 is already installed"
    python3.9 --version
    exit 0
fi

# Detect OS and install Python 3.9
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    echo "📦 Installing Python 3.9 on macOS..."
    
    if command -v brew &> /dev/null; then
        echo "Using Homebrew to install Python 3.9..."
        brew install python@3.9
        echo "✅ Python 3.9 installed via Homebrew"
    else
        echo "❌ Homebrew not found. Please install Homebrew first:"
        echo "   /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
        exit 1
    fi
    
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    echo "📦 Installing Python 3.9 on Linux..."
    
    if command -v apt-get &> /dev/null; then
        # Ubuntu/Debian
        sudo apt-get update
        sudo apt-get install -y python3.9 python3.9-venv python3.9-dev
        echo "✅ Python 3.9 installed via apt-get"
    elif command -v yum &> /dev/null; then
        # CentOS/RHEL
        sudo yum install -y python39 python39-devel
        echo "✅ Python 3.9 installed via yum"
    else
        echo "❌ Package manager not supported. Please install Python 3.9 manually."
        exit 1
    fi
    
else
    echo "❌ Unsupported OS: $OSTYPE"
    echo "Please install Python 3.9 manually from https://www.python.org/downloads/"
    exit 1
fi

echo ""
echo "🎉 Python 3.9 installation complete!"
echo ""
echo "Next steps:"
echo "1. Create a virtual environment: python3.9 -m venv venv"
echo "2. Activate it: source venv/bin/activate"
echo "3. Install requirements: pip install -r requirements.txt"
echo ""
echo "Or run the setup script: ./scripts/setup.sh"

