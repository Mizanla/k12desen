#!/bin/bash

# Configuration - Using the exact Raw GitHub path
BASE_URL="https://raw.githubusercontent.com/Mizanla/k12desen/main"

echo -e "\033[1;36m[K12] Starting Installation...\033[0m"

# 1. Setup Persistent Directory
sudo mkdir -p /var/lib/k12
sudo chmod 777 /var/lib/k12

# 2. Download Components
echo -e "\033[1;36m[K12] Downloading Engine...\033[0m"
sudo curl -sSL "$BASE_URL/k12_engine.py" -o /usr/local/bin/k12_engine.py

echo -e "\033[1;36m[K12] Downloading Wrapper...\033[0m"
sudo curl -sSL "$BASE_URL/k12" -o /usr/local/bin/k12

# 3. Set Permissions
sudo chmod +x /usr/local/bin/k12_engine.py
sudo chmod +x /usr/local/bin/k12

# 4. Install Dependencies
echo -e "\033[1;36m[K12] Installing Python dependencies...\033[0m"
pip3 install psutil colorama --break-system-packages 2>/dev/null || pip3 install psutil colorama

echo -e "\033[1;32m------------------------------------------"
echo -e "K12 DEŞEN v3.0 INSTALLED SUCCESSFULLY!"
echo -e "Run 'k12' to start."
echo -e "------------------------------------------\033[0m"
