#!/bin/bash

# Script to uninstall trufflehog3 using pip3

# Uninstall trufflehog3
echo "Uninstalling trufflehog3..."
pip3 uninstall -y trufflehog3

# Verify uninstallation
echo "Verifying uninstallation..."
if ! command -v trufflehog3 &>/dev/null; then
    echo "trufflehog3 has been successfully uninstalled."
else
    echo "Failed to uninstall trufflehog3."
fi

echo "Uninstallation complete."
