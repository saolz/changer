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
            results[key] = output.strip() if output.strip() else "No data returned"
        except subprocess.CalledProcessError:
            results[key] = "Error running Nmap"
    
    return results

def save_results(tool_name, user, target, results, output_dir=None):
    """
    Saves the raw scan results in a structured JSON file.
    """
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    default_dir = f"./{tool_name}_results/{tool_name}_{user}_{timestamp}/"
    output_directory = output_dir if output_dir else default_dir

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    output_file = f"{output_directory}{tool_name}_{user}_{timestamp}_{target}.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=4)

    print(f"Results saved to {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Automate Nmap database scanning.")
    parser.add_argument("--target", required=True, help="Target IP or domain")
    parser.add_argument("-u", required=True, help="User ID")
    parser.add_argument("-o", help="Optional output directory")

    args = parser.parse_args()
    tool_name = "NMAP"

    print(f"Running Nmap scan on {args.target}...")
    nmap_results = run_nmap_scan(args.target)
    
    save_results(tool_name, args.u, args.target, nmap_results, args.o)

if __name__ == "__main__":
    main()
