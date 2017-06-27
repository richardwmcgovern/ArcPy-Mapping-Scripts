#!usr\bin\python

import os, shutil, time
import gzip

## Download all Arctic nc.gz -zipped NetCDF files from
# ftp://ftp-projects.zmaw.de/seaice/AMSR2/3.125km/
## Use gzip as necessary to unzip


from ftplib import FTP
ftp = FTP('ftp-projects.cen.uni-hamburg.de', timeout=10000)
ftp.login()

## Outpath
netcdfs = r"E:\DropboxCopy_KristinRichard\Erica\Raster\AMSR2\NetCDF"

## Get the netCDF files (.nc and .nc.gz)
amsr2_files = r"./seaice/AMSR2/3.125km"
ftp.cwd(amsr2_files)
ftp_files = ftp.nlst()

months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
days = {'01': ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31'], \
        '02': ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29'], \
        '03': ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31'], \
        '04': ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30'], \
        '05': ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31'], \
        '06': ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30'], \
        '07': ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31'], \
        '08': ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31'], \
        '09': ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30'], \
        '10': ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31'], \
        '11': ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30'], \
        '12': ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']}
#years = [str(x) for x in [2012, 2013, 2014, 2015]]
years = [str(x) for x in [2016, 2017]]

couldnotfind = []

for year in years:
    t1 = time.time()
    print year
    for month in months:
        print '\t'+month
        for day in days[month]:
            
            ## Check if it doesn't have this file
            # Arc_20140828_res3.125_pyres.nc.gz or .nc
            
            netCDF = 'Arc_'+year+month+day+'_res3.125_pyres.nc'
            zipped_netCDF = 'Arc_'+year+month+day+'_res3.125_pyres.nc.gz'
            
            ## Write to appropriate folder if file exists
            
            # Simply download if it is an unpacked NetCDF
            if netCDF in ftp_files:
                out_name = netCDF
                # Build output path if it doesnt exist yet
                out_path = os.path.join(netcdfs, year, month)
                if not os.path.exists(out_path):
                    os.makedirs(out_path)
                    
                # Download nc file
                with open(os.path.join(out_path, out_name), 'wb') as localfile:
                    ftp.retrbinary('RETR %s' % netCDF, localfile.write)
                    
            # Unzip using "gzip" if it is a gz file
            elif zipped_netCDF in ftp_files:
                out_name = zipped_netCDF
                # Build output path if it doesnt exist yet
                out_path = os.path.join(netcdfs, year, month)
                if not os.path.exists(out_path):
                    os.makedirs(out_path)
                gz_file = os.path.join(out_path, out_name)
                
                # Download gz file
                with open(gz_file, 'wb') as localfile:
                    ftp.retrbinary('RETR %s' % zipped_netCDF, localfile.write)
                # Unzip gz file. Save to NetCDF
                nc_file = os.path.join(out_path, netCDF)
                with open(nc_file, 'wb') as f:
                    with gzip.open(gz_file, 'rb') as gz:
                        f.write(gz.read())
                # Delete the gz file afterwards
                os.remove(gz_file)
                
            else:
                couldnotfind.append(year+month+day)
                pass 
                # Cant find...
                # 2012 Jan ~ Sep
                # 2014 Nov 5, 6 15
                # 2015 Apr 7, Nov 26
                
    print "Took: " + str(time.time()-t1) + " seconds."
print "DONE!"

print "Could not find ..."
print couldnotfind



