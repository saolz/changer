import os
import subprocess
import argparse
import csv
from datetime import datetime


# Function to create a folder structure for storing results
def create_user_folder(tool_folder, user_id):
    """Creates a folder structure for storing results."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    user_folder = os.path.join(tool_folder, f"{user_id}_{timestamp}")
    os.makedirs(user_folder, exist_ok=True)
    return user_folder, timestamp


# Function to run the sqlmap command and capture output
def run_sqlmap(user_folder, tool_name, user_id, url, data, random_agent, proxy, tor, dbs, dump, other_flags):
    """Runs the sqlmap command with the given parameters."""
    try:
        # Base sqlmap command
        command = ["sqlmap", "-u", url, "--batch"]

        # Adding optional arguments
        if data:
            command += ["--data", data]
        if random_agent:
            command.append("--random-agent")
        if proxy:
            command += ["--proxy", proxy]
        if tor:
            command.append("--tor")
        if dbs:
            command.append("--dbs")
        if dump:
            command.append("--dump")
        if other_flags:
            command += other_flags.split()

        # Execute the command and capture the output
        print(f"Running command: {' '.join(command)}")
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        # Decode stdout
        output_text = stdout.decode()

        # Save the output to a CSV file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        sanitized_url = url.replace("https://", "").replace("http://", "").replace("/", "_")
        csv_file = os.path.join(
            user_folder,
            f"{tool_name}_{user_id}_{timestamp}_{sanitized_url}.csv"
        )
        save_to_csv(output_text, csv_file, url)

        print(f"Execution completed. Output saved to {csv_file}")
        return csv_file

    except Exception as e:
        print(f"[ERROR] An error occurred while running sqlmap: {e}")
        return None


# Function to parse and save output to a CSV file
def save_to_csv(output_text, csv_file, input_url):
    """Parses sqlmap output and saves it to a CSV file."""
    try:
        # Split output into lines
        lines = output_text.split("\n")

        # Open CSV file for writing
        with open(csv_file, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "Input URL", "Message"])  # Header row

            # Parse SQLmap output line-by-line
            for line in lines:
                if line.strip():  # Skip empty lines
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    writer.writerow([timestamp, input_url, line.strip()])

    except Exception as e:
        print(f"[ERROR] Failed to save output to CSV: {e}")


# Main function
def main():
    """Main function to handle argument parsing and tool execution."""
    parser = argparse.ArgumentParser(description="Automate sqlmap with output management.")
    parser.add_argument("--user_id", required=True, help="Unique identifier for the user.")
    parser.add_argument("--url", required=True, help="Target URL for SQL injection testing.")
    parser.add_argument("--data", help="POST data to send with the request.")
    parser.add_argument("--random_agent", action="store_true", help="Use a random User-Agent.")
    parser.add_argument("--proxy", help="Proxy to connect to the target URL.")
    parser.add_argument("--tor", action="store_true", help="Use the Tor anonymity network.")
    parser.add_argument("--dbs", action="store_true", help="Enumerate databases.")
    parser.add_argument("--dump", action="store_true", help="Dump database contents.")
    parser.add_argument("--other_flags", help="Additional sqlmap flags to include.")
    parser.add_argument("--output", help="Custom output folder path.")

    args = parser.parse_args()

    # Set up tool and output folders
    tool_folder = "sqlmap_tool"
    os.makedirs(tool_folder, exist_ok=True)

    if args.output:
        # Use custom output folder
        user_folder = args.output
        os.makedirs(user_folder, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    else:
        # Create default user folder
        user_folder, timestamp = create_user_folder(tool_folder, args.user_id)

    # Run the sqlmap command
    run_sqlmap(
        user_folder=user_folder,
        tool_name="sqlmap",
        user_id=args.user_id,
        url=args.url,
        data=args.data,
        random_agent=args.random_agent,
        proxy=args.proxy,
        tor=args.tor,
        dbs=args.dbs,
        dump=args.dump,
        other_flags=args.other_flags,
    )

    print(f"Results saved in folder: {user_folder}")


if __name__ == "__main__":
    main()
