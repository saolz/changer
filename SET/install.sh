#!/bin/bash

# This script installs SET (Social-Engineer Toolkit) on Ubuntu 2022

# Update package lists
echo "Updating package lists..."
sudo apt update

# Install required dependencies
echo "Installing dependencies..."
sudo apt install -y git python3 python3-pip python3-setuptools libpython3-dev build-essential

# Clone the SET repository from GitHub
echo "Cloning SET repository..."
git clone https://github.com/trustedsec/social-engineer-toolkit.git

# Navigate into the SET directory
cd social-engineer-toolkit

# Install SET's required Python dependencies
echo "Installing Python dependencies for SET..."
sudo pip3 install -r requirements.txt

# Script completion message
echo "SET installation complete!"
echo "To run SET, navigate to the social-engineer-toolkit directory and use python3 setool.py"
