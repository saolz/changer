#!/bin/bash

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Array to track installed tools
installed_tools=()
failed_tools=()

# Update package lists
sudo apt update -y && sudo apt full-upgrade -y

# Install common tools
TOOLS=(
    "nmap" "netcat" "whatweb" "recon-ng" "psmisc"
    "john" "hashcat" "hydra" "crackmapexec"
    "burpsuite" "owasp-zap" "nikto" "wfuzz"
    "wireshark" "tshark" "sleuthkit" "exiftool"
    "bettercap" "proxychains" "ettercap-text-only"
)

for tool in "${TOOLS[@]}"; do
    if command_exists "$tool"; then
        installed_tools+=("$tool")
    else
        if sudo apt install -y "$tool"; then
            installed_tools+=("$tool")
        else
            failed_tools+=("$tool")
        fi
    fi
done

# Install Burp Suite
if command_exists "burpsuite"; then
    installed_tools+=("burpsuite")
else
    echo "Installing Burp Suite..."
    wget -O burpsuite.sh "https://portswigger-cdn.net/burp/releases/download?product=community&version=latest&type=Linux"
    chmod +x burpsuite.sh && ./burpsuite.sh
    if command_exists "burpsuite"; then
        installed_tools+=("burpsuite")
    else
        failed_tools+=("burpsuite")
    fi
fi

# Install OWASP ZAP
if command_exists "zaproxy"; then
    installed_tools+=("owasp-zap")
else
    echo "Installing OWASP ZAP..."
    wget -O zap.tar.gz "https://github.com/zaproxy/zaproxy/releases/latest/download/ZAP_2_13_0_Linux.tar.gz"
    tar -xvzf zap.tar.gz -C /opt/
    ln -s /opt/ZAP_2_13_0/zap.sh /usr/local/bin/zaproxy
    if command_exists "zaproxy"; then
        installed_tools+=("owasp-zap")
    else
        failed_tools+=("owasp-zap")
    fi
fi

# Special installations
# Amass & Sublist3r
if command_exists "amass"; then
    installed_tools+=("amass")
else
    if sudo snap install amass; then
        installed_tools+=("amass")
    else
        failed_tools+=("amass")
    fi
fi

if command_exists "sublist3r"; then
    installed_tools+=("sublist3r")
else
    if pip3 install sublist3r; then
        installed_tools+=("sublist3r")
    else
        failed_tools+=("sublist3r")
    fi
fi

# Metasploit
if command_exists "msfconsole"; then
    installed_tools+=("metasploit-framework")
else
    if sudo apt install -y metasploit-framework; then
        installed_tools+=("metasploit-framework")
    else
        failed_tools+=("metasploit-framework")
    fi
fi

# PsExec
if [ -d "impacket" ]; then
    installed_tools+=("PsExec")
else
    if git clone https://github.com/SecureAuthCorp/impacket.git impacket; then
        installed_tools+=("PsExec")
    else
        failed_tools+=("PsExec")
    fi
fi

# Evilginx2
if [ -d "evilginx2" ]; then
    installed_tools+=("evilginx2")
else
    if git clone https://github.com/kgretzky/evilginx2.git evilginx2; then
        installed_tools+=("evilginx2")
        cd evilginx2 && make && sudo make install
        cd ..
    fi
fi

# Sherloq
if [ -d "Sherloq" ]; then
    installed_tools+=("Sherloq")
else
    if git clone https://github.com/GuidoBartoli/sherloq.git Sherloq; then
        installed_tools+=("Sherloq")
    fi
fi

# Install Sherloq dependencies if Sherloq exists
if [ -d "Sherloq" ]; then
    cd Sherloq/gui && pip3 install -r requirements.txt
    cd ../..
fi

# Volatility
if [ -d "volatility3" ]; then
    installed_tools+=("Volatility")
else
    if git clone https://github.com/volatilityfoundation/volatility3.git volatility3; then
        installed_tools+=("Volatility")
    fi
fi

# Install Volatility dependencies if Volatility exists
if [ -d "volatility3" ]; then
    cd volatility3 && python3 setup.py install
    cd ..
fi

# Ghidra
if command_exists "ghidra"; then
    installed_tools+=("ghidra")
else
    if sudo snap install ghidra; then
        installed_tools+=("ghidra")
    fi
fi

# Dex2jar
if [ -d "dex2jar" ]; then
    installed_tools+=("dex2jar")
else
    if git clone https://github.com/pxb1988/dex2jar.git dex2jar; then
        installed_tools+=("dex2jar")
    fi
fi

# Radare2
if [ -d "radare2" ]; then
    installed_tools+=("radare2")
else
    if git clone https://github.com/radareorg/radare2.git radare2; then
        installed_tools+=("radare2")
        cd radare2 && ./sys/install.sh
        cd ..
    fi
fi

# Display installation summary
echo -e "\nInstallation Summary:"
echo -e "Installed tools: ${installed_tools[@]}"
echo -e "Failed to install: ${failed_tools[@]}"
