#!/bin/bash

# This script installs Kismet on Ubuntu by building from the official GitHub source

# Update package lists
echo "Updating package lists..."
sudo apt update

# Install required dependencies
echo "Installing required dependencies..."
sudo apt install -y build-essential git libmicrohttpd-dev libnl-3-dev libnl-genl-3-dev \
  libcap-dev pkg-config libpcap-dev libssl-dev python3 python3-setuptools python3-dev python3-pip

# Clone the Kismet GitHub repository
echo "Cloning the Kismet repository..."
if [ -d "kismet" ]; then
  echo "Kismet directory already exists. Pulling latest changes..."
  cd kismet && git pull && cd ..
else
  git clone https://github.com/kismetwireless/kismet.git
fi

# Navigate to the Kismet directory
cd kismet

# Build and install Kismet
echo "Building Kismet..."
./configure
make -j$(nproc)
sudo make install

# Verify installation
echo "Verifying installation..."
if command -v kismet &> /dev/null; then
  kismet --version
  echo "Kismet installation is complete!"
else
  echo "Error: Kismet installation failed."
fi
