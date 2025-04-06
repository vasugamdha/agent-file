#!/bin/bash
# Cleanup Script
# This script cleans up temporary files before running tests

# Set up colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Cleaning up temporary files...${NC}"

# Set paths for parent directory
PARENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Save current directory
CURRENT_DIR=$(pwd)

# Change to parent directory
cd "${PARENT_DIR}"

# Remove temporary JSON files
echo "Removing temporary JSON files..."
rm -f example_*.json
rm -f token_test_*.json
rm -f compare_*.json
rm -f *.langchain.json
rm -f *.autogen.json
rm -f memgpt_agent.langchain.json
rm -f customer_service.autogen.json

# Remove temporary virtual environment
echo "Removing temporary virtual environment..."
rm -rf test_venv

# Return to original directory
cd "${CURRENT_DIR}"

echo -e "${GREEN}Cleanup completed.${NC}" 