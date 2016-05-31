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
    input_file = glob.glob(path_input)
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
    #Return to original directory
    os.chdir(original_path)
    #END of the masterbias reduction messsage
    print '\nsuperbias.fits created!\n'
    print '\nEND of superbias reduction!\n'
    #obtain the value of return
    output = glob.glob(save_path+'superbias*.fits')
    if len(output) != 0:
        output = 0
    else:
        output = 1
    return output
