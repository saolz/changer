#!/bin/bash

# Script to uninstall URLextractor and clean up
echo "Uninstalling URLextractor..."

# Remove the cloned repository directory
if [ -d "URLExtractor" ]; then
    rm -rf URLExtractor
    echo "Repository directory removed."
else
    echo "Repository directory not found!"
fi

# Uninstall dependencies listed in requirements.txt
if [ -f "requirements.txt" ]; then
    while read -r dependency; do
        pip3 uninstall -y "$dependency"
    done < requirements.txt
    echo "Dependencies uninstalled."
else
    echo "requirements.txt not found. Dependencies might remain installed."
fi

echo "URLextractor uninstalled successfully."
