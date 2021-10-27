import csv

class _CSVWriter:

    def __init__(self, fileName):
        try:
            self.csvFile = open(fileName, 'wb')
            self.writer = csv.writer(self.csvFile, delimiter=',', quoting=csv.QUOTE_ALL)
            self.writer.writerow( ('Image Path', 'TimeStamp', 'Camera Make', 'Camera Model', 'Lat Ref', 'Latitude', 'Lon Ref','Longitude' ) )
        except:
            log.error('CSV File Failure')

    def writeCSVRow(self, fileName, timeStamp, CameraMake, CameraModel,latRef, latValue, lonRef, lonValue):
        latStr = '%.8f' %  latValue
        lonStr= '%.8f' %  lonValue
        self.writer.writerow((fileName, timeStamp, CameraMake, CameraModel, latRef, latStr, lonRef, lonStr))

    def __del__(self):
        self.csvFile.close()
