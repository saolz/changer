python phishing_mailer.py --server smtp.yandex.com --port 587 --username dloklok@yandex.com --password YOUR_PASSWORD --sender dloklok@yandex.com --recipient target@example.com --subject "Important Update" --html email_template.html --attachment file.pdf
#!/bin/bash

echo "Installing Social-Engineer Toolkit (SET) and dependencies..."

# Update system
sudo apt update && sudo apt install -y git python3-pip

# Clone SET from GitHub
git clone https://github.com/trustedsec/social-engineer-toolkit.git setoolkit

# Navigate to SET directory and install
cd setoolkit || exit
pip3 install -r requirements.txt
python3 setup.py install

echo "Installation complete. Run using: sudo setoolkit"
