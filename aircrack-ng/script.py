import os
import subprocess
import argparse
import csv
from datetime import datetime, timedelta

# Convert UTC to IST
def get_ist_time():
    utc_now = datetime.utcnow()
    ist_offset = timedelta(hours=5, minutes=30)
    return utc_now + ist_offset

# Function to create a folder structure for storing results
def create_user_folder(tool_folder, user_id):
    timestamp = get_ist_time().strftime("%Y-%m-%d_%H-%M-%S")
    user_folder = os.path.join(tool_folder, f"{user_id}_{timestamp}")
    os.makedirs(user_folder, exist_ok=True)
    return user_folder, timestamp

# Function to sanitize the command string for the filename
def sanitize_command(command):
    return "_".join(filter(None, "".join([c if c.isalnum() or c == " " else "_" for c in command]).split()))

# Function to run the Aircrack-ng command
def run_aircrack(user_folder, user_id, input_file, attack_mode, essid, bssid, wordlist, quiet_mode, other_flags):
    try:
        # Base Aircrack-ng command
        command = ["aircrack-ng", input_file]

        # Adding optional arguments
        if attack_mode:
            command += ["-a", attack_mode]
        if essid:
            command += ["-e", essid]
        if bssid:
            command += ["-b", bssid]
        if wordlist:
            command += ["-w", wordlist]
        if quiet_mode:
            command.append("-q")
        if other_flags:
            command += other_flags.split()

        # Execute the command and capture the output
        print(f"Running command: {' '.join(command)}")
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        # Save stdout to a variable
        output_text = stdout.decode()

        # Sanitize command for filename
        sanitized_command = sanitize_command(" ".join(command))

        # Save the output to a CSV file
        timestamp = get_ist_time().strftime("%Y-%m-%d_%H-%M-%S")
        csv_file = os.path.join(
            user_folder, f"aircrack_{user_id}_{timestamp}_{sanitized_command}.csv"
        )
        save_to_csv(output_text, csv_file)

        print(f"Execution completed. Output saved to {csv_file}")
        return csv_file

    except Exception as e:
        print(f"[ERROR] An error occurred while running Aircrack-ng: {e}")
        return None

# Function to parse and save output to a CSV file
def save_to_csv(output_text, csv_file):
    try:
        # Split output into lines
        lines = output_text.split("\n")

        # Open CSV file for writing
        with open(csv_file, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp (IST)", "Message"])  # Header row

            # Parse Aircrack-ng output line-by-line
            for line in lines:
                if line.strip():  # Skip empty lines
                    timestamp = get_ist_time().strftime("%Y-%m-%d %H:%M:%S")
                    writer.writerow([timestamp, line.strip()])

    except Exception as e:
        print(f"[ERROR] Failed to save output to CSV: {e}")

# Main function
def main():
    parser = argparse.ArgumentParser(description="Automate Aircrack-ng with output management.")
    parser.add_argument("--user_id", required=True, help="Unique identifier for the user.")
    parser.add_argument("--input_file", required=True, help="Input file(s) for Aircrack-ng.")
    parser.add_argument("--attack_mode", help="Force attack mode (1=WEP, 2=WPA-PSK).")
    parser.add_argument("--essid", help="Target network identifier (ESSID).")
    parser.add_argument("--bssid", help="Target access point's MAC address.")
    parser.add_argument("--wordlist", help="Path to wordlist(s) for cracking WPA-PSK.")
    parser.add_argument("--quiet_mode", action="store_true", help="Enable quiet mode (no status output).")
    parser.add_argument("--other_flags", help="Additional Aircrack-ng flags to include.")
    
    args = parser.parse_args()

    # Create the main tool folder and user folder
    tool_folder = "aircrack_tool"
    os.makedirs(tool_folder, exist_ok=True)
    user_folder, timestamp = create_user_folder(tool_folder, args.user_id)

    # Run the Aircrack-ng command
    run_aircrack(
        user_folder=user_folder,
        user_id=args.user_id,
        input_file=args.input_file,
        attack_mode=args.attack_mode,
        essid=args.essid,
        bssid=args.bssid,
        wordlist=args.wordlist,
        quiet_mode=args.quiet_mode,
        other_flags=args.other_flags,
    )

    print(f"Results saved in folder: {user_folder}")


if __name__ == "__main__":
    main()
