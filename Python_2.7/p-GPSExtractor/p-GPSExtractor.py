# Python 2.7

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
    exit()

for aFile in picts:

    targetFile = scanDir + aFile

    if os.path.isfile(targetFile):

        gpsDictionary = _modEXIF.ExtractGPSDictionary(targetFile)

        if (gpsDictionary):
            dCoor = _modEXIF.ExtractLatLon(gpsDictionary)

            lat = dCoor.get("Lat")
            latRef = dCoor.get("LatRef")
            lon = dCoor.get("Lon")
            lonRef = dCoor.get("LonRef")

            if (lat and lon and latRef and lonRef):
                print str(lat) + ',' + str(lon)

                oCSV.writeCSVRow(targetFile, exifList[TS], exifList[MAKE], exifList[MODEL],latRef, lat, lonRef, lon)
                oLog.writeLog("INFO", "GPS Data Calculated for :" + targetFile)
            else:
                oLog.writeLog("WARNING", "No GPS EXIF Data for " + targetFile)
        else:
            oLog.writeLog("WARNING", "No GPS EXIF Data for " + targetFile)
    else:
        oLog.writeLog("WARNING", targetFile + " not a valid file")

del oLog
del oCSV