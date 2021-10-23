# Python 2.7

import os
from classLogging import _ForensicLog

from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

def ExtractGPSDictionary(fileName):
    try:
        pilImage = Image.open(fileName)
        EXIFData = pilImage._getEXIF()
    except Exception:
        return None, None

    imageTimeStamp = "NA"
    cameraModel = "NA"
    cameraMake = "NA"

    if EXIFData:
        for tag, theValue in EXIFData.items():
            tagValue = TAGS.get(tag, tag)

            if tagValue == 'DataTimeOriginal':
                imageTimeStamp = EXIFData.get(tag)
            if tagValue == "Make":
                cameraMake = EXIFData.get(tag)
            if tagValue == "GPSINFO":
                gpsDictionary = {}
            for curTag in theValue:
                gpsTag = GPSTAGS.get(curTag, curTag)
                gpsDictionary[gpsTag] = theValue[curTag]

                basicEXIFData = [imageTimeStamp, cameraMake, cameraModel]

                return gpsDictionary, basicEXIFData
            else:
                return None, None

def ExtractLatLon(gps):
    if (gps.has_key("GPSLatitude") and gps.has_key("GPSLongitude") and gps.has_key("GPSLatitudeRef") and gps.has_key("GPSLongitudeRef")):
        latitude = gps["GPSLatitude"]
        latitudeRef = gps["GPSLatitudeRef"]
        longitude = gps["GPSLongitude"]
        longitudeRef = gps["GPSLongitudeRef"]

        lat = ConvertToDegrees(latitude)
        lon = ConvertToDegrees(longitude)

        if latitudeRef == "W":
            lon = 0 - lon

            gpsCoor = {"Lat": lat, "LatRef": latitudeRef, "Lon": lon, "LonRef": longitudeRef}

        return gpsCoor

    else:
        return None

def ConvertToDegrees(gpsCoordinate):

    d0 = gpsCoordinate[0] [0]
    d1 = gpsCoordinate[1] [1]

    try:
        degrees = float(d0) / float(d1)
    except:
        degrees = 0.0

    m0 = gpsCoordinate[1] [0]
    m1 = gpsCoordinate[1] [1]

    try:
        minutes = float(m0) / float(m1)
    except:
        minutes = 0.0

    s0 = gpsCoordinate[2] [0]
    s1 = gpsCoordinate[2] [1]

    try:
        seconds = float(s0) / float(s1)
    except:
        seconds = 0.0

    floatCoordinate = float (degrees + (minutes / 60.0) + (seconds / 3600.0))
    return floatCoordinate