import subprocess
import re

# Function to parse output and extract relevant details
def parse_nmap_output(scan_type, output):
    # Searching for MySQL version
    if scan_type == "mysql_version":
        match = re.search(r"Version: (.*)", output)
        if match:
            return match.group(1)
        else:
            return "MySQL version not detected"

    # Searching for MySQL users
    elif scan_type == "mysql_users":
        match = re.search(r"Users: (.*)", output)
        if match:
            return match.group(1)
        else:
            return "No MySQL users found"

    # Searching for MySQL databases
    elif scan_type == "mysql_databases":
        match = re.search(r"Databases: (.*)", output)
        if match:
            return match.group(1)
        else:
            return "No MySQL databases found"
    
    # Searching for database services
    elif scan_type == "database_services":
        if "3306/tcp" in output:
            return "MySQL detected"
        elif "5432/tcp" in output:
            return "PostgreSQL detected"
        elif "1433/tcp" in output:
            return "MSSQL detected"
        elif "1521/tcp" in output:
            return "Oracle detected"
        else:
            return "No database services detected"

    return "Scan result not recognized"

# Run Nmap scan and parse results
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

# Main function
def main():
    target = "testphp.vulnweb.com"
    scan_data = run_nmap_scan(target)
    print(scan_data)

if __name__ == "__main__":
    main()
