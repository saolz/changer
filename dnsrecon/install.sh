#!/bin/bash

# This script installs dnsrecon on Ubuntu using sudo apt install

# Update package lists
echo "Updating package lists..."
sudo apt update

# Install dnsrecon
echo "Installing dnsrecon..."
sudo apt install -y dnsrecon

# Verify installation
echo "Verifying installation..."
dnsrecon --version

# Completion message
echo "dnsrecon installation is complete!"
