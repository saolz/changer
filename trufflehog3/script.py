#!/usr/bin/env python3

import argparse
import subprocess
import os
import json
import csv
from datetime import datetime
import pytz  # For timezone handling

# Function to create directories if they don't exist
def create_directory(path):
    try:
        os.makedirs(path, exist_ok=True)
        print(f"Directory created: {path}")
    except Exception as e:
        print(f"Error creating directory: {e}")
        raise

# Function to run TruffleHog and capture its output
def run_trufflehog(repo_url, output_file):
    try:
        # Run TruffleHog command
        command = ["trufflehog", "git", repo_url, "--json"]
        result = subprocess.run(command, capture_output=True, text=True)
        
        # Check for errors
        if result.returncode != 0:
            print(f"Error running TruffleHog: {result.stderr}")
            return None
        
        # Parse JSON output
        output = result.stdout.strip().split('\n')
        secrets = [json.loads(line) for line in output if line]
        
        # Write output to CSV
        with open(output_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            # Write header
            writer.writerow(["Detector", "File", "Line", "Secret"])
            # Write data if secrets are found
            if secrets:
                for secret in secrets:
                    writer.writerow([
                        secret.get("DetectorName", ""),
                        secret.get("SourceMetadata", {}).get("Data", {}).get("Git", {}).get("file", ""),
                        secret.get("SourceMetadata", {}).get("Data", {}).get("Git", {}).get("line", ""),
                        secret.get("Raw", "")
                    ])
                print(f"Secrets found. Output saved to: {output_file}")
            else:
                # Write "No secrets found" in the CSV
                writer.writerow(["No secrets found", "", "", ""])
                print("No secrets found. Output saved to CSV.")
        
        return secrets
    except Exception as e:
        print(f"Error during TruffleHog execution: {e}")
        return None

# Main function
def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Automate TruffleHog for secret scanning.")
    parser.add_argument("-f", "--folder", help="Base folder path for output. Default: 'trufflehog_results' in current directory.")
    parser.add_argument("-o", "--output", help="Custom output file path.")
    parser.add_argument("repo_url", help="Git repository URL to scan.")
    parser.add_argument("-u", "--username", required=True, help="Username for folder naming.")
    args = parser.parse_args()

    # Generate timestamp in IST
    ist = pytz.timezone('Asia/Kolkata')
    timestamp = datetime.now(ist).strftime("%Y%m%d_%H%M%S")
    
    # Set default folder if not provided
    if args.folder:
        base_folder = args.folder
    else:
        base_folder = os.path.join(os.getcwd(), "trufflehog_results")
    
    # Create output folder structure
    user_folder = f"{args.username}_{timestamp}"
    output_folder = os.path.join(base_folder, user_folder)
    create_directory(output_folder)

    # Define output file path
    if args.output:
        output_file = args.output
    else:
        # Generate input command used in terminal for filename
        input_command = args.repo_url.replace('/', '_').replace(':', '_').replace('.', '_')
        output_file = os.path.join(output_folder, f"trufflehog_{args.username}_{timestamp}_{input_command}.csv")

    # Run TruffleHog
    print(f"Scanning repository: {args.repo_url}")
    secrets = run_trufflehog(args.repo_url, output_file)

    if secrets is None:
        print("An error occurred during the scan.")
    else:
        print(f"Scan completed. Results saved to: {output_file}")

if __name__ == "__main__":
    main()
