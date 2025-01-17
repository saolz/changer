import argparse
import os
import subprocess
import sys
from datetime import datetime

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
            "-f", save_file,
            "-i", str(url_timeout),
            "-l", str(search_max),
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

        print(f"Metagoofil completed successfully. Output:\n{result.stdout}")

    except Exception as e:
        print(f"Error running Metagoofil command: {e}")
        sys.exit(1)

# Main function to parse arguments and initiate the process
def main():
    # Setting up argument parser
    parser = argparse.ArgumentParser(description="Automated script for Metagoofil")
    parser.add_argument("-d", "--domain", required=True, help="Domain to perform information gathering on")
    parser.add_argument("-t", "--file_types", required=True, help="Comma separated file types (e.g., pdf,docx,xls)")
    parser.add_argument("-e", "--delay", type=int, default=2, help="Delay between requests in seconds (default 2)")
    parser.add_argument("-f", "--save_file", help="Output filename (default toolname_userid_timestamp_inputcommand.csv)")
    parser.add_argument("-i", "--url_timeout", type=int, default=30, help="URL timeout in seconds (default 30)")
    parser.add_argument("-l", "--search_max", type=int, default=50, help="Maximum number of search results (default 50)")
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
    input_save_file = args.save_file
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
        if not input_save_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            input_save_file = f"metagoofil_{user_id}_{timestamp}_output.csv"

        # If save directory is not provided, use the user folder
        if not input_save_directory:
            input_save_directory = output_folder

        # Full path for save file
        save_file_path = os.path.join(input_save_directory, input_save_file)

        # Run the Metagoofil tool
        run_metagoofil(
            input_domain, input_file_types, input_delay, save_file_path,
            input_search_max, input_url_timeout, input_download_limit,
            input_save_directory, input_threads, input_user_agent, input_verbose
        )

        # Check if the output file was created
        if os.path.exists(save_file_path):
            print(f"Output saved successfully in: {save_file_path}")
        else:
            print("Error: Output file was not generated.")

    except Exception as e:
        print(f"Error in script execution: {e}")
        sys.exit(1)

# Execute the script
if __name__ == "__main__":
    main()
