import os
import argparse
import subprocess
import time

def create_output_folder(base_folder, tool_name, user_id, timestamp):
    # Ensure the parent folder 'toolname_results' exists
    results_folder = os.path.join(base_folder, f"{tool_name}_results")
    os.makedirs(results_folder, exist_ok=True)

    # Create the user-specific folder within 'toolname_results'
    user_folder = os.path.join(results_folder, f"{tool_name}_{user_id}_{timestamp}")
    os.makedirs(user_folder, exist_ok=True)
    
    return user_folder

def run_trufflehog3(target, output_file):
    try:
        # Construct the command with additional options
        command = [
            "trufflehog3", "--no-history", "--format", "JSON",
            target
        ]
        print(f"Executing command: {' '.join(command)}")  # Log the command for debugging
        
        result = subprocess.run(command, capture_output=True, text=True)
        
        # Print stdout and stderr for further debugging
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
        
        # Handle empty output
        if result.stdout.strip():
            with open(output_file, "w") as f:
                f.write(result.stdout)
        else:
            with open(output_file, "w") as f:
                f.write('{"message": "No secrets found"}')
        return f"Results saved to {output_file}"
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Trufflehog3 failed: {e.stderr.strip()}")
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise

def main():
    parser = argparse.ArgumentParser(description="Automate trufflehog3 scanning.")
    parser.add_argument("target", help="Target to scan (e.g., https://github.com/saolz/changer)")
    parser.add_argument("-u", "--user", required=True, help="User ID for organizing outputs")
    parser.add_argument("-o", "--output", help="Base output folder (default: current directory)")
    args = parser.parse_args()

    # Fix URL parsing
    if not args.target.startswith("http://") and not args.target.startswith("https://"):
        raise ValueError("Target URL must start with 'http://' or 'https://'")

    tool_name = "trufflehog3"
    base_folder = args.output if args.output else os.getcwd()
    ist_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())

    try:
        user_folder = create_output_folder(base_folder, tool_name, args.user, ist_time)
        json_filename = f"{tool_name}_{args.user}_{ist_time}_output.json"
        json_filepath = os.path.join(user_folder, json_filename)

        result = run_trufflehog3(args.target, json_filepath)
        print(result)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

if __name__ == "__main__":
    main()
