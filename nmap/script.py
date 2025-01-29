import argparse
import os
import subprocess
import datetime
import json
import csv
import re

# Get IST timestamp
def get_ist_time():
    ist_time = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)
    return ist_time.strftime("%Y-%m-%d_%H-%M-%S")

# Create output directory
def create_output_directory(tool_name, user, target, base_output_dir=None, file_format="json"):
    timestamp = get_ist_time()
    if base_output_dir:
        output_dir = os.path.join(base_output_dir, f"{tool_name}_{user}_{timestamp}")
    else:
        output_dir = os.path.join(f"{tool_name}_results", f"{tool_name}_{user}_{timestamp}")
    
    os.makedirs(output_dir, exist_ok=True)
    file_extension = "json" if file_format == "json" else "csv"
    return output_dir, os.path.join(output_dir, f"{tool_name}_{user}_{timestamp}_{target}.{file_extension}")

# Parse Nmap output to extract useful information
def parse_nmap_output(output):
    # Regular expressions for extracting useful information
    services = {}
    
    # General Database Services (MySQL, PostgreSQL, MSSQL, Redis, MongoDB)
    db_services = {
        "mysql": "MySQL detected",
        "postgresql": "PostgreSQL detected",
        "mssql": "MSSQL detected",
        "mongodb": "MongoDB detected",
        "redis": "Redis detected",
        "oracle": "Oracle detected"
    }

    for db, db_name in db_services.items():
        if db_name.lower() in output.lower():
            services[db] = db_name
    
    # Extract database version info if available
    version_match = re.search(r"(MySQL|PostgreSQL|MSSQL|MongoDB|Redis|Oracle)\s*version\s*([\d\.]+)", output)
    if version_match:
        services["version"] = version_match.group(2)
    else:
        services["version"] = "Version not detected"
    
    # Extract database users (if mentioned)
    users_match = re.findall(r"User:\s*(\S+)", output)
    services["users"] = users_match if users_match else "No users found"
    
    # Extract database details (schemas, databases, etc.)
    db_match = re.findall(r"Database:\s*(\S+)", output)
    services["databases"] = db_match if db_match else "No databases found"

    return services

# Run Nmap scan and return structured data
def run_nmap_scan(target):
    scan_data = {}

    try:
        # Full DB Service Scan (MySQL, PostgreSQL, MSSQL, Oracle, MongoDB, Redis)
        full_scan = subprocess.run(["nmap", "-p", "3306,5432,1433,1521,27017,6379", "--script=*db*,*nosql*", target],
                                   capture_output=True, text=True)
        scan_data["database_services"] = parse_nmap_output(full_scan.stdout)

    except Exception as e:
        scan_data["error"] = str(e)

    return scan_data

# Save results in JSON format
def save_as_json(data, output_path):
    with open(output_path, "w") as f:
        json.dump(data, f, indent=4)
    print(f"[+] JSON results saved: {output_path}")

# Save results in CSV format
def save_as_csv(data, output_path):
    with open(output_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Category", "Result"])
        for key, value in data.items():
            writer.writerow([key, value])
    print(f"[+] CSV results saved: {output_path}")

# Main function
def main():
    parser = argparse.ArgumentParser(description="Automated Nmap Database Scanner")
    parser.add_argument("--target", required=True, help="Target IP address or hostname")
    parser.add_argument("-u", required=True, help="User ID")
    parser.add_argument("-o", help="Optional output directory")
    parser.add_argument("-f", choices=["json", "csv"], default="json", help="Output format (json/csv)")

    args = parser.parse_args()

    tool_name = "nmap_scan"
    output_dir, output_path = create_output_directory(tool_name, args.u, args.target, args.o, args.f)

    print(f"[+] Scanning target: {args.target}")
    print(f"[+] Saving results to: {output_path}")

    scan_data = run_nmap_scan(args.target)

    if args.f == "json":
        save_as_json(scan_data, output_path)
    else:
        save_as_csv(scan_data, output_path)

if __name__ == "__main__":
    main()
