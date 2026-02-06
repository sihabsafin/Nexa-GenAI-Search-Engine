#!/bin/bash

# Nexa Search - Easy Run Script
# This script handles virtual environment and launches the app

echo "🔍 Starting Nexa Search..."
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}⚠️  Virtual environment not found. Creating one...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if requirements are installed
if ! python -c "import streamlit" &> /dev/null; then
    echo -e "${YELLOW}⚠️  Dependencies not found. Installing...${NC}"
    pip install -r requirements.txt
    echo -e "${GREEN}✓ Dependencies installed${NC}"
fi

# Check for API key
if [ ! -f ".env" ]; then
    echo -e "${RED}❌ Error: .env file not found${NC}"
    echo -e "${YELLOW}Please copy .env.example to .env and add your Groq API key${NC}"
    echo ""
    echo "Run: cp .env.example .env"
    echo "Then edit .env and add your GROQ_API_KEY"
    exit 1
fi

# Check if API key is set
if grep -q "your_groq_api_key_here" .env; then
    echo -e "${RED}❌ Error: Please set your GROQ_API_KEY in .env file${NC}"
    echo -e "${YELLOW}Edit .env and replace 'your_groq_api_key_here' with your actual key${NC}"
    exit 1
fi

# Launch the app
echo -e "${GREEN}✓ Starting Nexa Search...${NC}"
echo ""
streamlit run app.py
