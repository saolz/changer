#!/bin/bash

# Script to install trufflehog3 using pip3

# Update package lists to ensure we have the latest information
echo "Updating package lists..."
sudo apt-get update -y

# Install pip3 if not already installed
echo "Checking if pip3 is installed..."
if ! command -v pip3 &>/dev/null; then
    echo "pip3 not found, installing pip3..."
    sudo apt-get install python3-pip -y
else
    echo "pip3 is already installed."
fi

# Install trufflehog3
echo "Installing trufflehog3..."
pip3 install trufflehog3

# Verify the installation
echo "Verifying trufflehog3 installation..."
trufflehog3 --version

echo "Installation complete."
