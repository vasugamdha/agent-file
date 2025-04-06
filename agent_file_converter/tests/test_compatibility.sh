#!/bin/bash
# Test Compatibility Script
# This script tests the compatibility of converted agent files with LangChain and AutoGen

# Set up colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Setting up test environment...${NC}"

# Set paths for parent directory
PARENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC_DIR="${PARENT_DIR}/src"
TESTS_DIR="${PARENT_DIR}/tests"

# Create and activate virtual environment
if [ -d "test_venv" ]; then
    echo "Using existing virtual environment"
else
    echo "Creating virtual environment..."
    python3 -m venv test_venv
fi

# Activate virtual environment
source test_venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install langchain langchain-openai pyautogen

# Run example.py to generate test files
echo -e "\n${YELLOW}Running example.py to generate test files...${NC}"
python3 example.py

# Run LangChain compatibility test
echo -e "\n${YELLOW}Running LangChain compatibility test...${NC}"
python test_langchain_compatibility.py
LANGCHAIN_COMPAT_RESULT=$?

# Run AutoGen compatibility test
echo -e "\n${YELLOW}Running AutoGen compatibility test...${NC}"
python3 test_autogen_compatibility.py
AUTOGEN_COMPAT_RESULT=$?

# Run LangChain functional test
echo -e "\n${YELLOW}Running LangChain functional test...${NC}"
python3 test_langchain_functional.py
LANGCHAIN_FUNC_RESULT=$?

# Run AutoGen functional test
echo -e "\n${YELLOW}Running AutoGen functional test...${NC}"
python3 test_autogen_functional.py
AUTOGEN_FUNC_RESULT=$?

# Summary of results
echo -e "\n${YELLOW}Test Results Summary:${NC}"
if [ $LANGCHAIN_COMPAT_RESULT -eq 0 ]; then
    echo -e "${GREEN}✓ LangChain Compatibility Test: PASSED${NC}"
else
    echo -e "${RED}✗ LangChain Compatibility Test: FAILED${NC}"
fi

if [ $AUTOGEN_COMPAT_RESULT -eq 0 ]; then
    echo -e "${GREEN}✓ AutoGen Compatibility Test: PASSED${NC}"
else
    echo -e "${RED}✗ AutoGen Compatibility Test: FAILED${NC}"
fi

if [ $LANGCHAIN_FUNC_RESULT -eq 0 ]; then
    echo -e "${GREEN}✓ LangChain Functional Test: PASSED${NC}"
else
    echo -e "${RED}✗ LangChain Functional Test: FAILED${NC}"
fi

if [ $AUTOGEN_FUNC_RESULT -eq 0 ]; then
    echo -e "${GREEN}✓ AutoGen Functional Test: PASSED${NC}"
else
    echo -e "${RED}✗ AutoGen Functional Test: FAILED${NC}"
fi

# Overall result
if [ $LANGCHAIN_COMPAT_RESULT -eq 0 ] && [ $AUTOGEN_COMPAT_RESULT -eq 0 ] && [ $LANGCHAIN_FUNC_RESULT -eq 0 ] && [ $AUTOGEN_FUNC_RESULT -eq 0 ]; then
    echo -e "\n${GREEN}All tests passed! The agent file converter is working correctly.${NC}"
    OVERALL=0
else
    echo -e "\n${RED}Some tests failed. Please check the output for details.${NC}"
    OVERALL=1
fi

# Deactivate virtual environment
deactivate

echo -e "\n${YELLOW}Tests completed. Virtual environment deactivated.${NC}"
exit $OVERALL 