#!/bin/bash

# This script installs fierce on Ubuntu 2022

# Update package lists
echo "Updating package lists..."
sudo apt update

# Install dependencies
echo "Installing dependencies..."
sudo apt install -y libnet-ssleay-perl libwww-perl libipc-run-perl

# Install fierce
echo "Installing fierce..."
sudo apt install -y fierce

# Verify installation
echo "Verifying installation..."
fierce --version

# Script completion message
echo "fierce installation complete!"
