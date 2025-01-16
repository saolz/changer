import os
import subprocess
import argparse
import datetime
import pytz

# Function to create the output directory
def create_output_directory(base_directory, user_id):
    try:
        # Setting IST timezone
        ist = pytz.timezone("Asia/Kolkata")
        current_time = datetime.datetime.now(ist).strftime("%Y-%m-%d_%H-%M-%S")
        user_folder = f"{user_id}_{current_time}"
        output_directory = os.path.join(base_directory, user_folder)
        os.makedirs(output_directory, exist_ok=True)
        return output_directory
    except Exception as e:
        raise Exception(f"Error creating output directory: {e}")

# Function to convert .kismet logs to CSV
def convert_kismet_to_csv(kismet_log, csv_output):
    try:
        cmd = ["kismetdb_to_csv", "--in", kismet_log, "--out", csv_output]
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"[SUCCESS] Converted {kismet_log} to {csv_output}")
    except subprocess.CalledProcessError as e:
        raise Exception(f"Error during Kismet log to CSV conversion: {e.stderr.decode().strip()}")
    except Exception as e:
        raise Exception(f"Unexpected error while converting log: {e}")

# Main function
def main():
    parser = argparse.ArgumentParser(description="Kismet Log Processor: Convert .kismet logs to CSV format")
    
    # Define arguments
    parser.add_argument("-u", "--user_id", required=True, help="User ID for folder organization")
    parser.add_argument("-l", "--kismet_log", required=True, help="Path to the .kismet log file")
    parser.add_argument("-o", "--output", help="Base directory for storing results (optional)")

    args = parser.parse_args()

    # Default base directory for results
    base_directory = args.output if args.output else os.path.join(os.getcwd(), "kismet_results")
    
    try:
        # Create the output directory for this session
        output_directory = create_output_directory(base_directory, args.user_id)
        print(f"[INFO] Output directory created: {output_directory}")

        # Prepare the output CSV file name
        ist = pytz.timezone("Asia/Kolkata")
        current_time = datetime.datetime.now(ist).strftime("%Y-%m-%d_%H-%M-%S")
        csv_output = os.path.join(output_directory, f"kismet_{args.user_id}_{current_time}.csv")

        # Convert the .kismet log to CSV
        convert_kismet_to_csv(args.kismet_log, csv_output)
        print(f"[INFO] CSV saved to: {csv_output}")

    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == "__main__":
    main()
