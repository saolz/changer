import argparse
import os
import subprocess
import datetime
import json

def get_timestamp():
    return datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

def create_output_directory(base_dir, user_id, timestamp):
    dir_name = f"theharvester_{user_id}_{timestamp}"
    full_path = os.path.join(base_dir, dir_name)
    counter = 1
    while os.path.exists(full_path):
        full_path = os.path.join(base_dir, f"{dir_name}_{counter}")
        counter += 1
    os.makedirs(full_path)
    return full_path

def run_theharvester(target, output_path, user_id, timestamp):
    output_file = os.path.join(output_path, f"theharvester_{user_id}_{timestamp}_{target}.json")
    command = ["theHarvester", "-d", target, "-b", "all", "-f", output_file]
    try:
        subprocess.run(command, check=True)
        print(f"Results saved to {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error running theHarvester: {e}")

def main():
    parser = argparse.ArgumentParser(description="Automate theHarvester tool usage.")
    parser.add_argument("target", help="Target domain for OSINT gathering.")
    parser.add_argument("-u", "--user", required=True, help="User ID for tracking.")
    parser.add_argument("-o", "--output", default="theharvester_results", help="Output directory (default: theharvester_results/).")
    
    args = parser.parse_args()
    timestamp = get_timestamp()
    output_dir = create_output_directory(args.output, args.user, timestamp)
    run_theharvester(args.target, output_dir, args.user, timestamp)

if __name__ == "__main__":
    main()
