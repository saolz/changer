import os
import sys
import argparse
import subprocess
import datetime
import pytz
# Function to create output directories
def create_output_directory(base_directory, user_id):
    try:
        # Setting IST timezone
        ist = pytz.timezone("Asia/Kolkata")
        current_time = datetime.datetime.now(ist).strftime("%Y-%m-%d_%H-%M-%S")
        user_folder = f"{user_id}_{current_time}"
        output_directory = os.path.join(base_directory, user_folder)
        os.makedirs(output_directory, exist_ok=True)
        return output_directory
    except Exception as e:
        print(f"Error creating output directory: {e}")
        sys.exit(1)
# Function to run the Kismet command
def run_kismet(args, output_file):
    try:
        # Base command
        cmd = ["kismet"]
        # Adding options based on user input
        if args.server:
            cmd.append("--server")
        if args.source:
            cmd.extend(["--source", args.source])
        if args.log_prefix:
            cmd.extend(["--log-prefix", args.log_prefix])
        if args.log_types:
            cmd.extend(["--log-types", ",".join(args.log_types)])
        if args.daemonize:
            cmd.append("--daemonize")
        if args.alerts:
            cmd.extend(["--alerts", ",".join(args.alerts)])
        if args.channels:
            cmd.extend(["--channels", args.channels])
        if args.capture_sources:
            cmd.extend(["--capture-sources", args.capture_sources])
        # Redirecting output to a file
        with open(output_file, "w") as out:
            subprocess.run(cmd, check=True, stdout=out, stderr=subprocess.PIPE)
        print(f"Kismet command executed successfully. Output saved to {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error running Kismet: {e.stderr.decode()}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)
# Main function
def main():
    parser = argparse.ArgumentParser(description="Automated Kismet Script")
    # Define arguments
    parser.add_argument("-u", "--user_id", required=True, help="User ID for folder creation")
    parser.add_argument("-o", "--output", help="Output directory for the results")
    parser.add_argument("--server", action="store_true", help="Start Kismet as a server")
    parser.add_argument("--source", help="Specify the capture source")
    parser.add_argument("--log-prefix", help="Specify the log prefix")
    parser.add_argument("--log-types", nargs="+", help="Specify log types (comma-separated)")
    parser.add_argument("--daemonize", action="store_true", help="Run Kismet as a daemon")
    parser.add_argument("--alerts", nargs="+", help="Specify alerts to log (comma-separated)")
    parser.add_argument("--channels", help="Specify channels to monitor")
    parser.add_argument("--capture-sources", help="Specify capture sources")
    args = parser.parse_args()
    # Set up base directory
    base_directory = args.output if args.output else os.path.join(os.getcwd(), "kismet_results")
    # Create output directory
    output_directory = create_output_directory(base_directory, args.user_id)
    # Set IST timezone for output file naming
    ist = pytz.timezone("Asia/Kolkata")
    current_time = datetime.datetime.now(ist).strftime("%Y-%m-%d_%H-%M-%S")
    output_file = os.path.join(output_directory, f"kismet_{args.user_id}_{current_time}.txt")
    # Run the Kismet command
    run_kismet(args, output_file)
if __name__ == "__main__":
    main()
