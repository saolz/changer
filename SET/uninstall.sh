#!/bin/bash

# This script uninstalls SET (Social-Engineer Toolkit) from Ubuntu 2022

# Navigate to the SET directory (if exists)
if [ -d "social-engineer-toolkit" ]; then
    echo "Removing SET directory..."
    rm -rf social-engineer-toolkit
else
    echo "SET directory not found. Skipping removal."
fi

# Remove dependencies installed for SET
echo "Removing dependencies..."
sudo apt remove --purge -y git python3 python3-pip python3-setuptools libpython3-dev build-essential

# Clean up unnecessary packages
echo "Removing unnecessary packages..."
sudo apt autoremove -y

# Verify removal
echo "Verifying removal..."
which setool.py
which set

# Script completion message
echo "SET has been uninstalled!"
