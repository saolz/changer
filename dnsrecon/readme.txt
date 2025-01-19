#example command
python3 script.py -u 001 -d example.com


# Components.txt
# This file lists all the Python libraries and tools required to run the Tool Script.

# Required Python Libraries
argparse==1.4.0       # For parsing command-line arguments
datetime==5.1         # For handling date and time
pytz==2023.3          # For timezone management
os                    # For file system operations
sys                   # For system-specific parameters and functions
subprocess            # For running shell commands
time                  # For generating timestamps
csv                   # For creating CSV outputs
json                  # For creating JSON outputs

# System Dependencies
dnsrecon              # Tool for DNS reconnaissance (ensure it is installed on the system via apt or pip)
