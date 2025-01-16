#!/bin/bash

# This script uninstalls fierce from Ubuntu 2022

# Uninstall fierce
echo "Uninstalling fierce..."
sudo apt remove --purge -y fierce

# Clean up unnecessary packages
echo "Removing unnecessary packages..."
sudo apt autoremove -y

# Verify uninstallation
echo "Verifying uninstallation..."
which fierce

# Script completion message
echo "fierce has been uninstalled!"

