"""
Reduction and Calibration of the exoplanet XO2b observation in the filter B Harris.
Data from Zellem et al.(2015): http://arxiv.org/abs/1505.01063

WARNING

You have to put your login.cl in the directory where you would like to run this script or a similar.
"""
#under astroconda envs
import time #package to calculate the time for all process

time_zero = time.time() #return the current time in seconds
import exotred #import the package
print 'Obtain the information in the YAML file:'
data_path, save_path, input_file = exotred.input_info('../input/') #include the YAML information
print 'Create the superbias image.'
exotred.masterbias(data_path, save_path, input_file) #create a superbias image
print 'Create the superflat image'
exotred.masterflat(data_path, save_path, input_file) #create a superflat image
print 'Reduce and calibrate science images'
exotred.science_reduction(data_path,save_path,input_file) #reduce and calibrate in flat e bias the science images
print 'Obtain time information of each science image'
exotred.time_info(data_path,save_path,input_file) #obtain the time information for each science image (based on astropy)
print 'Obtain airmass and put the time information in the header of each science image'
exotred.time_calibration(data_path,save_path,input_file) #obtain the airmass, and put all information of time in the header (based on pyraf).
time_final = (abs(time.time()-time_zero)/60.) #time in minutes
print 'Duration = ',time_final,' minutes'
