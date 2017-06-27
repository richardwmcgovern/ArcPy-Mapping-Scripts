#!usr\bin\python

import arcpy, os, shutil, time
arcpy.CheckOutExtension("SPATIAL")
arcpy.env.overwriteOutput = True

## Process binary files downloaded from NSIDC into .bil files
## Then convert those to ESRI native raster format: grids.

binary_files = [file for file in os.listdir(r"I:\DropboxCopy_KristinRichard\KristinRichardProjects\BaffinBay_PolarBears\Data\NSIDC\Monthly\BIN") if file.endswith('.bin')]

bil_folder = r"I:\DropboxCopy_KristinRichard\KristinRichardProjects\BaffinBay_PolarBears\Data\NSIDC\Monthly\BIL"
years = ['1991', '1992', '1993', '1994', '1995', '1996', '1997', '2009', '2010', '2011', '2012', '2013', '2014']

t1 = time.time()

## Convert .bin files to .bil
## and create a .hdr file for each
# file looks like nt_199101_f08_v1.1_n
for file in binary_files:
    outfile = file.split("_")[0]+file.split("_")[1]
    # Make .bil file
    shutil.copyfile(os.path.join(r"I:\DropboxCopy_KristinRichard\KristinRichardProjects\BaffinBay_PolarBears\Data\NSIDC\Monthly\BIN", file), os.path.join(bil_folder, outfile + ".bil"))
    # Make .hdr file (copy the original)
    shutil.copyfile(r"I:\DropboxCopy_KristinRichard\KristinRichardProjects\BaffinBay_PolarBears\Data\NSIDC\Monthly\BIN\headerfile.hdr", os.path.join(bil_folder, outfile + ".hdr"))
    
print "Time to make .bil and .hdr files: " + str(time.time()-t1) + " seconds."

t2 = time.time()

## For each year separately
## Convert .bil files to raster and send to that year's folder
for year in years:
    # Make ; separated list for RasterToOtherFormat
    bilfiles = ';'.join([x for x in os.listdir(bil_folder) if (x.endswith(".bil") and x[2:6] == year)])
    arcpy.env.workspace = bil_folder

    ## This step reads the .bil and .hdr files together to produce raster
    arcpy.RasterToOtherFormat_conversion(bilfiles, os.path.join(r"I:\DropboxCopy_KristinRichard\KristinRichardProjects\BaffinBay_PolarBears\Data\NSIDC\Monthly\GRID", year), "GRID")
    

print "Time to make GRID files: " + str(time.time()-t2) + " seconds."

t3 = time.time()

## Convert to GDB and make percentages
for year in years:
    arcpy.env.workspace = os.path.join(r"I:\DropboxCopy_KristinRichard\KristinRichardProjects\BaffinBay_PolarBears\Data\NSIDC\Monthly\GRID", year)
    rasters = arcpy.ListRasters()
    outgdb = r"I:\DropboxCopy_KristinRichard\KristinRichardProjects\BaffinBay_PolarBears\Data\nsidc_monthlyAverages\monthavg"+year+".gdb"
    
    # Convert to %
    for raster in rasters:
        ras = arcpy.sa.Raster(raster) / 2.5
        ras.save(os.path.join(outgdb, "perc_"+raster[2:]))
        
print "Time to make percentages: " + str(time.time() - t3) + " seconds."


## Define projections (NSIDC_SSMI_NP_Stereographic)
sr = arcpy.Describe(r"I:\DropboxCopy_KristinRichard\KristinRichardProjects\BaffinBay_PolarBears\Data\nsidc1991.gdb\nt19910128").spatialReference
for year in years:
    arcpy.env.workspace = r"I:\DropboxCopy_KristinRichard\KristinRichardProjects\BaffinBay_PolarBears\Data\nsidc_monthlyAverages\monthavg"+year+".gdb"
    for raster in arcpy.ListRasters():
        arcpy.DefineProjection_management(raster, sr)

print "Finished projecting!"