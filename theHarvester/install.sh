#!/bin/bash

echo "Installing theHarvester from GitHub..."

# Install dependencies
sudo apt update
sudo apt install -y git python3 python3-pip

# Clone theHarvester repository
git clone https://github.com/laramies/theHarvester.git ~/theHarvester

# Navigate to the directory
cd ~/theHarvester || { echo "Failed to navigate to theHarvester directory"; exit 1; }

# Install Python dependencies
pip3 install -r requirements.txt

# Create a symlink for easier access
sudo ln -sf ~/theHarvester/theHarvester.py /usr/local/bin/theHarvester

echo "Installation complete. You can now use 'theHarvester'."
