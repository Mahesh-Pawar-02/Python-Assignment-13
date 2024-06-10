import hashlib
import os
import time
import urllib.error
import urllib.request
import smtplib
from sys import argv
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

def is_connected():
    try:
        urllib.request.urlopen('https://www.google.co.in/', timeout=1)
        return True
    except urllib.error.URLError:
        return False

def MailSender(filename, time):
    try:
        fromaddr = "try.web.new@gmail.com"
        toaddr = "jayshripawar8329@gmail.com"

        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr

        body = f"""
        Hello..!
        Greeting from Mahesh Pawar.
        Please find the attached document which contains Log of Deleted Duplicate files.
        Log File is created at: {time}

        Starting time of scanning:
        Total number of files scanned:
        Total number of duplicate files found:

        This is an auto-generated mail.

        Thanks and Regards,
        Mahesh Pawar
        RID: PM0100047
        +91 9322150275
        """
        
        subject = f"Deleted Duplicate file Log generated at: {time}"
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        with open(filename, "rb") as attachment:
            p = MIMEBase('application', 'octet-stream')
            p.set_payload(attachment.read())
        
        encoders.encode_base64(p)
        p.add_header('Content-Disposition', f"attachment; filename={os.path.basename(filename)}")
        msg.attach(p)
        
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(fromaddr, "qvbp xnrv pbcb pxaf")
        text = msg.as_string()
        s.sendmail(fromaddr, toaddr, text)
        s.quit()

        print("Log file successfully sent through mail...")

    except Exception as E:
        print("Unable to send mail", E)

def LogFile(logPath, duplicateFiles=[]):
    timestamp = time.ctime().replace(" ", "").replace(":", "").replace("/", "_")
    separator = "-" * 80
    
    with open(logPath, 'w') as f:
        f.write(separator + "\n")
        f.write("Welcome..! to Log File\n")
        f.write(f"Log File created at: {time.ctime()}\n")
        f.write(separator + "\n")
        f.write("Deleted Duplicate files are:\n")
        f.write(separator + "\n")

        for element in duplicateFiles:
            f.write(f"{element}\n")

        f.write(separator + "\n")

    print(f"Log File is successfully generated at location {logPath}")

    if is_connected():
        StartTime = time.time()
        MailSender(logPath, time.ctime())
        endTime = time.time()
        print(f"Took {endTime - StartTime} seconds to send email")
    else:
        print("There is no internet connection")

def DeleteFiles(dict1):
    results = list(filter(lambda x: len(x) > 1, dict1.values()))
    duplicateFiles = []

    if len(results) > 0:
        for result in results:
            for i, subresult in enumerate(result):
                if i >= 1:
                    os.remove(subresult)
                    duplicateFiles.append(subresult)
    else:
        print("No duplicate files found...")
    
    return duplicateFiles

def hashfile(path, blocksize=1024):
    hasher = hashlib.md5()
    with open(path, 'rb') as afile:
        buf = afile.read(blocksize)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(blocksize)
    return hasher.hexdigest()

def FindDuplicate(path):
    if not os.path.isabs(path):
        path = os.path.abspath(path)
    
    exists = os.path.isdir(path)
    dups = {}

    if exists:
        for DirName, SubDir, fileList in os.walk(path):
            for filen in fileList:
                filePath = os.path.join(DirName, filen)
                FileHash = hashfile(filePath)
                if FileHash in dups:
                    dups[FileHash].append(filePath)
                else:
                    dups[FileHash] = [filePath]
        return dups
    else:
        print("Invalid path...")

def PrintResults(dict1):
    results = list(filter(lambda x: len(x) > 1, dict1.values()))

    if len(results) > 0:
        print("Duplicate Found:")
        print("The following files are identical:")

        for result in results:
            for subresult in result[1:]:
                print(f'\t\t{subresult}')
    else:
        print("No duplicate files found...")

def main():
    print('-------------------------------------------------------------------')
    print("Created by Mahesh Pawar")
    print(f"Application name: {argv[0]}")
    print('-------------------------------------------------------------------')

    if len(argv) != 2:
        print("Error: Invalid number of arguments")
        print("Use -h option to get the help and use -u option to get the usage of application")
        exit()

    if argv[1] in ("-h", "-H"):
        print("This script is used to traverse a specific directory and delete duplicate files")
        exit()

    if argv[1] in ("-u", "-U"):
        print("usage: ApplicationName AbsolutePath_of_Directory")
        exit()

    try:
        StartTime = time.time()
        arr = FindDuplicate(argv[1])
        PrintResults(arr)
        duplicateFiles = DeleteFiles(arr)
        LogFile("Log.txt", duplicateFiles)
        EndTime = time.time()
        print(f"This app Took total {EndTime - StartTime} seconds to evaluate.")

    except ValueError:
        print("Error: Invalid datatype of input")

    except Exception as E:
        print("Error: Invalid input", E)

if __name__ == "__main__":
    main()