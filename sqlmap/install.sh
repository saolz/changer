#!/bin/bash

# Update package list
echo "Updating package list..."
sudo apt update

# Install sqlmap
echo "Installing sqlmap..."
sudo apt install -y sqlmap

# Verify installation
echo "Verifying sqlmap installation..."
if command -v sqlmap &> /dev/null
then
    echo "sqlmap successfully installed!"
else
    echo "Error: sqlmap installation failed."
fi
