#!usr\bin\python

import arcpy, os, csv
arcpy.env.overwriteOutput = True
arcpy.CheckOutExtension("SPATIAL")

## Construct polygon features from sea ice concentration % contours
## and the East Greenland coast. Then compute their area.

## Get Final (Editted) Contours
arcpy.env.workspace = r"I:\DropboxCopy_KristinRichard\Erica\Shapefiles\AMSR2 Final Contours"
contours = arcpy.ListFeatureClasses()

## Get Area Container (Lines) - Bounding area
area_container = arcpy.MakeFeatureLayer_management(r"I:\DropboxCopy_KristinRichard\Erica\Shapefiles\Land\Area_Container_Lines.shp", "ac")

## Make Coast To Contour Polygons
for contour in contours:
    
    outpath = r"I:\DropboxCopy_KristinRichard\Erica\Shapefiles\Coast to Contour Polygons"
    outname = 'poly'+contour[8:]
    fullpath = os.path.join(outpath, outname)
    print '\n...'*5
    
    # "Cut out" a set of polygons using this contour from the area container
    arcpy.FeatureToPolygon_management([contour, area_container], fullpath, cluster_tolerance="#", attributes="NO_ATTRIBUTES", label_features="#")
    #
    print "Made polygon!"
    
    # Compute Area
    arcpy.AddField_management(fullpath, "AREA", "DOUBLE")
    arcpy.CalculateField_management(fullpath, "AREA", "!shape.geodesicArea@SQUAREKILOMETERS!", "PYTHON_9.3")
    print "Finished computing area!"

print 'done'
