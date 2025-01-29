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
    # Initialize the results dictionary
    services = {}

    # Check for MySQL version
    if "mysql" in output.lower():
        version_match = re.search(r"mysql.*?version\s*([^\s]+)", output, re.IGNORECASE)
        if version_match:
            services["mysql_version"] = version_match.group(1)
        else:
            services["mysql_version"] = "Version not detected"
    
    # Check for MongoDB info
    if "mongodb" in output.lower():
        services["mongodb"] = "MongoDB detected"
        db_match = re.findall(r"Database:\s*(\S+)", output)
        if db_match:
            services["mongodb_databases"] = db_match
        else:
            services["mongodb_databases"] = "No databases found"
    
    # Check for Redis info
    if "redis" in output.lower():
        services["redis"] = "Redis detected"
    
    # Check for PostgreSQL info
    if "postgresql" in output.lower():
        services["postgresql"] = "PostgreSQL detected"
        version_match = re.search(r"PostgreSQL\s*version\s*([^\s]+)", output, re.IGNORECASE)
        if version_match:
            services["postgresql_version"] = version_match.group(1)
        else:
            services["postgresql_version"] = "Version not detected"
    
    # Check for MSSQL info
    if "mssql" in output.lower():
        services["mssql"] = "MSSQL detected"
        version_match = re.search(r"Microsoft\s*SQL\s*Server\s*version\s*([^\s]+)", output, re.IGNORECASE)
        if version_match:
            services["mssql_version"] = version_match.group(1)
        else:
            services["mssql_version"] = "Version not detected"

    # Check for Oracle DB info
    if "oracle" in output.lower():
        services["oracle"] = "Oracle detected"
        version_match = re.search(r"Oracle\s*version\s*([^\s]+)", output, re.IGNORECASE)
        if version_match:
            services["oracle_version"] = version_match.group(1)
        else:
            services["oracle_version"] = "Version not detected"

    return services

# Run Nmap scan and return structured data
def run_nmap_scan(target):
    scan_data = {}

    try:
        # Full DB Service Scan (MySQL, PostgreSQL, MSSQL, Oracle, MongoDB, Redis)
        full_scan = subprocess.run(
            ["nmap", "-p", "3306,5432,1433,1521,27017,6379", "--script=mysql-info,mongodb-info,postgresql-info,mssql-info,oracle-info", target],
            capture_output=True, text=True)

        # Parse the Nmap output
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
