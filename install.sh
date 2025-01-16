#!/bin/bash

# Function to print messages
function print_message() {
    echo -e "\n\033[1;32m$1\033[0m\n"
}

# Update package list
print_message "Updating package list..."
sudo apt update -y

# Install Python 3 and pip
print_message "Installing Python 3 and pip..."
sudo apt install -y python3 python3-pip git

# Clone DNSRecon repository
print_message "Cloning DNSRecon repository..."
if [ -d "dnsrecon" ]; then
    print_message "DNSRecon directory already exists. Pulling latest changes..."
    cd dnsrecon && git pull && cd ..
else
    git clone https://github.com/darkoperator/dnsrecon.git
fi

# Navigate to DNSRecon directory
cd dnsrecon

# Install dependencies with system override
print_message "Installing dependencies with system override..."
pip3 install -r requirements.txt --break-system-packages

# Verify installation
print_message "Verifying installation..."
if python3 dnsrecon.py -h >/dev/null 2>&1; then
    print_message "DNSRecon installed successfully!"
else
    echo -e "\n\033[1;31mInstallation failed. Please check for errors.\033[0m\n"
    exit 1
fi

# Usage message
print_message "You can now run DNSRecon using:\npython3 dnsrecon.py -h"
