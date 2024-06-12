# DuplicateFileRemoval

## Description
This script deletes duplicate files in a specified directory based on their checksums. It logs the names of the deleted files and sends an email with the log file attached.

## Command Line Options
- `DuplicateFileRemoval.py <directory_path> <interval_minutes> <email_id>`
  - `<directory_path>`: Absolute path of the directory which may contain duplicate files.
  - `<interval_minutes>`: Time interval in minutes after which the script performs the duplicate file removal.
  - `<email_id>`: Email ID of the receiver for the log file.

## Usage
python DuplicateFileRemoval.py E:/Data/Demo 50 admin123@gmail.com


## Dependencies
- `hashlib`
- `os`
- `time`
- `smtplib`
- `email`
- `argparse`
- `schedule`
