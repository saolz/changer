import os
import sys
import argparse
import subprocess
import datetime
import pytz

# Function to handle the creation of directories
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

# Function to construct the DNSRecon command and execute it
def run_dnsrecon(args, output_file):
    try:
        # Base command
        cmd = ["dnsrecon"]

        # Adding options based on user input
        if args.domain:
            cmd.extend(["-d", args.domain])
        if args.ns_server:
            cmd.extend(["-n", args.ns_server])
        if args.range:
            cmd.extend(["-r", args.range])
        if args.dictionary:
            cmd.extend(["-D", args.dictionary])
        if args.force:
            cmd.append("-f")
        if args.axfr:
            cmd.append("-a")
        if args.standard:
            cmd.append("-s")
        if args.bind_version:
            cmd.append("-b")
        if args.dnssec:
            cmd.append("-y")
        if args.check_ns:
            cmd.append("-k")
        if args.whois:
            cmd.append("-w")
        if args.nsec3:
            cmd.append("-z")
        if args.threads:
            cmd.extend(["--threads", str(args.threads)])
        if args.lifetime:
            cmd.extend(["--lifetime", str(args.lifetime)])
        if args.tcp:
            cmd.append("--tcp")
        if args.db:
            cmd.extend(["--db", args.db])
        if args.xml:
            cmd.extend(["-x", args.xml])
        if args.csv:
            cmd.extend(["-c", args.csv])
        if args.json:
            cmd.extend(["-j", args.json])
        if args.iw:
            cmd.append("--iw")
        if args.disable_check_recursion:
            cmd.append("--disable_check_recursion")
        if args.disable_check_bindversion:
            cmd.append("--disable_check_bindversion")
        if args.type:
            cmd.extend(["-t", args.type])

        # Redirect output to a file
        cmd.extend(["-c", output_file])

        # Execute the command
        subprocess.run(cmd, check=True)
        print(f"DNSRecon command executed successfully. Output saved to {output_file}")
    except Exception as e:
        print(f"Error running DNSRecon: {e}")
        sys.exit(1)

# Main function
def main():
    parser = argparse.ArgumentParser(description="Automated DNSRecon Script")

    # Define arguments
    parser.add_argument("-u", "--user_id", required=True, help="User ID for folder creation")
    parser.add_argument("-o", "--output", help="Output directory for the results")
    parser.add_argument("-d", "--domain", help="Domain to query")
    parser.add_argument("-n", "--ns_server", help="Specify the nameserver")
    parser.add_argument("-r", "--range", help="IP range for reverse lookup")
    parser.add_argument("-D", "--dictionary", help="Path to dictionary file for brute force")
    parser.add_argument("-f", "--force", action="store_true", help="Force continue even on errors")
    parser.add_argument("-a", "--axfr", action="store_true", help="Perform zone transfer")
    parser.add_argument("-s", "--standard", action="store_true", help="Perform standard enumeration")
    parser.add_argument("-b", "--bind_version", action="store_true", help="Check BIND version")
    parser.add_argument("-y", "--dnssec", action="store_true", help="Check DNSSEC configuration")
    parser.add_argument("-k", "--check_ns", action="store_true", help="Check nameservers")
    parser.add_argument("-w", "--whois", action="store_true", help="Perform WHOIS lookup")
    parser.add_argument("-z", "--nsec3", action="store_true", help="Perform NSEC3 walk")
    parser.add_argument("--threads", type=int, help="Number of threads")
    parser.add_argument("--lifetime", type=int, help="Query lifetime in seconds")
    parser.add_argument("--tcp", action="store_true", help="Use TCP for queries")
    parser.add_argument("--db", help="SQLite database for storing results")
    parser.add_argument("-x", "--xml", help="Output in XML format")
    parser.add_argument("-c", "--csv", help="Output in CSV format")
    parser.add_argument("-j", "--json", help="Output in JSON format")
    parser.add_argument("--iw", action="store_true", help="Ignore wildcard resolution")
    parser.add_argument("--disable_check_recursion", action="store_true", help="Disable recursion check")
    parser.add_argument("--disable_check_bindversion", action="store_true", help="Disable BIND version check")
    parser.add_argument("-t", "--type", help="Specify the type of query")

    args = parser.parse_args()

    # Set up base directory
    base_dir = args.output if args.output else os.path.join(os.getcwd(), "dnsrecon_results")

    # Create output directory
    output_dir = create_output_directory(base_dir, args.user_id)

    # Set IST timezone for output file naming
    ist = pytz.timezone("Asia/Kolkata")
    current_time = datetime.datetime.now(ist).strftime("%Y-%m-%d_%H-%M-%S")
    output_file = os.path.join(output_dir, f"dnsrecon_{args.user_id}_{current_time}.csv")

    # Run the DNSRecon command
    run_dnsrecon(args, output_file)

if __name__ == "__main__":
    main()
