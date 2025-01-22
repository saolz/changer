import os
import csv
import argparse
import subprocess
import time
from urllib.parse import urlparse

# Function to create directories for output
def create_output_folder(base_folder, tool_name, user_id, timestamp):
    # Base folder: tool_timestamp
    tool_folder = os.path.join(base_folder, f"{tool_name}_{timestamp}")
    os.makedirs(tool_folder, exist_ok=True)
    
    # User folder inside the tool folder
    user_folder = os.path.join(tool_folder, f"{tool_name}_{user_id}_{timestamp}")
    os.makedirs(user_folder, exist_ok=True)
    
    return user_folder

# Function to validate domain
def validate_domain(domain):
    try:
        parsed_url = urlparse(domain)
        if not parsed_url.scheme or not parsed_url.netloc:
            raise ValueError("Invalid domain. Ensure it starts with http:// or https://")
    except Exception as e:
        raise ValueError(f"Error parsing domain: {e}")

# Function to execute trufflehog3 command
def run_trufflehog3(domain, output_file):
    try:
        # Construct the command
        command = [
            "trufflehog3", "--no-entropy", "--no-pattern", "--no-history",
            "--format", "JSON", domain
        ]
        # Run the command and capture output
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        # Write JSON output to a file
        with open(output_file, "w") as f:
            f.write(result.stdout)
        return f"Results saved to {output_file}"
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Trufflehog3 failed: {e.stderr.strip()}")

# Main function
def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Automate trufflehog3 scanning.")
    parser.add_argument("-d", "--domain", required=True, help="Domain to scan (e.g., https://example.com)")
    parser.add_argument("-u", "--user", required=True, help="User ID for organizing outputs")
    parser.add_argument("-o", "--output", help="Base output folder (default: current directory)")
    args = parser.parse_args()

    # Tool name
    tool_name = "trufflehog3"

    # Default base folder
    base_folder = args.output if args.output else os.getcwd()

    # Generate timestamp in IST and human-readable format
    ist_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())

    try:
        # Validate domain
        validate_domain(args.domain)

        # Create output folders
        user_folder = create_output_folder(base_folder, tool_name, args.user, ist_time)

        # Default CSV file name
        csv_filename = f"{tool_name}_{args.user}_{ist_time}_{urlparse(args.domain).netloc.replace('.', '_')}.csv"
        csv_filepath = os.path.join(user_folder, csv_filename)

        # Run trufflehog3 and save results
        result = run_trufflehog3(args.domain, csv_filepath)
        print(result)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
