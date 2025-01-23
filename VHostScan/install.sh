#!/bin/bash

# Install script for VHostScan
echo "Cloning VHostScan repository..."
git clone https://github.com/codingo/VHostScan || { echo "Failed to clone repository"; exit 1; }

echo "Changing directory to VHostScan..."
cd VHostScan || { echo "Failed to navigate to VHostScan directory"; exit 1; }

echo "Installing VHostScan..."
sudo python3 setup.py install || { echo "Failed to install VHostScan"; exit 1; }

echo "VHostScan installation completed."
