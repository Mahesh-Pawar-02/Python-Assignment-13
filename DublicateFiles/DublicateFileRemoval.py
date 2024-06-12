import sys
import time
import schedule
from duplicate_removal_module import *

def main():
    if len(sys.argv) != 4:
        print("Usage: python script.py <directory> <interval> <email>")
        sys.exit(1)

    directory = sys.argv[1]
    interval = sys.argv[2]
    email = sys.argv[3]


    try:
        validate_directory(directory)
        validate_interval(interval)
        validate_email(email)
        print(email,"this email verified successfuly..")
        print("wait for deleting dublicate file from",directory)

        interval_minutes = int(interval)
        
        schedule.every(interval_minutes).minutes.do(main_task, directory, email)

        while True:
            schedule.run_pending()
            time.sleep(1)
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
