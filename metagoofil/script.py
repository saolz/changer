import os
import argparse
import time
import json
from datetime import datetime
from pytz import timezone  # Add this import
import shutil

# Function to create output directory if not exists
def create_output_directory(output_dir, folder_name):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    counter = 1
    new_folder_name = folder_name
    while os.path.exists(new_folder_name):
        new_folder_name = f"{folder_name}_{counter}"
        counter += 1
    os.makedirs(new_folder_name)
    return new_folder_name

# Function to format timestamp in IST (Indian Standard Time)
def get_timestamp():
    timestamp = datetime.now().astimezone(timezone('Asia/Kolkata')).strftime('%Y-%m-%d_%H-%M-%S')
    return timestamp

# Function to run the tool (Metagoofil in your case)
def run_tool(target, user_id, output_dir):
    timestamp = get_timestamp()
    folder_name = f"toolname_{user_id}_{timestamp}"
    if not output_dir:
        output_dir = os.path.join(os.getcwd(), "toolname_results")
    final_output_dir = create_output_directory(output_dir, folder_name)
    output_file = os.path.join(final_output_dir, f"toolname_{user_id}_{timestamp}_{target}.json")
    
    # Here you'd call the actual Metagoofil script using subprocess or similar
    # For the sake of this example, assume it's just a placeholder
    tool_output = {"target": target, "user_id": user_id, "timestamp": timestamp}
    
    # Saving results to a JSON file
    with open(output_file, 'w') as json_file:
        json.dump(tool_output, json_file, indent=4)
    
    print(f"Results saved in: {output_file}")

# Main function to handle argparse and the script's logic
def main():
    parser = argparse.ArgumentParser(description="Automate Metagoofil tool usage")
    parser.add_argument('target', help='Target (URL, file, or directory)')
    parser.add_argument('-u', '--user', required=True, help='User ID')
    parser.add_argument('-o', '--output', help='Output directory (optional)')

    args = parser.parse_args()
    
    try:
        run_tool(args.target, args.user, args.output)
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)

if __name__ == "__main__":
    main()
