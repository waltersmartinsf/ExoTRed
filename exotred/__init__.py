"""
This file contains all the functions for ExoTRed Package

@author: Walter Martins-Filho
e-mail: walter at on.br
        waltersmartinsf at gmail.com

"""


"""
Loading packges and python useful scritps
"""
from pyraf import iraf #loading iraf package
from login import * #loading login.cl parameters for iraf
from ExoSetupTaskParameters import * #loading setup from PyExoDRPL
import glob #package for list files
import os #package for control bash commands
import yaml #input data without any trouble
import string
import numpy as np
from astropy.io import fits
#******************************************************************************
#**************** BEGIN INPUT PATH FILE ***************************************
#******************************************************************************



def input_info(path_input):
    """
    Obtain information about the files that will be reduced or analised.
    ___
    Input:

    path_input: string, path of your yaml file directory with the information of the data

    Return:

    save_path: string, path where is your data to be reduced.
    data_path: string, path where the data reduced will be saved.
    input_file: dictionary, information from YAML file.

    """
    #path for your data directory, path for your data save, and names for the lists
    #Import with yaml file: input path and prefix information for files
    input_file = glob.glob(path_input+'*.yaml')
    if input_file: #if exist the input file, the code will obtain all information We need to run all tasks
        if len(input_file) == 1: #if there is only one yaml file, obtain data and save paths, and return that with a dictionary with information
            print 'reading input file ... \n'
            file = yaml.load(open(input_file[0])) #creating our dictionary of input variables
            data_path = file['data_path']
            save_path = file['save_path']
            print '....  done! \n'
            if len(input_file) > 1: #if are more than one yaml file,. the code will ask to you remove the others.
                print 'reading input file ... \n'
                print '.... there is more than 1 input_path*.yaml.\n \nPlease, remove the others files that you do not need. \n'
                raise SystemExit
    else:
        #if aren't a yaml file, the code ask for you to put a valid yaml file path.
        print 'There is no input_path*.yaml. \nPlease, create a input file describe in INPUT_PARAMETERS.'
        raise SystemExit
    input_file = file #creating a better name to our dictionary info
    return data_path, save_path, input_file

def masterbias(data_path, save_path, input_file):
    """
    Obtain the masterbias.fits image.
    ___
    Input:
    For obtain this parameters, use the input_info function.

    data_path: string, path where are the images data.
    save_path: string, path where will save all reduced images.
    input_file: dict, with information describe in the YAML file.

    Output:
    It is possible that the function return some of these values:

    0. Create the masterbias image on the save_path.
    1. It do not create the masterbias image, because of some error
    ___
    """
    #Set original directory
    original_path = os.getcwd()
    #Change your directory to data diretory
    os.chdir(data_path)
    #list all bias images
    bias = glob.glob('bias*.fits')
    print 'Loading bias images \nTotal of bias files = ',len(bias),'\nFiles = \n'
    print bias
    print '\nCreating superbias \n'
    #if save_path exist, continue; if not, create.
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    #copy bias images to save_path
    os.system('cp bias*.fits '+save_path)
    #change to sabe_path
    os.chdir(save_path)
    #verify if previous superbias exist
    if os.path.isfile('superbias.fits') == True:
        os.system('rm superbias.fits')
    #create the list of bias images
    bias_list = string.join(bias,',')
    #combine the bias image and create the superbias
    iraf.imcombine(bias_list,'superbias.fits')
    iraf.imstat('superbias.fits')
    #clean previos bias files
    print '\n Cleaning bias*.fits images ....\n'
    os.system('rm bias*.fits')
    print '\n.... done.'
    #print output
    #test of outpu value
    #os.remove('superbias.fits')
    #Verify if the image was created:
    output = glob.glob('superbias*.fits')
    if len(output) != 0:
        output = 0
    else:
        output = 1
    #Return to original directory
    os.chdir(original_path)
    #END of the masterbias reduction messsage
    print '\nsuperbias.fits created!\n'
    print '\nEND of superbias reduction!\n'
    #obtain the value of return
    if output == 1:
        print '!!! ERROR/WARNING !!!'
        print 'Check if the superbias was created or if there is more than one superbias image.'
    return output

def masterflat(data_path,save_path,input_file):
    """
    Obtain the masterflat image for calibration.
    ___
    INPUT:
    For obtain this parameters, use the input_info function.

    data_path: string, path where are the images data.
    save_path: string, path where will save all reduced images.
    input_file: dict, with information describe in the YAML file.

    OUTPUT:
    It is possible that the function return some of these values:

    0. Create the masterflat image on the save_path.
    1. It do not create the masterflat image, because of some erros.
    """
    #set original directory
    original_path = os.getcwd()
    #Change your directory to data diretory
    os.chdir(data_path)
    #list all flat images
    flat = glob.glob('flat*.fits')
    print 'Loading flat images \nTotal of flat files = ',len(flat),'\nFiles = \n'
    print flat
    #if save_path exist, continue; if not, create.
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    #create a list of bias images and copy images to save_path
    os.system('cp flat*.fits '+save_path)
    #creating the names of flat with bias subctracted
    bflat = []
    for i in flat:
        bflat.append('B'+i)
    print '\n Names os flat images with bias subtracted: \n \n',bflat
    #change for save_path directory
    os.chdir(save_path)
    #verify if previous superbias exist
    if os.path.isfile('superflat.fits') == True:
        os.system('rm superflat.fits')
    #verify if exits previous bflat*.fits files and remove then.
    for i in bflat:
        if os.path.isfile(i) == True:
            os.system('rm -f '+i)
    print '\nCreating superflat .... \n'
    #create the list of flat images  and bflat images
    #flat = string.join(flat,',')
    #bflat = string.join(bflat,',')
    print '\n Subtracting bias from flat images and creating bflat images.... \n'
    #iraf.imarith()
    for i in range(len(flat)):
        iraf.imarith(flat[i],'-','superbias.fits',bflat[i])
        #print statistics from bflat*.fits images
        iraf.imstat(bflat[i])
    print '\n .... done \n'
    #clean previos flat*.fits files
    print '\n Clean flat*.fits images .... \n'
    os.system('rm flat*.fits')
    print '\n .... done. \n'
    #normalizing each flat
    print '\nNormalizing each flat ....\n'
    #checking if mean from numpy is the same from your bflat images using imstat
    #take the mean of each bflat image
    bflat_mean = np.zeros(len(bflat))
    for i in range(len(bflat)):
        image = fits.getdata(bflat[i])
        image = np.array(image,dtype='Float64')
        bflat_mean[i] = round(np.mean(image))
    image = 0 #clean image allocate to this variable
    print 'The mean of each bflat image, respectivaly ...'
    print bflat_mean
    #creating the names of bflat images after the normalization:
    abflat = []
    for i in bflat:
        abflat.append('A'+i)
    print '\n Names os bflat images with bias subtracted and normalizad: \n \n',abflat
    #verify if exist previous ABflat*.fits images and remove then.
    for i in abflat:
        if os.path.isfile(i) == True:
            os.system('rm -f '+i)
    for i in range(len(abflat)):
        iraf.imarith(bflat[i],'/',bflat_mean[i],abflat[i])
    print '\n.... done!\n'
    print '\n Cleaning bflat*.fits images ....\n'
    os.system('rm Bflat*.fits')
    print '\n.... done.\n'
    print 'Statistics of the abflat*.fits images .... \n'
    for i in range(len(abflat)):
        iraf.imstat(abflat[i])
    print '\n Combining abflat images ....\n'
    ablist = string.join(abflat,',')
    iraf.imcombine(ablist,'superflat.fits')
    iraf.imstat('superflat.fits')
    print '\n .... done. \n'
    print '\nCleaning ABflat*.fits images ....\n'
    os.system('rm ABflat*.fits')
    print '\n.... done!'
    #Verify if the image was created:
    output = glob.glob('superflat*.fits')
    if len(output) != 0:
        output = 0
    else:
        output = 1
    #Return to original directory
    os.chdir(original_path)
    #last mensage
    print '\n MASTERFLAT.FITS created! \n'
    print '\n END of Data Reduction for create a masterflat.fits file. \n'
    #obtain the value of return
    if output == 1:
        print '!!! ERROR/WARNING !!!'
        print 'Check if the superbias was created or if there is more than one superbias image.'
    return output

def science_reduction(data_path,save_path,input_file):
    """
    Calibrate science images with masterflat (or superflat) and masterbias (or superbias) images.
    ___
    INPUT:
    For obtain this parameters, use the input_info function.

    data_path: string, path where are the images data.
    save_path: string, path where will save all reduced images.
    input_file: dict, with information describe in the YAML file.

    OUTPUT:
    It is possible that the function return some of these values:

    0. Create the masterflat image on the save_path.
    1. It do not create the masterflat image, because of some erros.
    """
    #name of the planet
    planet = file['exoplanet']
    return
