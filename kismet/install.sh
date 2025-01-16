#!/bin/bash

# This script installs Kismet on Ubuntu using the official repository

# Add the Kismet official repository
echo "Adding the Kismet repository..."
wget -O - https://www.kismetwireless.net/repos/kismet-release.gpg.key | gpg --dearmor > kismet.gpg
sudo mv kismet.gpg /etc/apt/trusted.gpg.d/
echo "deb https://www.kismetwireless.net/repos/apt/release/ubuntu/ $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/kismet.list

# Update package lists
echo "Updating package lists..."
sudo apt update

# Install Kismet
echo "Installing Kismet..."
sudo apt install -y kismet

# Verify installation
echo "Verifying installation..."
kismet --version

# Completion message
echo "Kismet installation is complete!"
