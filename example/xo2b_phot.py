"""
Aperture photometry of the exoplanet XO2b observation in the filter B Harris.
Data from Zellem et al.(2015): http://arxiv.org/abs/1505.01063
DATE-OBS= '2012-12-10' #from the header of the images

WARNING

You have to put your login.cl in the directory where you would like to run this script or a similar.
"""

#under astroconda envs
import time #package to calculate the time for all process

time_zero = time.time() #return the current time in seconds
import exotred #import the package

print 'Obtain the information in the YAML file:'
data_path, save_path, input_file = exotred.input_info('../input/') #include the YAML information

print 'Obtain the sky background information for each image: '
exotred.bkg_info(input_file)

print 'Loading sky background data: '
bkg_data, bkg_rms = exotred.bkg_read(input_file)

print 'Making the aperture photometry: '
exotred.phot_aperture(input_file,bkg_data,bkg_rms)

print 'Reading the results of the aperture photometry: '
rawflux, eflux, hjd, airmass =  exotred.phot_readData(input_file)

print 'Make a beautifull plot: '

from matplotlib.gridspec import GridSpec
import matplotlib.pyplot as plt #plot library
import numpy as np
def init_plotting():
    """
    Funcao para definir uma janela grafica com parametros customizados para aptresentacoes em ppt ou latex.
    """
    plt.rcParams['figure.figsize'] = (14.0,8.0)
    plt.rcParams['font.size'] = 20
    #plt.rcParams['font.family'] = 'Times New Roman'
    plt.rcParams['axes.labelsize'] = plt.rcParams['font.size']
    plt.rcParams['axes.titlesize'] = 0.75*plt.rcParams['font.size']
    plt.rcParams['legend.fontsize'] = 0.65*plt.rcParams['font.size']
    plt.rcParams['xtick.labelsize'] = plt.rcParams['font.size']
    plt.rcParams['ytick.labelsize'] = plt.rcParams['font.size']
    plt.rcParams['xtick.major.size'] = 3
    plt.rcParams['xtick.minor.size'] = 3
    plt.rcParams['xtick.major.width'] = 1
    plt.rcParams['xtick.minor.width'] = 1
    plt.rcParams['ytick.major.size'] = 3
    plt.rcParams['ytick.minor.size'] = 3
    plt.rcParams['ytick.major.width'] = 1
    plt.rcParams['ytick.minor.width'] = 1
    plt.rcParams['legend.frameon'] = True
    plt.rcParams['legend.loc'] = 'best'
    plt.rcParams['axes.linewidth'] = 1

init_plotting()


f = plt.figure()
plt.suptitle(input_file['exoplanet']+" - rawdata")
gs1 = GridSpec(2, 2, width_ratios=[1,2],height_ratios=[4,1])
gs1.update(wspace=0.5)
ax1 = plt.subplot(gs1[:-1, :])
ax2 = plt.subplot(gs1[-1, :])
ax1.grid()
ax1.errorbar(hjd,rawflux,yerr=eflux,ecolor='g')
ax1.set_xticklabels([])
ax1.set_ylabel('Relative Flux')
ax2.grid()
ax2.plot(hjd,airmass,color='green')
plt.yticks(np.array([airmass.min(), (airmass.min()+airmass.max())/2., airmass.max()]))
ax2.set_xlabel('JD')
ax2.set_ylabel('airmass')
plt.savefig('raw_data_example.png')



print 'total time = ',abs(time.time()-time_zero)/60.,' minutes'