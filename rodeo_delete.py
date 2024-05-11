import sys
import os
import argparse
import pandas as pd
from collections import Counter
from Chrome_Session import chromeSession
from util.utilities import runtime

def parse_args():
    parser = argparse.ArgumentParser(
        description="Rodeo script to process containers and perform actions based on the CSV data."
    )
    
    parser.add_argument(
        "CSV_FILE_PATH",
        type=str,
        help="Path to the CSV file containing key-value pairs (containers).",
    )
    
    parser.add_argument(
        "SITE_CODE",
        type=str,
        help="Site code for FCMenu Login",
    )
    
    parser.add_argument(
        "BADGE_ID",
        type=int,
        help="Badge ID to login to FCMenu",
    )
    
    return parser.parse_args()

def load_containers_from_csv(file_path):
    import pandas as pd

    # Read with comma delimiter, expecting at least two columns
    df = pd.read_csv(file_path, delimiter=',', header=None)

    if df.shape[1] < 2:
        raise ValueError("CSV must have at least two columns.")

    return dict(zip(df.iloc[:, 0], df.iloc[:, 1]))

# Step 4: Main function to perform the task
def main():
    # Parse the command line arguments
    args = parse_args()
    
    # Load the containers from the specified CSV
    containers = load_containers_from_csv(args.CSV_FILE_PATH)
    
    # Create the chromeSession with the given session name and ID
    session = chromeSession(args.SITE_CODE, args.BADGE_ID)
    
    try:
        # Loop through the containers and perform the desired action
        for i, (sku, container) in enumerate(containers.items(), start=1):
            print(f"{i}/{len(containers)}) {container} :: {sku} // {runtime(session.rodeo_delete, container, sku)}")
    finally:
        # Ensure the session is closed
        session.close()

# Step 5: Ensure the script executes if called directly
if __name__ == "__main__":
    main()
