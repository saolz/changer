# install.sh
#!/bin/bash

echo "Installing Social Engineering Toolkit (SET) and dependencies..."

# Update package list
sudo apt update

# Install SET
sudo apt install -y setoolkit

# Install Python dependencies
if [ -f components.txt ]; then
    pip3 install -r components.txt
fi

echo "Installation complete."
