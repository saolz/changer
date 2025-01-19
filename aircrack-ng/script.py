import os
import subprocess
import argparse
import csv
from datetime import datetime

# Function to create a folder structure for storing results
def create_user_folder(tool_folder, user_id):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    user_folder = os.path.join(tool_folder, f"{user_id}_{timestamp}")
    os.makedirs(user_folder, exist_ok=True)
    return user_folder, timestamp

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

        # Save the output to a CSV file
        csv_file = os.path.join(user_folder, f"aircrack_{user_id}.csv")
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
            writer.writerow(["Timestamp", "Message"])  # Header row

            # Parse Aircrack-ng output line-by-line
            for line in lines:
                if line.strip():  # Skip empty lines
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    writer.writerow([timestamp, line.strip()])

    except Exception as e:
        print(f"[ERROR] Failed to save output to CSV: {e}")

# Function to scan for wireless access points, clients, and SSIDs using airodump-ng
def scan_wireless_networks(user_folder):
    try:
        # Use airodump-ng to scan for networks and clients
        command = ["airodump-ng", "mon0", "--write", os.path.join(user_folder, "network_scan"), "--output-format", "csv"]
        print(f"Running command: {' '.join(command)}")
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        # Save output to a CSV file (output is saved by airodump-ng itself)
        print(f"Network scan completed. Results saved to {user_folder}/network_scan.csv")
        return os.path.join(user_folder, "network_scan.csv")

    except Exception as e:
        print(f"[ERROR] An error occurred while scanning for wireless networks: {e}")
        return None

# Main function
def main():
    parser = argparse.ArgumentParser(description="Automate Aircrack-ng with output management.")
    parser.add_argument("--user_id", required=True, help="Unique identifier for the user.")
    parser.add_argument("--input_file", help="Input file(s) for Aircrack-ng.")
    parser.add_argument("--attack_mode", help="Force attack mode (1=WEP, 2=WPA-PSK).")
    parser.add_argument("--essid", help="Target network identifier (ESSID).")
    parser.add_argument("--bssid", help="Target access point's MAC address.")
    parser.add_argument("--wordlist", help="Path to wordlist(s) for cracking WPA-PSK.")
    parser.add_argument("--quiet_mode", action="store_true", help="Enable quiet mode (no status output).")
    parser.add_argument("--other_flags", help="Additional Aircrack-ng flags to include.")
    parser.add_argument("--scan", action="store_true", help="Scan for wireless networks and clients before running Aircrack-ng.")
    
    args = parser.parse_args()

    # Create the main tool folder and user folder
    tool_folder = "aircrack_tool"
    os.makedirs(tool_folder, exist_ok=True)
    user_folder, timestamp = create_user_folder(tool_folder, args.user_id)

    if args.scan:
        # Run wireless network scan
        scan_result_file = scan_wireless_networks(user_folder)
        if scan_result_file:
            print(f"Scan results saved to {scan_result_file}")

    if args.input_file:
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
    else:
        print("No input file provided for Aircrack-ng. Skipping cracking process.")

    print(f"Results saved in folder: {user_folder}")

if __name__ == "__main__":
    main()
