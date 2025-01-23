import argparse
import os
import subprocess
from datetime import datetime
import pytz

def create_output_folder(base_folder, user_id, timestamp, target):
    """Creates the output folder structure. Ensures no overwrite by appending a counter."""
    folder_name = f"toolname_{user_id}_{timestamp}"
    folder_path = os.path.join(base_folder, folder_name)
    counter = 1
    while os.path.exists(folder_path):
        folder_path = os.path.join(base_folder, f"{folder_name}_{counter}")
        counter += 1
    os.makedirs(folder_path)
    return folder_path

def run_vhostscan(target, output_file):
    """Runs the VHostScan tool with the specified target and output file."""
    try:
        command = [
            "VHostScan",
            "-t", target,
            "-oJ", output_file
        ]
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running VHostScan: {e}")
    except FileNotFoundError:
        print("VHostScan is not installed or not found in the PATH.")

def main():
    """Main script logic."""
    parser = argparse.ArgumentParser(description="Automate VHostScan tool usage.")
    parser.add_argument("target", help="The target to scan (e.g., URL, file, or directory).")
    parser.add_argument("-u", "--user_id", required=True, help="User ID for organizing output files.")
    parser.add_argument("-o", "--output", help="Optional output directory.")
    
    args = parser.parse_args()
    
    # Create a timestamp in IST
    ist = pytz.timezone("Asia/Kolkata")
    timestamp = datetime.now(ist).strftime("%Y-%m-%d_%H-%M-%S")
    
    # Determine output folder
    base_folder = args.output if args.output else "toolname_results"
    output_folder = create_output_folder(base_folder, args.user_id, timestamp, args.target)
    
    # Set output file path
    output_file = os.path.join(output_folder, f"toolname_{args.user_id}_{timestamp}_{args.target}.json")
    
    # Run VHostScan
    print(f"Running VHostScan for target: {args.target}")
    print(f"Output will be saved in: {output_file}")
    run_vhostscan(args.target, output_file)
    print("Scan completed.")

if __name__ == "__main__":
    main()
