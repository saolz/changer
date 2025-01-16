#!/bin/bash

# This script installs Kismet on Ubuntu using sudo apt install

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
