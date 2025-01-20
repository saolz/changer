#!/bin/bash

# Update the package list
echo "Updating package list..."
sudo apt update

# Install nikto
echo "Installing Nikto..."
sudo apt install -y nikto

# Verify installation
echo "Verifying Nikto installation..."
nikto -Version

echo "Nikto installation complete!"
