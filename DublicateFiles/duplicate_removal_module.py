import os
import hashlib
import time
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def calculate_checksum(file_path):
    try:
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception as e:
        print(f"Error calculating checksum for {file_path}: {str(e)}")
        return None

def find_duplicates(directory):
    try:
        checksums = {}
        duplicates = []
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                checksum = calculate_checksum(file_path)
                if checksum in checksums:
                    duplicates.append(file_path)
                else:
                    checksums[checksum] = file_path
        return duplicates
    except Exception as e:
        print(f"Error finding duplicates in {directory}: {str(e)}")
        return []

def delete_files(files):
    try:
        for file in files:
            os.remove(file)
            print(f"Deleted duplicate file: {file}")
    except Exception as e:
        print(f"Error deleting file {file}: {str(e)}")

def send_email(log_file, email_id, stats):
    try:
        msg = MIMEMultipart()
        msg['From'] = "try.web.new@gmail.com"
        msg['To'] = email_id
        msg['Subject'] = "Duplicate File Removal Log"

        body = f"""\
    Hello..!

    Greeting from Mahesh Pawar.
    Please find the attached document which contains Log of Deleted Dublicate file.
    
    Starting time of scanning: {stats['start_time']}
    Total number of files scanned: {stats['files_scanned']}
    Total number of duplicate files found: {stats['duplicates_found']} 

    NOTE : This is auto generated mail.

    Thanks and Regards,

    Mahesh Dinkar Pawar
    +91 9322150275"""
        msg.attach(MIMEText(body, 'plain'))

        with open(log_file, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename= {os.path.basename(log_file)}")
        msg.attach(part)

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login("try.web.new@gmail.com",  "qvbp xnrv pbcb pxaf")
            server.sendmail("try.web.new@gmail.com", email_id, msg.as_string())
    except Exception as e:
        print(f"Error sending email to {email_id}: {str(e)}")

def validate_directory(directory):
    if not os.path.isdir(directory):
        raise ValueError(f"Invalid directory: {directory}")

def validate_email(email):
    if "@" not in email or "." not in email.split("@")[1]:
        raise ValueError(f"Invalid email address: {email}")

def validate_interval(interval):
    if not interval.isdigit() or int(interval) <= 0:
        raise ValueError(f"Invalid interval: {interval}")

def main_task(directory, email_id):
    start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"Scanning started at: {start_time}")
    try:
        all_files = [os.path.join(root, file) for root, _, files in os.walk(directory) for file in files]
        duplicates = find_duplicates(directory)
        delete_files(duplicates)
        
        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"Scanning ended at: {end_time}")
        
        stats = {
            "start_time": start_time,
            "end_time": end_time,
            "files_scanned": len(all_files),
            "duplicates_found": len(duplicates)
        }
        
        print(f"Total files scanned: {stats['files_scanned']}")
        print(f"Total duplicate files found: {stats['duplicates_found']}")

        log_file = "Marvellous/duplicate_removal_log.txt"
        write_stats_to_file(log_file, stats)
        send_email(log_file, email_id, stats)
    except Exception as e:
        print(f"Error in main_task: {str(e)}")

def write_stats_to_file(file_path, stats):
    try:
        with open(file_path, 'w') as f:
            f.write("Duplicate File Removal Operation\n")
            f.write("---------------------------------\n")
            f.write(f"Starting time of scanning: {stats['start_time']}\n")
            f.write(f"Ending time of scanning: {stats['end_time']}\n")
            f.write(f"Total number of files scanned: {stats['files_scanned']}\n")
            f.write(f"Total number of duplicate files found: {stats['duplicates_found']}\n")
    except Exception as e:
        print(f"Error writing stats to file: {str(e)}")

def ProcessLog(log_dir="Marvellous"):
    duplicates = []
    if not os.path.exists(log_dir):
        try:
            os.mkdir(log_dir)
        except:
            pass

    separator = "_"*80
    log_path = os.path.join(log_dir, "DuplicateFile.log")
    with open(log_path, "w") as f:
        f.write(separator + "\n")
        f.write("Welcome..! to Log File "+"\n")
        f.write("Log File created at : "+time.ctime()+"\n")
        f.write(separator + "\n")
        f.write("Deleted Duplicate files are : " + "\n")
        f.write(separator + "\n")

        for element in duplicates:
            f.write("%s\n" % element)

    print("Log File is successfully generated at location:", log_path)