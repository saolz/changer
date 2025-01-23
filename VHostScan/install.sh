#!/bin/bash

# Install script for VHostScan
echo "Cloning VHostScan repository..."
git clone https://github.com/codingo/VHostScan || { echo "Failed to clone repository"; exit 1; }

echo "Changing directory to VHostScan..."
cd VHostScan || { echo "Failed to navigate to VHostScan directory"; exit 1; }

echo "Installing required dependencies..."
# Ensure pip is up-to-date
pip3 install --upgrade pip || { echo "Failed to upgrade pip"; exit 1; }

# Install the required version of numpy
pip3 install "numpy>=1.22.4" || { echo "Failed to install numpy"; exit 1; }

echo "Installing VHostScan..."
sudo python3 setup.py install || { echo "Failed to install VHostScan"; exit 1; }

echo "VHostScan installation completed successfully."
