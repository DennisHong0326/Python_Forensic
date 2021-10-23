# Python 2.7

#
# pfish support functions, where all the real work gets done
#

# DisplayMessage() ParseCommandLine() WalkPath()
# HashFile() class _CVSWriter
# ValidateDirectory() ValidateDirectoryWritable()
#

import os #Python Standard Library - Miscellaneous operating system interfaces
import stat #Python Standard Library - functions for interpreting os results
import time #Python Standard Library - Time access and conversions functions
import hashlib #Python Standard Library - Secure hashes and message digests
import csv #Python Standard Library - Parser for commandline options, arguments import csv
import argparse #Python Standard Library - reader and writer for csv files 76 CHAPTER 3 Our First Python Forensics App
import logging #Python Standard Library - logging facility

log = logging.getLogger('main._pfish')

# Name: ParseCommand() Function
#
# Desc: Process and Validate the command line arguments
# use Python Standard Library module argparse
#
# Input: none
#
# Actions:
# Uses the standard library argparse to process the command line
# establishes a global variable gl_args where any of the functions can
# obtain argument information
#
def ParseCommandLine():
    parser = argparse.ArgumentParser('Python file system hashing . . pfish')

    parser.add_argument('-v', '-verbose', help='allows progress messages to be displayed', action='store_true')

    # setup a group where the selection is mutually exclusive and required.
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--md5', help='specifies MD5 algorithm', action='store_true')
    group.add_argument('--sha256', help='specifies SHA256 algorithm', action='store_true')
    group.add_argument('--sha512', help='specifies SHA512 algorithm', action='store_true')

    parser.add_argument('-d', '--rootPath', type=ValidateDirectoryWritable, required=True, help="specify the path for reports and logs will be written")
    parser.add_argument('-r', '--reportPath', type=ValidateDirectoryWritable, required=True, help="specify the path for reports and logs will be written")

    # create a global object to hold the validated arguments, these will be available then
    # to all the Functions within the _phish.py module

    global gl_args
    global gl_hashType

    gl_args = parser.parse_args()

    if gl_args.md5:
        gl_hashType='MD5'
    elif gl_args.sha256:
        gl_hashType='SHA256'
    elif gl_args.sha512:
        gl_hashType='SHA512'
    else:
        gl_hashType = "unknown"
        logging.error('Unknown Hash Type Specified')

    DisplayMessage("Command line processed: Successfully")

    return

# End ParseCommandLine===================================
#
# Name: WalkPath() Function
#
# Desc: Walk the path specified on the command line
#             use Python Standard Library module os and sys
#
# Input: none, uses command line arguments
#
# Actions:
#             Uses the standard library modules os and sys
#             to traverse the directory structure starting a root
#             path specified by the user. For each file discovered, WalkPath
#             will call the Function HashFile() to perform the file hashing
#

def WalkPath():

    processCount = 0
    errorCount = 0

    oCVS = _CSVWriter(gl_args.reportPath+'fileSystemReport.csv', gl_hashType)

    log.info('Root Path:' + gl_args.rootPath)

    for root, dirs, files in os.walk(gl_args.rootPath):
        for file in files:
            fname = os.path.join(root, file)
            result = HashFile(fname, file, oCVS)

            if result is True:
                processCount += 1
            else:
                errorCount += 1
        oCVS.writerClose()

        return processCount

# End WalkPath==========================================
#
# Name: HashFile Function
#
# Desc: Processes a single file which includes performing a hash of the file
#             and the extraction of metadata regarding the file processed
#             use Python Standard Library modules hashlib, os, and sys
#
# Input: theFile = the full path of the file
#             simpleName = just the filename itself
#
# Actions:
#             Attempts to hash the file and extract metadata
#             Call GenerateReport for successful hashed files
#

def HashFile(theFile, simpleName, o_result):
    if os.path.exists(theFile):
        if not os.path.islink(theFile):
            try:
                f = open(theFile, 'rb')
            except IOError:
                log.warning('Open Failed:'+theFile)
                return
            else:
                try:
                    rd = f.read()
                except IOError:
                    f.close()
                    log.warning('Read Failed:'+theFile)
                    return
            else:
                theFileStats = os.stat(theFile)
                (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(theFile)

                DisplayMessage("Processing File:"+theFile)

                fileSize = str(size)

                modifiedTime = time.ctime(mtime)
                accessTime = time.ctime(atime)
                createdTime = time.ctime(ctime)

                ownerID = str(uid)
                groupID = str(gid)
                fileMode = bin(mode)

                if gl_args.md5:
                    hash = hashlib.md5()
                    hash.update(rd)
                    hexMD5 = hash.hexdigest()
                    hashValue = hexMD5.upper()
                elif gl_args.sha256:
                    hash = hashlib.sha256()
                    hash.update(rd)
                    hexSHA256 = hash.hexdigest()
                    hashValue = hexSHA256.upper()
                elif gl_args.sha512:
                    hash = hashlib.sha512()
                    hash.update(rd)
                    hexSHA512 = hash.hexdigest()
                    hashValue = hexSHA512.upper()
                else:
                    log.error('Hash not Selected')
                    print "============================"
                    f.close()

                    o_result.writeCSVRow(simpleName, theFile, fileSize, modifiedTime, accessTime, createdTime, hashValue, ownerID, groupID, mode)
            else:
                log.warning('['+repr(simpleName) +', Skipped Not a File'+']')
                return False
        else:
            log.warning('['+repr(simpleName) +', Skipped Link Not a File'+']')
            return False
    else:
        log.warning('['+repr(simpleName) +', Patch does NOT exist'+']')
    return False


def ValidateDirectory(theDir):
    if not os.path.isdir(theDir):
        raise argparse.ArgumentTypeError('Directory does not exist')
    if os.access(theDir, os.R_OK):
        return theDir
    else:
        raise argparse.ArgumentTypeError('Directory is not readable')

def ValidateDirectoryWritable(theDir):
    if not os.path.isdir(theDir):
        raise argparse.ArgumentTypeError('Directory does not exist')
    if os.access(theDir, os.W_OK):
        return theDir
    else:
        raise argparse.ArgumentTypeError('Directory is not writable')

def DisplayMessage(msg):
    if gl_args.verbose:
        print(msg)
    return

class _CSVWriter:
    def __init__(self, fileName, hashType):
        try:
            self.csvFile = open(fileName,'wb')
            self.writer = csv.writer(self.csvFile, delimiter=',',quoting=csv.QUOTE_ALL)
            self.writer.writerow(('File','Path', 'Size', 'Modified Time', 'Access Time', 'Created Time', 'hashType', 'Owner', 'Group', 'Mode'))
        except:
            log.error('CSV File Failure')

    def writeCSVRow(self, fileName, filePath, filesize, mTime, aTime, cTime, hashVal, own, grp, mod):
        self.writer.writerow((fileName, filePath, filesize, mTime, aTime, cTime, hashVal, own, grp, mod))

    def writerClose(self):
        self.csvFile.close()