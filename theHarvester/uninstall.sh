#!/bin/bash
echo "Removing theHarvester and dependencies..."
sudo apt remove -y theharvester
pip3 uninstall -y $(cat components.txt)
echo "Uninstallation complete."
