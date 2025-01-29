import subprocess
import argparse
import re
import json

# Function to parse Nmap scan results
def parse_nmap_output(scan_type, output):
    # Example pattern to look for versions or other valuable info
    if scan_type == "database_services":
        if "3306/tcp" in output:
            return "MySQL detected"
        if "5432/tcp" in output:
            return "PostgreSQL detected"
        if "1433/tcp" in output:
            return "MSSQL detected"
        if "1521/tcp" in output:
            return "Oracle detected"
        return "No database services detected"

    # Look for version information
    if "version" in output:
        match = re.search(r"Version: (\S+)", output)
        if match:
            return match.group(1)
    return "Version not detected"

# Run Nmap scan
def run_nmap_scan(target):
    scan_data = {}

    try:
        # MySQL Version Scan
        version_scan = subprocess.run(
            ["nmap", "-p", "3306", "--script=mysql-info", target],
            capture_output=True, text=True)
        scan_data["mysql_version"] = parse_nmap_output("mysql_version", version_scan.stdout)

        # MySQL Users Enumeration
        user_scan = subprocess.run(
            ["nmap", "-p", "3306", "--script=mysql-users", target],
            capture_output=True, text=True)
        scan_data["mysql_users"] = parse_nmap_output("mysql_users", user_scan.stdout)

        # MySQL Database Enumeration
        db_scan = subprocess.run(
            ["nmap", "-p", "3306", "--script=mysql-databases", target],
            capture_output=True, text=True)
        scan_data["mysql_databases"] = parse_nmap_output("mysql_databases", db_scan.stdout)

        # Full DB Service Scan (MySQL, PostgreSQL, MSSQL, Oracle)
        full_scan = subprocess.run(
            ["nmap", "-p", "3306,5432,1433,1521", "--script=*db*", target],
            capture_output=True, text=True)
        scan_data["database_services"] = parse_nmap_output("database_services", full_scan.stdout)

    except Exception as e:
        scan_data["error"] = str(e)

    return scan_data

# Main function to handle arguments and trigger the scan
def main():
    parser = argparse.ArgumentParser(description="Automated Nmap Database Scanner")
    parser.add_argument("target", help="Target IP address or hostname")
    parser.add_argument("-u", required=True, help="User ID")

    args = parser.parse_args()

    print(f"[+] Scanning target: {args.target}")

    scan_data = run_nmap_scan(args.target)

    # Output the scan data in JSON format
    print(json.dumps(scan_data, indent=4))

if __name__ == "__main__":
    main()
