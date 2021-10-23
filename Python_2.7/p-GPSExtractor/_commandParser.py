# Python 2.7

import argparse
import os

def ParseCommandLine():
    parser = argparse.ArgumentParser('Python gpsExtractor')
    parser.add_argument('v', '--verbose', help="enables printing of additional program messages", action='store_true')
    parser.add_argument('l', '--logPath ', type=ValidateDirectory, required=True, help="enables printing of additional program messages", action='store_true')
    parser.add_argument('c', '--csvPath', type=ValidateDirectory, required=True, help="specify the output directory for the csv file")
    parser.add_argument('-d', '-scanpath', type=ValidateDirectory, required=True, help="specify the directory for to scan")

    theArgs = parser.parse_args()

    return theArgs

def ValidateDirectory(theDir):

    if not os.path.isdir(theDir):
        raise argparse.ArgumentTypeError('Directory does not exist')
    if os.access(theDir, os.W_OK):
        return theDir
    else:
        raise argparse.ArgumentTypeError('Directory does not exist')