#!/bin/bash

# Check if Nikto is installed
if dpkg -l | grep -q nikto; then
  echo "Nikto is installed. Proceeding with uninstallation..."

  # Uninstall nikto
  sudo apt remove --purge -y nikto

  # Clean up unnecessary packages
  sudo apt autoremove -y

  # Verify if Nikto has been uninstalled
  if ! dpkg -l | grep -q nikto; then
    echo "Nikto has been successfully uninstalled."
  else
    echo "There was an issue uninstalling Nikto."
  fi
else
  echo "Nikto is not installed on this system."
fi
