#!usr\bin\python

import arcpy, os, csv

## Export a map JPEG for each contour polygon layer in this map document

mxd = arcpy.mapping.MapDocument(r"I:\DropboxCopy_KristinRichard\Erica\Contour Polygons.mxd")

# Get polygon coast-to-contour layers
poly_layers = arcpy.mapping.ListLayers(mxd, "poly*")
# AMSR2 Raster layers
amsr2_lyrs = arcpy.mapping.ListLayers(mxd, "amsr2*")

# Make raster layers accessible by DATE (in name) with a dictionary
# Typical layer name: 'amsr2_20170415.tif'
amsr2_dict = dict((lyr.name[6:-4], lyr) for lyr in amsr2_lyrs)

# Export a map for each set of polygons
for poly in poly_layers:

    print "Processing " + poly.name
    
    # Get the date of this polygon
    date = poly.name[5:-4]
    # Get the matching AMSR2 layer
    ras = amsr2_dict[date]
    
    # Make them visible
    poly.visible = True
    ras.visible = True
    arcpy.RefreshActiveView()
    
    # Export
    outfolder = os.path.join(r"J:\Laidre McGovern 2017\East Greenland\Survey Study 2017\Maps\JPEGS\Coast to Contour Polygon JPEGS")
    outname = poly.name
    arcpy.mapping.ExportToJPEG(mxd, os.path.join(outfolder, outname), resolution=300)
    print "Export successful!"
    
    # Turn them back off
    poly.visible = False
    ras.visible = False
    
print "Done."


