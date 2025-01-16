#!/bin/bash

# Update package list
echo "Updating package list..."
sudo apt update

# Install dependencies
echo "Installing required dependencies..."
sudo apt install -y python3 python3-pip libxml2-dev libxslt1-dev zlib1g-dev

# Install Metagoofil using pip
echo "Installing Metagoofil..."
pip3 install metagoofil

# Verify installation
echo "Verifying Metagoofil installation..."
if command -v metagoofil &> /dev/null
then
    echo "Metagoofil successfully installed!"
else
    echo "Error: Metagoofil installation failed."
fi
