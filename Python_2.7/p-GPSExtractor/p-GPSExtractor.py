import os
import _modEXIF
import _csvHandler
import _commandParser
from classLogging import _ForensicLog

TS = 0
MAKE = 1
MODEL = 2

userArgs = _commandParser.ParseCommandLine()

logPath = userArgs.logPath + "ForensicLog.txt"
oLog = _ForensicLog(logPath)

oLog.writeLog("INFO", "Scan Started")

csvPath = userArgs.csvPath + "imageResults.csv"
oCSV = _csvHandler._CSVWriter(csvPath)

scanDir = userArgs.scanPath
try:
    picts = os.listdir(scanDir)
except:
    oLog.writeLog("ERROR", "Invalid Directory " + scanDir)
    exit(0)

print "Program Start"
print

for aFile in picts:
    targetFile = scanDir + aFile
    if os.path.isfile(targetFile):
        gpsDictionary, exifList = _modEXIF.ExtractGPSDictionary(targetFile)
        if (gpsDictionary):
            dCoor = _modEXIF.ExtractLatLon(gpsDictionary)

            lat = dCoor.get("Lat")
            latRef = dCoor.get("LatRef")
            lon = dCoor.get("Lon")
            lonRef = dCoor.get("LonRef")

            if (lat and lon and latRef and lonRef):
                print str(lat) + ',' + str(lon)
                oCSV.writeCSVRow(targetFile, exifList[TS], exifList[MAKE], exifList[MODEL], latRef, lat, lonRef, lon)
                oLog.writeLog("INFO", "GPS Data Calculated for :" + targetFile)
            else:
                oLog.writeLog("WARNING", "No GPS EXIF Data for " + targetFile)
        else:
            oLog.writeLog("WARNING", "No GPS EXIF Data for " + targetFile)
    else:
        oLog.writeLog("WARNING", targetFile + " not a valid file")

del oLog
del oCSV