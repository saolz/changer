import os
import subprocess
import argparse
import datetime

def create_output_folder(base_folder, user_id):
    """Create the main tool folder and user-specific folder."""
    try:
        # Create the main tool folder if it doesn't exist
        if not os.path.exists(base_folder):
            os.makedirs(base_folder)

        # Create user-specific folder with timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        user_folder = os.path.join(base_folder, f"{user_id}_{timestamp}")
        os.makedirs(user_folder)

        return user_folder
    except Exception as e:
        print(f"Error creating output folder: {e}")
        exit(1)

def construct_sqlmap_command(args, output_file):
    """Construct the sqlmap command based on provided arguments."""
    try:
        command = ["sqlmap"]

        if args.url:
            command.extend(["-u", args.url])
        if args.data:
            command.extend(["--data", args.data])
        if args.cookie:
            command.extend(["--cookie", args.cookie])
        if args.random_agent:
            command.append("--random-agent")
        if args.proxy:
            command.extend(["--proxy", args.proxy])
        if args.tor:
            command.append("--tor")
        if args.check_tor:
            command.append("--check-tor")
        if args.dbms:
            command.extend(["--dbms", args.dbms])
        if args.level:
            command.extend(["--level", str(args.level)])
        if args.risk:
            command.extend(["--risk", str(args.risk)])
        if args.technique:
            command.extend(["--technique", args.technique])

        # Enumeration options
        if args.all:
            command.append("--all")
        if args.banner:
            command.append("--banner")
        if args.current_user:
            command.append("--current-user")
        if args.current_db:
            command.append("--current-db")
        if args.passwords:
            command.append("--passwords")
        if args.dbs:
            command.append("--dbs")
        if args.tables:
            command.append("--tables")
        if args.columns:
            command.append("--columns")
        if args.schema:
            command.append("--schema")
        if args.dump:
            command.append("--dump")
        if args.dump_all:
            command.append("--dump-all")
        if args.db:
            command.extend(["-D", args.db])
        if args.table:
            command.extend(["-T", args.table])
        if args.column:
            command.extend(["-C", args.column])

        # OS Access options
        if args.os_shell:
            command.append("--os-shell")
        if args.os_pwn:
            command.append("--os-pwn")

        # General options
        if args.batch:
            command.append("--batch")
        if args.flush_session:
            command.append("--flush-session")

        # Output redirection
        command.extend(["-o", output_file])

        return command
    except Exception as e:
        print(f"Error constructing sqlmap command: {e}")
        exit(1)

def main():
    """Main function to handle argument parsing and script execution."""
    parser = argparse.ArgumentParser(description="Automate sqlmap tool execution with customized output management.")

    # User-specific arguments
    parser.add_argument("--user_id", required=True, help="User ID for creating specific folder and output files.")
    parser.add_argument("--url", help="Target URL.")
    parser.add_argument("--data", help="Data string for POST requests.")
    parser.add_argument("--cookie", help="HTTP Cookie header value.")
    parser.add_argument("--random_agent", action="store_true", help="Use a random User-Agent header.")
    parser.add_argument("--proxy", help="Proxy URL.")
    parser.add_argument("--tor", action="store_true", help="Use Tor network.")
    parser.add_argument("--check_tor", action="store_true", help="Check Tor network connectivity.")
    parser.add_argument("--dbms", help="Specify back-end DBMS.")
    parser.add_argument("--level", type=int, help="Level of tests (1-5).")
    parser.add_argument("--risk", type=int, help="Risk of tests (1-3).")
    parser.add_argument("--technique", help="SQL injection techniques to use.")

    # Enumeration options
    parser.add_argument("--all", action="store_true", help="Retrieve everything.")
    parser.add_argument("--banner", action="store_true", help="Retrieve DBMS banner.")
    parser.add_argument("--current_user", action="store_true", help="Retrieve current DBMS user.")
    parser.add_argument("--current_db", action="store_true", help="Retrieve current database.")
    parser.add_argument("--passwords", action="store_true", help="Enumerate DBMS user passwords.")
    parser.add_argument("--dbs", action="store_true", help="Enumerate DBMS databases.")
    parser.add_argument("--tables", action="store_true", help="Enumerate DBMS tables.")
    parser.add_argument("--columns", action="store_true", help="Enumerate DBMS columns.")
    parser.add_argument("--schema", action="store_true", help="Enumerate DBMS schema.")
    parser.add_argument("--dump", action="store_true", help="Dump DBMS data.")
    parser.add_argument("--dump_all", action="store_true", help="Dump all DBMS data.")
    parser.add_argument("--db", help="Specific database to enumerate.")
    parser.add_argument("--table", help="Specific table to enumerate.")
    parser.add_argument("--column", help="Specific column to enumerate.")

    # OS Access
    parser.add_argument("--os_shell", action="store_true", help="Open OS shell.")
    parser.add_argument("--os_pwn", action="store_true", help="Prompt for Meterpreter/VNC.")

    # General options
    parser.add_argument("--batch", action="store_true", help="Run in batch mode.")
    parser.add_argument("--flush_session", action="store_true", help="Flush session data.")

    # Output management
    parser.add_argument("--output", help="Path to output file.")

    args = parser.parse_args()

    # Base tool folder
    tool_folder = "sqlmap_tool"

    # Create output folder
    user_output_folder = create_output_folder(tool_folder, args.user_id)

    # Generate output file name if not provided
    if not args.output:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        args.output = os.path.join(
            user_output_folder, f"sqlmap_{args.user_id}_{timestamp}.csv"
        )

    # Construct sqlmap command
    sqlmap_command = construct_sqlmap_command(args, args.output)

    # Execute the sqlmap command
    try:
        print(f"Running command: {' '.join(sqlmap_command)}")
        subprocess.run(sqlmap_command)
        print(f"Output saved to: {args.output}")
    except Exception as e:
        print(f"Error running sqlmap: {e}")

if __name__ == "__main__":
    main()
