import os
import json
import argparse
import subprocess
import datetime

def run_nmap_scan(target):
    """
    Runs Nmap scans for MySQL version, MySQL users, MySQL databases, and other database services.
    """
    commands = {
        "mysql_version": f"nmap -p 3306 --script=mysql-info {target}",
        "mysql_users": f"nmap -p 3306 --script=mysql-users --script-args=mysqluser=root {target}",
        "mysql_databases": f"nmap -p 3306 --script=mysql-databases --script-args=mysqluser=root {target}",
        "db_services": f"nmap -p 3306,5432,1433,1521 -sV {target}"  # MySQL, PostgreSQL, MSSQL, Oracle
    }

    results = {}
    for key, cmd in commands.items():
        try:
            output = subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL, text=True)
            results[key] = output.strip() if output.strip() else "Not detected"
        except subprocess.CalledProcessError:
            results[key] = "Not detected"
    
    return results

def parse_nmap_output(nmap_results):
    """
    Parses the Nmap output to extract database details.
    """
    parsed_data = {
        "MySQL Version": "Not detected",
        "MySQL Users": "No users found",
        "MySQL Databases": "No databases found",
        "Detected Database Services": []
    }

    if "mysql_version" in nmap_results and "3306/tcp open" in nmap_results["mysql_version"]:
        parsed_data["MySQL Version"] = nmap_results["mysql_version"]

    if "mysql_users" in nmap_results and "3306/tcp open" in nmap_results["mysql_users"]:
        parsed_data["MySQL Users"] = nmap_results["mysql_users"]

    if "mysql_databases" in nmap_results and "3306/tcp open" in nmap_results["mysql_databases"]:
        parsed_data["MySQL Databases"] = nmap_results["mysql_databases"]

    if "db_services" in nmap_results:
        for service in ["MySQL", "PostgreSQL", "MSSQL", "Oracle"]:
            if service.lower() in nmap_results["db_services"].lower():
                parsed_data["Detected Database Services"].append(service)
    
    if not parsed_data["Detected Database Services"]:
        parsed_data["Detected Database Services"] = "No database services detected"

    return parsed_data

def save_results(tool_name, user, target, parsed_data, output_dir=None):
    """
    Saves the scan results in a structured JSON file.
    """
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    default_dir = f"./{tool_name}_results/{tool_name}_{user}_{timestamp}/"
    output_directory = output_dir if output_dir else default_dir

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    output_file = f"{output_directory}{tool_name}_{user}_{timestamp}_{target}.json"
    with open(output_file, "w") as f:
        json.dump(parsed_data, f, indent=4)

    print(f"Results saved to {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Automate Nmap database scanning.")
    parser.add_argument("--target", required=True, help="Target IP or domain")
    parser.add_argument("-u", required=True, help="User ID")
    parser.add_argument("-o", help="Optional output directory")

    args = parser.parse_args()
    tool_name = "db_scan"

    print(f"Running Nmap scan on {args.target}...")
    nmap_results = run_nmap_scan(args.target)
    parsed_data = parse_nmap_output(nmap_results)
    
    save_results(tool_name, args.u, args.target, parsed_data, args.o)

if __name__ == "__main__":
    main()
