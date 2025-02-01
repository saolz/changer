import smtplib
import argparse
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def send_email(smtp_server, port, username, password, sender, recipient, subject, html_body, attachment=None, use_tls=True):
    try:
        # Setup email headers
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = recipient
        msg['Subject'] = subject
        
        # Attach the HTML content
        msg.attach(MIMEText(html_body, 'html'))
        
        # Attach a file if specified
        if attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(open(attachment, 'rb').read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(attachment)}')
            msg.attach(part)
        
        # Connect to SMTP server
        server = smtplib.SMTP(smtp_server, port)
        if use_tls:
            server.starttls()
        server.login(username, password)
        
        # Send email
        server.sendmail(sender, recipient, msg.as_string())
        server.quit()
        print("[+] Email Sent Successfully!")
    except Exception as e:
        print(f"[-] Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Custom Phishing Email Sender")
    parser.add_argument('--server', required=True, help='SMTP Server (e.g., smtp.yandex.com)')
    parser.add_argument('--port', type=int, required=True, help='SMTP Port (465 for SSL, 587 for TLS)')
    parser.add_argument('--username', required=True, help='SMTP Username')
    parser.add_argument('--password', required=True, help='SMTP Password')
    parser.add_argument('--sender', required=True, help='Fake Sender Email')
    parser.add_argument('--recipient', required=True, help='Target Email')
    parser.add_argument('--subject', required=True, help='Email Subject')
    parser.add_argument('--html', required=True, help='HTML file for email body')
    parser.add_argument('--attachment', help='File to attach (optional)')
    parser.add_argument('--no-tls', action='store_true', help='Disable TLS (use SSL)')
    
    args = parser.parse_args()
    
    # Read HTML file content
    if not os.path.exists(args.html):
        print("[-] HTML file not found!")
        exit(1)
    with open(args.html, 'r', encoding='utf-8') as f:
        html_body = f.read()
    
    send_email(
        smtp_server=args.server,
        port=args.port,
        username=args.username,
        password=args.password,
        sender=args.sender,
        recipient=args.recipient,
        subject=args.subject,
        html_body=html_body,
        attachment=args.attachment,
        use_tls=not args.no_tls
    )
