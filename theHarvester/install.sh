#!/bin/bash
echo "Installing theHarvester and dependencies..."
sudo apt update
sudo apt install -y theharvester
pip3 install -r components.txt
echo "Installation complete."
