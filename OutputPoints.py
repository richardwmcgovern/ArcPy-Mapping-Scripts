#!usr\bin\python

import arcpy, os, csv

### 
# Output a csv of lat/lons for each route delineated in the North West Passage project.
# midlines & outer perimeter polygons

## Input
# Lines
in_lines_folder = r"I:\DropboxCopy_KristinRichard\Donna\Northwest Passage\Route Segments and Lines\Westward"
arcpy.env.workspace = in_lines_folder
in_lines = [os.path.join(in_lines_folder, line) for line in arcpy.ListFeatureClasses(feature_type="Polyline")]
# # Perimeters
# in_peri_folder = r"I:\DropboxCopy_KristinRichard\Donna\Northwest Passage\Route Boundaries\Eastward\clipped"
# arcpy.env.workspace = in_peri_folder
# in_perimeters = [os.path.join(in_peri_folder, poly) for poly in arcpy.ListFeatureClasses("*_b*", feature_type="Polygon")]


## Output - points
out_midlines = r"I:\DropboxCopy_KristinRichard\Donna\Northwest Passage\Route Points CSV\_Final\west\route_lines"
#out_perimeters = r"I:\DropboxCopy_KristinRichard\Donna\Route Points\Outer Perimeters"

# Get lat/lon GCS_WGS_1984 geographic coordinate system
gcs = arcpy.Describe(r"I:\DropboxCopy_KristinRichard\KristinRichardProjects\BaffinBay_PolarBears\Data\Shapefiles\_test.shp")
gcs = gcs.spatialReference

## Write line coords to csv
for line in in_lines:
    line_points = []
    outname = os.path.basename(line)[:-4]+".csv"
    print "Making %s" % outname
    
    # Get coordinates. Append to list
    with arcpy.da.SearchCursor(line, ["SHAPE@"], spatial_reference=gcs) as cursor:
        for row in cursor:
            for part in row[0]:
                for vertex in part:
                    line_points.append((vertex.X, vertex.Y))
    
    # Write these coordinates to csv
    with open(os.path.join(out_midlines, outname), 'wb') as file:
        ww = csv.writer(file, delimiter=",")
        ww.writerow(["LON", "LAT"])
        ww.writerows(line_points)
    
## Repeat for polygon (perimeter) NWP route corridors
for peri in in_perimeters:
    peri_points = []
    outname = os.path.basename(peri)[:-4]+".csv"
    
    # Get coordinates. Append to list
    # Use handy spatial reference argument support by da search cursors
    with arcpy.da.SearchCursor(peri, ["SHAPE@"], spatial_reference=gcs) as cursor:
        for row in cursor:
            for part in row[0]:
                for vertex in part:
                    peri_points.append((vertex.X, vertex.Y))
    
    # Write these coordinates to csv
    with open(os.path.join(r"I:\DropboxCopy_KristinRichard\Donna\Route Points\Outer Perimeters", outname), 'wb') as file:
        ww = csv.writer(file, delimiter=",")
        ww.writerow(["LON", "LAT"])
        ww.writerows(peri_points)
        
        
