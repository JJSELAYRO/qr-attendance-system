#!/bin/bash

# QR Attendance System - APK Build Script
# Run this script to build the Android APK

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  QR Attendance System - APK Builder    ${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Check if buildozer is installed
if ! command -v buildozer &> /dev/null; then
    echo -e "${RED}Error: buildozer is not installed!${NC}"
    echo "Install it with: pip install buildozer"
    exit 1
fi

# Navigate to frontend directory
cd ../frontend

# Clean previous builds
echo -e "${YELLOW}Cleaning previous builds...${NC}"
buildozer android clean

# Build APK
echo -e "${YELLOW}Building APK...${NC}"
echo -e "${YELLOW}This may take 10-30 minutes on first run...${NC}"
echo ""

buildozer android debug

# Check if build was successful
if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}  Build Successful!                     ${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""
    echo "APK location: ./bin/"
    ls -lh ./bin/*.apk 2>/dev/null || echo "Check the bin directory"
    echo ""
    echo "To install on device:"
    echo "  buildozer android deploy run"
else
    echo ""
    echo -e "${RED}========================================${NC}"
    echo -e "${RED}  Build Failed!                         ${NC}"
    echo -e "${RED}========================================${NC}"
    echo ""
    echo "Check the error messages above."
    echo "Common issues:"
    echo "  - Missing dependencies"
    echo "  - Java not installed"
    echo "  - Android SDK not configured"
fi
