import os
import sys
import argparse
import subprocess
import datetime
import pytz

# Function to handle the creation of directories
def create_user_output_directory(base_dir, user_id):
    """
    Creates a user-specific directory inside the main tool folder based on the user ID and timestamp.
    """
    try:
        # Get IST timezone
        ist = pytz.timezone("Asia/Kolkata")
        timestamp = datetime.datetime.now(ist).strftime("%Y-%m-%d_%H-%M-%S")
        user_folder_name = f"{user_id}_{timestamp}"
        user_output_path = os.path.join(base_dir, user_folder_name)
        os.makedirs(user_output_path, exist_ok=True)
        return user_output_path
    except Exception as e:
        print(f"Error creating user output directory: {e}")
        sys.exit(1)

# Function to run the Fierce tool and save the output
def run_fierce_tool(input_args, output_file_path):
    """
    Constructs and runs the Fierce command based on user inputs, and saves the output to a file.
    """
    try:
        # Base command for Fierce
        fierce_command = ["fierce"]

        # Add arguments based on user inputs
        if input_args.input_domain:
            fierce_command.extend(["--domain", input_args.input_domain])
        if input_args.connect:
            fierce_command.append("--connect")
        if input_args.wide:
            fierce_command.append("--wide")
        if input_args.traverse:
            fierce_command.extend(["--traverse", str(input_args.traverse)])
        if input_args.search_domains:
            fierce_command.extend(["--search"] + input_args.search_domains)
        if input_args.ip_range:
            fierce_command.extend(["--range", input_args.ip_range])
        if input_args.delay:
            fierce_command.extend(["--delay", str(input_args.delay)])
        if input_args.subdomains:
            fierce_command.extend(["--subdomains"] + input_args.subdomains)
        if input_args.subdomain_file:
            fierce_command.extend(["--subdomain-file", input_args.subdomain_file])
        if input_args.dns_servers:
            fierce_command.extend(["--dns-servers"] + input_args.dns_servers)
        if input_args.dns_file:
            fierce_command.extend(["--dns-file", input_args.dns_file])
        if input_args.use_tcp:
            fierce_command.append("--tcp")

        # Redirect output to a file
        with open(output_file_path, "w") as output_file:
            subprocess.run(fierce_command, check=True, stdout=output_file, stderr=subprocess.PIPE)

        print(f"Fierce command executed successfully. Output saved to: {output_file_path}")
    except subprocess.CalledProcessError as error:
        print(f"Error while running Fierce: {error.stderr.decode()}\nCommand: {' '.join(error.cmd)}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error while running Fierce: {e}")
        sys.exit(1)

# Main function to handle argument parsing and execution
def main():
    """
    Main function to parse arguments, create directories, and run the Fierce tool.
    """
    parser = argparse.ArgumentParser(description="Automated Script for the Fierce DNS Reconnaissance Tool")

    # User and output arguments
    parser.add_argument("-u", "--user_id", required=True, help="User ID for folder creation")
    parser.add_argument("-o", "--output_dir", help="Base directory for output files (default: current directory)")
    parser.add_argument("-f", "--file_name", help="Specify output file name (optional)")

    # Fierce tool arguments
    parser.add_argument("--domain", dest="input_domain", required=True, help="Domain name to test")
    parser.add_argument("--connect", action="store_true", help="Attempt HTTP connection to non-RFC 1918 hosts")
    parser.add_argument("--wide", action="store_true", help="Scan entire class C of discovered records")
    parser.add_argument("--traverse", type=int, help="Scan IPs near discovered records")
    parser.add_argument("--search", dest="search_domains", nargs="+", help="Filter on these domains when expanding lookup")
    parser.add_argument("--range", dest="ip_range", help="Scan an internal IP range, use CIDR notation")
    parser.add_argument("--delay", type=int, help="Time to wait between lookups")
    parser.add_argument("--subdomains", nargs="+", help="Use these subdomains")
    parser.add_argument("--subdomain-file", help="Use subdomains specified in this file (one per line)")
    parser.add_argument("--dns-servers", nargs="+", help="Use these DNS servers for reverse lookups")
    parser.add_argument("--dns-file", help="Use DNS servers specified in this file for reverse lookups (one per line)")
    parser.add_argument("--tcp", dest="use_tcp", action="store_true", help="Use TCP instead of UDP")

    # Parse arguments
    args = parser.parse_args()

    # Determine the base output directory
    base_output_directory = args.output_dir if args.output_dir else os.path.join(os.getcwd(), "fierce_results")

    # Create user-specific output directory
    user_output_directory = create_user_output_directory(base_output_directory, args.user_id)

    # Create output file name
    ist = pytz.timezone("Asia/Kolkata")
    timestamp = datetime.datetime.now(ist).strftime("%Y-%m-%d_%H-%M-%S")
    if args.file_name:
        output_file_name = args.file_name
    else:
        output_file_name = f"fierce_{args.user_id}_{timestamp}_{args.input_domain}.csv"

    output_file_path = os.path.join(user_output_directory, output_file_name)

    # Run the Fierce tool with the given arguments
    run_fierce_tool(args, output_file_path)

if __name__ == "__main__":
    main()
