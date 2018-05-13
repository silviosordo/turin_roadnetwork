import sys
import os

try:
    from osgeo import ogr, osr, gdal
except:
    sys.exit(0)

def list_drivers():
    # list available drivers (i.e., readers for different file formats)
    cnt = ogr.GetDriverCount()
    formatsList = []  # Empty List

    for i in range(cnt):
        driver = ogr.GetDriver(i)
        driverName = driver.GetName()
        if not driverName in formatsList:
            formatsList.append(driverName)

    formatsList.sort() # Sorting the messy list of ogr drivers

    for i in formatsList:
        print(i)

#list_drivers()
#sys.exit(0)

DWGfile = "turin.dxf" # input file

driver = ogr.GetDriverByName('DXF') # specify formats of input file

dataSource = driver.Open(DWGfile, 0) # 0 means read-only. 1 means writeable.

# Check to see if shapefile is found.
if dataSource is None:
    print('Could not open %s' % (DWGfile))
else:
    print('Opened %s' % (DWGfile))
    layer = dataSource.GetLayer() # get layer
    featureCount = layer.GetFeatureCount() # get feature count
    print("Number of features in %s: %d" % (os.path.basename(DWGfile), featureCount))
    sys.exit(0)
    # for feature in layer:
    #    print(feature.ExportToJson())
    ogr.GetDriverByName("GeoJSON").CopyDataSource(dataSource, "turin.json") # export data to output format