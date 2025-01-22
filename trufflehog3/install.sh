#!/bin/bash

# Define the installation directory
INSTALL_DIR="/usr/local/bin"

# Download and execute the official TruffleHog installation script
curl -sSfL https://raw.githubusercontent.com/trufflesecurity/trufflehog/main/scripts/install.sh | sh -s -- -b "$INSTALL_DIR"

# Verify the installation
if command -v trufflehog &> /dev/null; then
    echo "TruffleHog has been installed successfully."
    trufflehog --version
else
    echo "Installation failed. Please check for errors and try again."
    exit 1
fi
