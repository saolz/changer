import argparse
import os
import subprocess
import sys
from datetime import datetime
import csv

# Function to create a folder for the UserID and store the output
def create_user_folder(user_id):
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        user_folder_name = f"{user_id}_{timestamp}"
        base_folder = "./tool_folder"
        output_folder = os.path.join(base_folder, user_folder_name)

        # Create base folder if it doesn't exist
        if not os.path.exists(base_folder):
            os.makedirs(base_folder)

        # Create user folder
        os.makedirs(output_folder)
        return output_folder

    except Exception as e:
        print(f"Error creating user folder: {e}")
        sys.exit(1)

# Function to run the Metagoofil command
def run_metagoofil(input_domain, file_types, delay, save_file, search_max, url_timeout, download_limit, save_directory, threads, user_agent, verbose):
    try:
        # Build the Metagoofil command
        command = [
            "python3", "metagoofil.py",
            "-d", input_domain,
            "-t", file_types,
            "-e", str(delay),
            "-l", str(search_max),
            "-i", str(url_timeout),
            "-n", str(download_limit),
            "-o", save_directory,
            "-r", str(threads)
        ]

        if user_agent:
            command += ["-u", user_agent]

        if verbose:
            command.append("-w")

        # Print the command for debugging
        print(f"Running command: {' '.join(command)}")

        # Run the Metagoofil command and capture its output
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Check for errors
        if result.returncode != 0:
            print(f"Error running Metagoofil: {result.stderr}")
            sys.exit(1)

        print("Metagoofil command completed successfully.")
        return result.stdout  # Return the terminal output

    except Exception as e:
        print(f"Error running Metagoofil command: {e}")
        sys.exit(1)

# Function to save terminal output to a CSV file
def save_output_to_csv(output_text, save_file_path):
    try:
        # Open the CSV file for writing
        with open(save_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)

            # Add a header row
            csv_writer.writerow(["Message Type", "Details"])

            # Parse the terminal output and save structured data
            for line in output_text.splitlines():
                if "[*]" in line:
                    csv_writer.writerow(["Info", line.strip("[*] ")])
                elif "[+]" in line:
                    csv_writer.writerow(["Success", line.strip("[+] ")])
                elif "Error" in line or "[!]" in line:
                    csv_writer.writerow(["Error", line.strip("[!] ")])

        print(f"Output successfully saved to {save_file_path}")
    except Exception as e:
        print(f"Error saving output to CSV: {e}")
        sys.exit(1)

# Main function to parse arguments and initiate the process
def main():
    # Setting up argument parser
    parser = argparse.ArgumentParser(description="Automated script for Metagoofil")
    parser.add_argument("-d", "--domain", required=True, help="Domain to perform information gathering on")
    parser.add_argument("-t", "--file_types", required=True, help="Comma separated file types (e.g., pdf,docx,xls)")
    parser.add_argument("-e", "--delay", type=int, default=2, help="Delay between requests in seconds (default 2)")
    parser.add_argument("-l", "--search_max", type=int, default=50, help="Maximum number of search results (default 50)")
    parser.add_argument("-i", "--url_timeout", type=int, default=30, help="URL timeout in seconds (default 30)")
    parser.add_argument("-n", "--download_file_limit", type=int, default=10, help="Limit on the number of files to download (default 10)")
    parser.add_argument("-o", "--save_directory", help="Directory to save output files (optional, defaults to user folder)")
    parser.add_argument("-r", "--threads", type=int, default=5, help="Number of threads to use (default 5)")
    parser.add_argument("-u", "--user_agent", help="User-agent string (optional)")
    parser.add_argument("-w", "--verbose", action="store_true", help="Enable verbose output (optional)")
    parser.add_argument("user_id", help="UserID to create a folder for output")

    # Parse the arguments
    args = parser.parse_args()

    # Assign arguments to variables
    input_domain = args.domain
    input_file_types = args.file_types
    input_delay = args.delay
    input_search_max = args.search_max
    input_url_timeout = args.url_timeout
    input_download_limit = args.download_file_limit
    input_save_directory = args.save_directory
    input_threads = args.threads
    input_user_agent = args.user_agent
    input_verbose = args.verbose
    user_id = args.user_id

    try:
        # Create user folder
        output_folder = create_user_folder(user_id)

        # Default save file name
        if not args.save_directory:
            args.save_directory = output_folder

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        save_file_name = f"metagoofil_{user_id}_{timestamp}_output.csv"
        save_file_path = os.path.join(args.save_directory, save_file_name)

        # Run the Metagoofil tool
        terminal_output = run_metagoofil(
            input_domain, input_file_types, input_delay, save_file_name,
            input_search_max, input_url_timeout, input_download_limit,
            args.save_directory, input_threads, input_user_agent, input_verbose
        )

        # Save the terminal output to a CSV file
        save_output_to_csv(terminal_output, save_file_path)

    except Exception as e:
        print(f"Error in script execution: {e}")
        sys.exit(1)

# Execute the script
if __name__ == "__main__":
    main()
