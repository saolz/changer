import os
import sys
import argparse
import subprocess
import datetime
import pytz

# Function to create output directory based on user ID and timestamp
def create_output_directory(base_dir, user_id):
    try:
        # Set IST timezone
        ist = pytz.timezone("Asia/Kolkata")
        current_time = datetime.datetime.now(ist).strftime("%Y-%m-%d_%H-%M-%S")
        user_folder = f"{user_id}_{current_time}"
        output_path = os.path.join(base_dir, user_folder)
        os.makedirs(output_path, exist_ok=True)
        return output_path
    except Exception as e:
        print(f"Error creating output directory: {e}")
        sys.exit(1)

# Function to run Nikto with user-provided arguments
def run_nikto(args, output_file):
    try:
        # Base command
        cmd = ["nikto"]

        # Adding options based on user input
        if args.host:
            cmd.extend(["-host", args.host])
        if args.find_vhosts:
            cmd.append("-vhost")
        
        # Ensure output is always in CSV format
        cmd.extend(["-Format", "csv", "-output", output_file])
        
        # Redirect output to a file
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Nikto command executed successfully. Output saved to {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error running Nikto: {e.stderr.decode()}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

# Main function
def main():
    parser = argparse.ArgumentParser(description="Automated Nikto Script")

    # Define arguments
    parser.add_argument("-u", "--user_id", required=True, help="User ID for folder creation")
    parser.add_argument("-o", "--output", help="Output directory for the results")
    parser.add_argument("-H", "--host", required=True, help="Host to scan with Nikto")
    parser.add_argument("-v", "--find_vhosts", action="store_true", help="Find virtual hosts on web and mail servers")

    args = parser.parse_args()

    # Set up base directory
    base_dir = args.output if args.output else os.path.join(os.getcwd(), "nikto_results")

    # Create output directory
    output_dir = create_output_directory(base_dir, args.user_id)

    # Set IST timezone for output file naming
    ist = pytz.timezone("Asia/Kolkata")
    current_time = datetime.datetime.now(ist).strftime("%Y-%m-%d_%H-%M-%S")
    output_file = os.path.join(output_dir, f"nikto_{args.user_id}_{current_time}.csv")

    # Run the Nikto command
    run_nikto(args, output_file)

if __name__ == "__main__":
    main()
