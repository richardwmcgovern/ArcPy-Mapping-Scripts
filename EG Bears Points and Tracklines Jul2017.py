#!usr\bin\python

#########################################################
## Update EG bear and trackline maps through July 2017 ##
#########################################################

import arcpy, os

## INPUT DATA FOLDER (Where points & lines live)
arcpy.env.workspace = r"C:\Users\Richard\Desktop\Laidre McGovern 2017\__Aug 2017 Backup\_August2017_Files_For_Kristin\EG Database\Data"

## PATH TO MXD
mxd_path = r"C:\Users\Richard\Desktop\Laidre McGovern 2017\__Aug 2017 Backup\_August2017_Files_For_Kristin\EG Database\_EG Bears and Tracklines July 2017.mxd"

## OUTPUT FOLDER
output_maps = r"C:\Users\Richard\Desktop\Laidre McGovern 2017\__Aug 2017 Backup\_August2017_Files_For_Kristin\EG Database\Maps Jul2017 Updated"

## LAYERS FOLDER (For making temporary layers)
layerfolder = r"C:\Users\Richard\Desktop\Laidre McGovern 2017\__Aug 2017 Backup\_August2017_Files_For_Kristin\EG Database\Data\Layers"

# Make input layers
points = arcpy.MakeFeatureLayer_management("EG_Database_Jul2017.shp", "ptlyr")
lines = arcpy.MakeFeatureLayer_management("EG_Database_Jul2017_lines.shp", "lnlyr")

# Setup access to MXD
mxd = arcpy.mapping.MapDocument(mxd_path)
df = arcpy.mapping.ListDataFrames(mxd)[0]  # The main map
df2 = arcpy.mapping.ListDataFrames(mxd)[1] # The inset
print df2.name

ptts = list(set([ptt for ptt, in arcpy.da.SearchCursor(points, "PTT")]))

for ptt in ptts:
    #ptt = '2011105799'
    print ptt

    # First turn off everything except for the land and imagery
    lyrs = arcpy.mapping.ListLayers(mxd, data_frame=df)+arcpy.mapping.ListLayers(mxd, data_frame=df2)
    for lyr in lyrs:
        if lyr.name != "ArcticLand" and lyr.name != "IBCAO_Elev":
            lyr.visible = False
    arcpy.RefreshTOC()
    arcpy.RefreshActiveView()

    ## This method below of making+adding layer, then applying symbology is good

    ## Add lines to map
    # Get lines layer object
    templyr = os.path.join(layerfolder, "temp.lyr")
    llyr = arcpy.MakeFeatureLayer_management(lines, "llyr"+ptt, '"PTT" = ' + "'%s'" % ptt)
    arcpy.SaveToLayerFile_management(llyr, templyr)
    line_lyr = arcpy.mapping.Layer(templyr)
    os.remove(templyr)
    # Apply symbology
    arcpy.ApplySymbologyFromLayer_management(line_lyr, os.path.join(layerfolder, "lines.lyr"))
    # Add lines
    arcpy.mapping.AddLayer(df, line_lyr, "TOP")

    ## Add points to map
    # Get points layer object
    templyr = os.path.join(layerfolder, "temp.lyr")
    plyr = arcpy.MakeFeatureLayer_management(points, "plyr"+ptt, '"PTT" = ' + "'%s'" % ptt)
    arcpy.SaveToLayerFile_management(plyr, templyr)
    pt_lyr = arcpy.mapping.Layer(templyr)
    os.remove(templyr)
    # Apply symbology
    arcpy.ApplySymbologyFromLayer_management(pt_lyr, os.path.join(layerfolder, "points.lyr"))
    arcpy.mapping.AddLayer(df, pt_lyr, "TOP")

    ## Repeat for inset dataframe
    # Add lines and points to inset-dataframe, and zoom in
    # DF2 Lines
    templyr = os.path.join(layerfolder, "temp.lyr")
    llyr = arcpy.MakeFeatureLayer_management(lines, "llyr2"+ptt, '"PTT" = ' + "'%s'" % ptt)
    arcpy.SaveToLayerFile_management(llyr, templyr)
    line_lyr = arcpy.mapping.Layer(templyr)
    os.remove(templyr)
    arcpy.ApplySymbologyFromLayer_management(line_lyr, os.path.join(layerfolder, "lines.lyr"))
    arcpy.mapping.AddLayer(df2, line_lyr, "TOP")
    # DF2 Points
    templyr = os.path.join(layerfolder, "temp.lyr")
    plyr = arcpy.MakeFeatureLayer_management(points, "plyr2"+ptt, '"PTT" = ' + "'%s'" % ptt)
    arcpy.SaveToLayerFile_management(plyr, templyr)
    pt_lyr = arcpy.mapping.Layer(templyr)
    os.remove(templyr)
    arcpy.ApplySymbologyFromLayer_management(pt_lyr, os.path.join(layerfolder, "points.lyr"))
    arcpy.mapping.AddLayer(df2, pt_lyr, "TOP")

    print "Added layers to map!"

    ## !!!!!!!!!! THIS WORKS!
    # Save previous extent
    old_ext = df2.extent

    # Access this point layer
    lyr = arcpy.mapping.ListLayers(mxd, pt_lyr.name)[0]
    # Select all points and zoom to them
    arcpy.SelectLayerByAttribute_management(lyr, "NEW_SELECTION", "#")
    df2.zoomToSelectedFeatures()


    # Zoom in
    #df2.zoomToSelectedFeatures()
    # Instead try to explicitly make the extents the same:
    #ext = lyr.getSelectedExtent()
    #print df2.extent.XMax
    #df2.extent = ext # layer obj has no attribute 'extent'
    #print df2.extent.XMax
    # EXTENT IS CHANGING!! But Still not quite right :(

    ### HELP:
    # "The data frame extent coordinates are based on the extent of the data frame in Layout View, not in Data View. This is because the shape of the data frame in Data View may have a different aspect ratio than the data frame in Layout View."
    # ^ http://help.arcgis.com/en/arcgisdesktop/10.0/help/index.html#//00s300000003000000
    #http://help.arcgis.com/en/arcgisdesktop/10.0/help/index.html#//00s300000003000000
    #^ This says lyr.getSelectedExtent is correct

    #### .... IS IT BECAUSE I"M USING GEODATABASE FC?

    ### Now it's adding the layers twice in both data frames??!?

    # Deselect afterwards
    arcpy.SelectLayerByAttribute_management(lyr, "CLEAR_SELECTION")

    # Refresh?
    arcpy.RefreshTOC()
    arcpy.RefreshActiveView()
    # or SAVE? mxd.save. Might not work...

    ## Get title parameters
    # Examine this PTT and the CaptureLoc.
    # Get category, tattoo, date captured, and end date
    category = ''
    tattoo = ''
    date_captured = ''
    end_date = ''
    where = '"PTT" = ' + "'%s'" % ptt
    with arcpy.da.SearchCursor(points, ["Category", "ID", "DateCapStr", "EndDateStr"], where) as sc:
        for row in sc:
            category = row[0]
            tattoo = row[1]
            date_captured = row[2]
            end_date = row[3]

    # Change title
    mxd.title = "PTT: " + ptt + " \n \n Category: " + category + "\nTattoo: " + tattoo + "\nDate Captured: " + date_captured + "\nEnd Date: " + end_date
    print "Built title!"
    
    # Export this map
    arcpy.mapping.ExportToJPEG(mxd, os.path.join(output_maps, "bear_"+ptt+".jpg"))
    print "Exported!\n...\n..."
    
    # Revert to old extent
    df2.extent = old_ext
    
    
    
# Save cuz why not
#mxd.save()
    
del df, df2, mxd




