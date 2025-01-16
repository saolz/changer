#!/bin/bash

# Update package list
echo "Adding Kismet GPG key..."
wget -O - https://www.kismetwireless.net/repos/kismet-release.gpg.key --quiet | gpg --dearmor | sudo tee /usr/share/keyrings/kismet-archive-keyring.gpg >/dev/null

# Add the Kismet repository
echo "Adding Kismet repository..."
echo 'deb [signed-by=/usr/share/keyrings/kismet-archive-keyring.gpg] https://www.kismetwireless.net/repos/apt/release/jammy jammy main' | sudo tee /etc/apt/sources.list.d/kismet.list >/dev/null

# Update the package list
echo "Updating package list..."
sudo apt update

# Install Kismet
echo "Installing Kismet..."
sudo apt install -y kismet

echo "Kismet installation completed!"
