#!/bin/bash

# Uninstall aircrack-ng
echo "Uninstalling aircrack-ng..."
sudo apt remove --purge -y aircrack-ng

# Clean up any unused packages
echo "Cleaning up unused packages..."
sudo apt autoremove -y

# Verify uninstallation
echo "Verifying aircrack-ng uninstallation..."
if ! command -v aircrack-ng &> /dev/null
then
    echo "aircrack-ng successfully uninstalled!"
else
    echo "Error: aircrack-ng uninstallation failed."
fi
