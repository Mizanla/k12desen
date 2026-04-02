#!/bin/bash

# Colors for the installer
CYAN='\033[1;36m'
RED='\033[1;31m'
GREEN='\033[1;32m'
NC='\033[0m'

echo -e "${CYAN}[K12] Starting Installation...${NC}"

# 1. Check for Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: python3 is not installed.${NC}"
    exit 1
fi

# 2. Install Python Dependencies
echo -e "${CYAN}[K12] Installing dependencies (psutil, colorama)...${NC}"
pip3 install psutil colorama --break-system-packages 2>/dev/null || pip3 install psutil colorama

# 3. Create Persistent Storage Directory
echo -e "${CYAN}[K12] Setting up /var/lib/k12...${NC}"
sudo mkdir -p /var/lib/k12
sudo chmod 777 /var/lib/k12

# 4. Download files from GitHub
# Replace 'mizanla' with your actual username if different
REPO_URL="https://raw.githubusercontent.com/mizanla/k12-desen/main"

echo -e "${CYAN}[K12] Downloading Engine and Wrapper...${NC}"
sudo curl -sSL "$REPO_URL/k12_engine.py" -o /usr/local/bin/k12_engine.py
sudo curl -sSL "$REPO_URL/k12" -o /usr/local/bin/k12

# 5. Set Permissions
sudo chmod +x /usr/local/bin/k12_engine.py
sudo chmod +x /usr/local/bin/k12

echo -e "${GREEN}------------------------------------------"
echo -e "K12 DEŞEN v3.0 successfully installed!"
echo -e "Usage: k12 (Kill Mode) or k12 -s (Suspend Mode)"
echo -e "------------------------------------------${NC}"
