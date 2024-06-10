
import hashlib
import os
import time
import urllib.error
import urllib.request
import smtplib
from sys import *
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

def is_connected():
    try:
        urllib.request.urlopen('https://www.google.co.in/',timeout = 1)
        return True
    except urllib.error as err:
        return False
def MailSender(filename, time):
    try:
        fromaddr = "try.web.new@gmail.com"
        toaddr = "maheshpawar7846@gmail.com"

        msg = MIMEMultipart()

        msg['From'] = fromaddr
        msg['To'] = toaddr

        body = """
    Hello..!
    Greeting from Mahesh Pawar.
    Please find the attached document which contains Log of Deleted Dublicate file.
    Log File is created at : %s

    Starting time of scanning : 
    Total number of file scaned : 
    Total number of files dublicate files found : 

    This is auto generated mail.

    Thanks and Regards,

    Mahesh Pawar
    RID : PM0100047
    +91 9322150275
    """ %(time)

        Subject = """
        Deleted Dublicate file Log generated at : %s
        """%(time)

        msg['Subject'] = Subject
        msg.attach(MIMEText(body,'plain'))
        attachment = open(filename,"rb")
        p = MIMEBase('application','octet-stream')
        p.set_payload((attachment).read())
        encoders.encode_base64(p)
        p.add_header('Content-Disposition', "attachment; filename = %s" %filename)
        msg.attach(p)
        s = smtplib.SMTP('smtp.gmail.com',587)
        s.starttls()
        s.login(fromaddr,"qvbp xnrv pbcb pxaf")
        text = msg.as_string()
        s.sendmail(fromaddr,toaddr,text)
        s.quit()

        print("Log file successfully sent through mail...")

    except Exception as E:
        print("Unable to send mail", E)


def LogFile(logDir, duplicateFiles = []):

    timestamp = time.ctime()
    timestamp = timestamp.replace(" ","")
    timestamp = timestamp.replace(":","_")
    timestamp = timestamp.replace("/","_")

    separator = "-"*50

    with open(logDir,"w") as f:
        f.write(separator + "\n")
        f.write("Welcome..! to Log File "+"\n")
        f.write("Log File created at : "+time.ctime()+"\n")
        f.write(separator + "\n")
        f.write("Deleted Dublicate file are : " + "\n")
        f.write(separator + "\n")

        for element in duplicateFiles:
            f.write("%s\n"%element)

        f.write("\n\n")
        f.write(separator + "\n")

    print("Log File is successfully generated at location %s",(logDir))

    connected = is_connected()
 
    if connected:
        StartTime = time.time()
        MailSender(logDir,time.ctime())
        endTime = time.time()

        print("Took %s seconds to send email"%(endTime-StartTime))
    else:
        print("There is a no internet connection")

    f.close()

def DeleteFiles(dict1):
    results = list(filter(lambda x:len(x) > 1, dict1.values()))
    iCnt = 0

    duplicateFiles = []

    if len(results) > 0:
        for result in results:
            for subresult in result:
                iCnt = iCnt + 1
                if iCnt >= 2:
                    os.remove(subresult)
                    duplicateFiles.append(subresult)
            iCnt = 0
    else:
        print("No dublicate files found...")
    return duplicateFiles

def hashfile(path, blocksize = 1024):
    afile = open(path, 'rb')
    hasher = hashlib.md5()
    buf = afile.read(blocksize)

    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    afile.close()
    return hasher.hexdigest()

def FindDublicate(path):
    flag = os.path.isabs(path)
    if flag == False:
        path = os.path.abspath(path)
    
    exists = os.path.isdir(path)

    dups = {}
    if exists:
        for DirName, SubDir, fileList in os.walk(path):
            print('\n-------------------------------------------------------------------')

            for filen in fileList:
                path = os.path.join(DirName,filen)
                FileHash = hashfile(path)
                if FileHash in dups:
                    dups[FileHash].append(path)
                else:
                    dups[FileHash] = [path]
        return dups
    else:
        print("Invalid path...")

def PrintResults(dict1):
    results = list(filter(lambda x:len(x)>1, dict1.values()))

    if len(results) > 0:
        print("Dublicate Found : ")
        print("The folowing file are identical.")

        iCnt = 0
        for result in results:
            for subresult in result:
                iCnt = iCnt + 1
                if iCnt >= 2:
                    print('\t\t%s' %subresult)           

def main():
    print('-------------------------------------------------------------------')
    print("Created by Mahesh Pawar")
    print("Application name:" +argv[0])
    print('-------------------------------------------------------------------')

    if (len(argv) != 2):
        print("Error: Invalid number of arguments")
        print("Use -h option to get the help and use -u option to get the usage of application")
        exit()

    if (argv[1] == "-h") or (argv[1] == "-H"):
        print("This Script is used to traverse specific directory and delete dublicate files")
        exit()

    if (argv[1] == "-u") or (argv[1] == "-U"): 
        print("usage: ApplicationName AbsolutePath_of_Directory ")
        exit()

    try:
        
        arr = {}
        StartTime = time.time()
        arr = FindDublicate(argv [1])
        PrintResults(arr)
        duplicateFiles = DeleteFiles(arr)

        LogFile("Log.txt",duplicateFiles)
        EndTime = time.time()

        print("Took %s seconds to evaluate."%(EndTime - StartTime))

    except ValueError:
        print("Error: Invalid datatype of input")

    except Exception as E:
        print("Error: Invalid input",E)

if __name__ =="__main__":
    main()