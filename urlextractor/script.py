# script.py
import os
import argparse
import subprocess
import datetime
from pathlib import Path

def create_output_dir(base_dir, user_id, target):
    # Get the current timestamp in IST
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    base_path = Path(base_dir) / f"urlextractor_results/{user_id}_{timestamp}"

    # Check if directory already exists
    n = 1
    final_path = base_path
    while final_path.exists():
        final_path = Path(f"{base_path}_{n}")
        n += 1

    # Create the directory
    final_path.mkdir(parents=True, exist_ok=True)
    return final_path, timestamp

def process_tool_output(raw_output):
    # Convert raw tool output to a readable JSON-like format
    lines = raw_output.splitlines()
    processed_output = {"info": []}

    for line in lines:
        if line.strip():
            processed_output["info"].append(line.strip())

    return processed_output

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
    output_file = final_dir / f"urlextractor_{user_id}_{timestamp}_{target.replace('/', '_')}.json"

    try:
        # Run the tool command
        command = ["./extractor.sh", target]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)

        # Process tool output to make it readable
        processed_output = process_tool_output(result.stdout)

        # Save the processed output to the JSON file
        with open(output_file, "w") as out_file:
            import json
            json.dump(processed_output, out_file, indent=4)

        print(f"Results saved to: {output_file}")

    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running the tool: {e.stderr}")

    except Exception as e:
        print(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    main()
