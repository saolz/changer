#!/bin/bash

# Update package list
echo "Updating package list..."
sudo apt update

# Install aircrack-ng
echo "Installing aircrack-ng..."
sudo apt install -y aircrack-ng

# Verify installation
echo "Verifying aircrack-ng installation..."
if command -v aircrack-ng &> /dev/null
then
    echo "aircrack-ng successfully installed!"
else
    echo "Error: aircrack-ng installation failed."
fi
