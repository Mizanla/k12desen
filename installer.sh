# The correct RAW path for your specific repo
BASE_URL="https://raw.githubusercontent.com/Mizanla/k12desen"

echo -e "Downloading K12 Engine..."
sudo curl -sSL "$BASE_URL/k12_engine.py" -o /usr/local/bin/k12_engine.py

echo -e "Downloading K12 Wrapper..."
sudo curl -sSL "$BASE_URL/k12" -o /usr/local/bin/k12

# Permissions
sudo chmod +x /usr/local/bin/k12_engine.py
sudo chmod +x /usr/local/bin/k12
