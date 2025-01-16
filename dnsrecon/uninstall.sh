#!/bin/bash

# This script uninstalls dnsrecon from Ubuntu 2022

# Uninstall dnsrecon
echo "Uninstalling dnsrecon..."
sudo apt remove --purge -y dnsrecon

# Clean up unnecessary packages
echo "Removing unnecessary packages..."
sudo apt autoremove -y

# Verify uninstallation
echo "Verifying uninstallation..."
which dnsrecon

# Script completion message
echo "dnsrecon has been uninstalled!"
