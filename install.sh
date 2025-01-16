#!/bin/bash

# This script installs dnsrecon on Ubuntu 2022

# Update package lists
echo "Updating package lists..."
sudo apt update

# Install dnsrecon
echo "Installing dnsrecon..."
sudo apt install -y dnsrecon

# Verify installation
echo "Verifying installation..."
dnsrecon --version

# Script completion message
echo "dnsrecon installation complete!"
