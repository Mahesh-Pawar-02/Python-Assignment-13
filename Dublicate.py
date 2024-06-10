# Problem Statements : Design automation script which accept diectory name and delet alldublicate files from that directory. write names of 
# dublicate files from that directory into log file named as Log.txt. Log.txt file should be created into current directory. Display the
# execution time required for the script

# Usage : DirectoryDublicateRemove.py "Test"

from sys import *
import os
import hashlib
import time

def LogFile(logDir = "Log.txt", duplicateFiles = []):

    if not os.path.exists(logDir):
        os.mkdir(logDir)

    timestamp = time.ctime()
    timestamp = timestamp.replace(" ","")
    timestamp = timestamp.replace(":","_")
    timestamp = timestamp.replace("/","_")

    separator = "-"*80
    logPath = os.path.join(logDir,"Log.txt")
    f = open(logPath,'w')
    f.write(separator + "\n")
    f.write("Welcome..! to Log File "+"\n")
    f.write("Log File created at : "+time.ctime()+"\n")
    f.write(separator + "\n")

    f.write("Deleted Dublicate file are : " + "\n")
    f.write(separator + "\n")

    for element in duplicateFiles:
        f.write("%s\n"%element)

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
    else:
        print("No dublicate file found...")

def main():
    print('-------------------------------------------------------------------')
    print("Created by Mahesh Pawar")
    print("Application name:" +argv[0])
    print('-------------------------------------------------------------------')

if (len(argv) != 2):
    print("Error: Invalid number of arguments")
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

    LogFile(os.getcwd(),duplicateFiles)
    EndTime = time.time()

    print("Took %s seconds to evaluate."%(EndTime - StartTime))

except ValueError:
    print("Error: Invalid datatype of input")

except Exception as E:
    print("Error: Invalid input",E)

if __name__ =="__main__":
    main()