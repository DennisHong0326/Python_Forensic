#Python 2.7

import os
import _modEXIF
import _csvHandler
import _commandParser
from classLogging import _ForensicLog

userArgs = _commandParser.ParseCommandLine()
logPath = userArgs.logPath+"ForensicLog.txt"

oLog = _ForensicLog(logPath)
oLog.writeLog("INFO", "Scan Started")

csvPath = userArgs.csvpath+"imageResult.csv"
oCSV = _csvHandler._CSVWriter(csvPath)

scanDir = userArgs.scanPath
try:
    picts = os.listdir(scanDir)
except:
    oLog.writeLog("ERROR", "Invalid Directory" + scanDir)
