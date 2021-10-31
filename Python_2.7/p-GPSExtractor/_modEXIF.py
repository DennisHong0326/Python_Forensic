from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

def ExtractGPSDictionary(fileName):
    try:
        pilImage = Image.open(fileName)
        exifData = pilImage._getexif()

    except Exception:

        return None, None

    imageTimeStamp = "NA"
    CameraModel = "NA"
    CameraMake = "NA"

    if exifData:
        for tag, theValue in exifData.items():
            tagValue = TAGS.get(tag, tag)
            if tagValue == 'DateTimeOriginal':
                imageTimeStamp = exifData.get(tag)
            if tagValue == "Make":
                cameraMake = exifData.get(tag)
            if tagValue == 'Model':
                cameraModel = exifData.get(tag)
            if tagValue == "GPSInfo":

                gpsDictionary = {}

                for curTag in theValue:
                    gpsTag = GPSTAGS.get(curTag, curTag)
                    gpsDictionary[gpsTag] = theValue[curTag]

                basicExifData = [imageTimeStamp, cameraMake, cameraModel]

                return gpsDictionary, basicExifData

    else:
        return None, None

def ExtractLatLon(gps):

    if (gps.has_key("GPSLatitude") and gps.has_key("GPSLongitude") and gps.has_key("GPSLatitudeRef") and gps.has_key("GPSLatitudeRef")):

        latitude = gps["GPSLatitude"]
        latitudeRef = gps["GPSLatitudeRef"]
        longitude = gps["GPSLongitude"]
        longitudeRef = gps["GPSLongitudeRef"]

        lat = ConvertToDegrees(latitude)
        lon = ConvertToDegrees(longitude)

        if latitudeRef == "S":
            lat = 0 - lat

        if longitudeRef == "W":
            lon = 0 - lon

        gpsCoor = {"Lat": lat, "LatRef": latitudeRef, "Lon": lon, "LonRef": longitudeRef}

        return gpsCoor

    else:
        return None

def ConvertToDegrees(gpsCoordinate):
    d0 = gpsCoordinate[0][0]
    d1 = gpsCoordinate[0][1]
    try:
        degrees = float(d0) / float(d1)
    except:
        degrees = 0.0

    m0 = gpsCoordinate[1][0]
    m1 = gpsCoordinate[1][1]
    try:
        minutes = float(m0) / float(m1)
    except:
        minutes = 0.0

    s0 = gpsCoordinate[2][0]
    s1 = gpsCoordinate[2][1]
    try:
        seconds = float(s0) / float(s1)
    except:
        seconds = 0.0

    floatCoordinate = float(degrees + (minutes / 60.0) + (seconds / 3600.0))

    return floatCoordinate