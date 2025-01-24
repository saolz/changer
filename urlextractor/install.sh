#!/bin/bash

# Script to install URLextractor and its dependencies
echo "Cloning URLextractor repository..."
git clone https://github.com/The404Hacking/URLExtractor || { echo "Failed to clone repository!"; exit 1; }

# Move into the cloned repository directory
cd URLExtractor || { echo "Failed to enter repository directory!"; exit 1; }

# Install dependencies
echo "Installing dependencies from requirements.txt..."
pip3 install -r requirements.txt || { echo "Failed to install dependencies!"; exit 1; }

echo "URLextractor installed successfully."
