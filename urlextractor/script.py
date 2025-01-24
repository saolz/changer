import os
import argparse
import subprocess
import datetime
from pathlib import Path

def create_output_dir(base_dir, user_id, target):
    # Get the current timestamp in IST
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    base_path = Path(base_dir) / f"toolname_results/toolname_{user_id}_{timestamp}"

    # Check if directory already exists
    n = 1
    final_path = base_path
    while final_path.exists():
        final_path = Path(f"{base_path}_{n}")
        n += 1

    # Create the directory
    final_path.mkdir(parents=True, exist_ok=True)
    return final_path, timestamp

def main():
    parser = argparse.ArgumentParser(description="Automate URLextractor usage.")
    parser.add_argument("target", help="The target URL, file, or directory to process.")
    parser.add_argument("-u", "--user", required=True, help="User ID.")
    parser.add_argument("-o", "--output", help="Optional output directory.")
    args = parser.parse_args()

    target = args.target
    user_id = args.user
    output_dir = args.output

    # Set default output directory if not provided
    if not output_dir:
        output_dir = os.getcwd()

    # Create the output directory structure
    final_dir, timestamp = create_output_dir(output_dir, user_id, target)
    output_file = final_dir / f"toolname_{user_id}_{timestamp}_{target.replace('/', '_')}.json"

    try:
        # Run the tool command
        command = ["./extractor.sh", target]
        with open(output_file, "w") as out_file:
            subprocess.run(command, stdout=out_file, stderr=subprocess.PIPE, check=True)

        print(f"Results saved to: {output_file}")

    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running the tool: {e.stderr.decode()}")

    except Exception as e:
        print(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    main()
