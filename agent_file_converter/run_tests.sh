#!/bin/bash
# Master Test Script
# This script runs cleanup and then the compatibility tests

# Set up colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Exit on error
set -e

echo -e "${YELLOW}Starting test process...${NC}"

# Set paths 
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TESTS_DIR="${SCRIPT_DIR}/tests"

# Check if we're in the right directory
if [[ ! -d "${TESTS_DIR}" ]]; then
    echo -e "${RED}Error: Tests directory not found. Make sure you're running this script from the agent_file_converter directory.${NC}"
    exit 1
fi

# Run cleanup first
echo "Running cleanup..."
bash "${TESTS_DIR}/cleanup.sh"

# Run compatibility tests
echo -e "\n${YELLOW}Running compatibility tests...${NC}"
bash "${TESTS_DIR}/test_compatibility.sh"
TEST_RESULT=$?

# Report final result
if [ $TEST_RESULT -eq 0 ]; then
    echo -e "\n${GREEN}All tests passed! The agent file converter is working correctly.${NC}"
    exit 0
else
    echo -e "\n${RED}Some tests failed. Please check the output above for details.${NC}"
    exit 1
fi 