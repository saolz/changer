#!/bin/bash

# Uninstall sqlmap
echo "Uninstalling sqlmap..."
sudo apt remove --purge -y sqlmap

# Clean up any unused packages
echo "Cleaning up unused packages..."
sudo apt autoremove -y

# Verify uninstallation
echo "Verifying sqlmap uninstallation..."
if ! command -v sqlmap &> /dev/null
then
    echo "sqlmap successfully uninstalled!"
else
    echo "Error: sqlmap uninstallation failed."
fi
