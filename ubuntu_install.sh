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
    "nikto" "wfuzz"
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
if [ -d "/opt/BurpSuite" ]; then
    installed_tools+=("burpsuite")
else
    echo "Installing Burp Suite..."
    wget -O burpsuite.sh "https://portswigger.net/burp/releases/download?product=community&version=2023.12.1&type=Linux" --content-disposition
    chmod +x burpsuite.sh && sudo ./burpsuite.sh
    sudo mv /opt/BurpSuiteCommunity /opt/BurpSuite
    if [ -d "/opt/BurpSuite" ]; then
        installed_tools+=("burpsuite")
    else
        failed_tools+=("burpsuite")
    fi
fi

# Install OWASP ZAP
if [ -d "owasp-zap" ]; then
    installed_tools+=("owasp-zap")
else
    echo "Installing OWASP ZAP..."
    sudo apt install -y openjdk-17-jre
    export INSTALL4J_JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
    wget -O zap.tar.gz "https://github.com/zaproxy/zaproxy/releases/download/v2.13.0/ZAP_2.13.0_Linux.tar.gz"
    tar -xvzf zap.tar.gz -C /opt/
    sudo mv /opt/ZAP_2.13.0 /opt/ZAP
    sudo ln -sf /opt/ZAP/zap.sh /usr/local/bin/zaproxy
    if [ -d "/opt/ZAP" ]; then
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

# PsExec (via Impacket)
if [ -d "impacket" ]; then
    installed_tools+=("PsExec")
else
    if git clone https://github.com/SecureAuthCorp/impacket.git impacket; then
        installed_tools+=("PsExec")
        cd impacket && pip3 install .
        cd ..
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
    else
        failed_tools+=("evilginx2")
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

# Responder
if [ ! -d "Responder" ]; then
    git clone https://github.com/lgandx/Responder.git Responder && installed_tools+=("Responder") || failed_tools+=("Responder")
fi

# Social-Engineer Toolkit (SET)
if ! command_exists "setoolkit"; then
    git clone https://github.com/trustedsec/social-engineer-toolkit.git setoolkit && \
    cd setoolkit && python3 setup.py install && cd .. && installed_tools+=("SET") || failed_tools+=("SET")
fi

# GoPhish
if [ ! -d "gophish" ]; then
    echo "Installing GoPhish..."
    wget https://github.com/gophish/gophish/releases/download/v0.12.1/gophish-v0.12.1-linux-64bit.zip
    unzip gophish-v0.12.1-linux-64bit.zip -d gophish
    if [ -d "gophish" ]; then
        installed_tools+=("GoPhish")
    else
        failed_tools+=("GoPhish")
    fi
fi

# Mimikatz
if [ ! -d "mimikatz" ]; then
    echo "Installing Mimikatz..."
    git clone https://github.com/gentilkiwi/mimikatz.git mimikatz
    if [ -d "mimikatz" ]; then
        installed_tools+=("Mimikatz")
    else
        failed_tools+=("Mimikatz")
    fi
fi

# Display installation summary
echo -e "\nInstallation Summary:"
echo -e "Installed tools: ${installed_tools[@]}"
echo -e "Failed to install: ${failed_tools[@]}"
