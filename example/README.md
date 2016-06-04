# Information

This is a simple example with a sample of the real set of observations published by Zellem et al.(2015) abut the exoplanet XO-2b.
I thank to the authors from disponilize those images.

The image "raw_data_with_all_sample.png" shows the result from reduction of the all observation data take in 2012-12-10.

xo2b.py -- script with the first part of reduction, following the default procedure of iraf reduction.
xo2b_phot.py -- script that calculating the aperture photometry.


WARNING:

All information about your data set, path where is your data and where you ant to save your results are edit in the YAML file on the input directory above.

## How to run:

#under astroconda environment

On bash terminal:

```
source activate astroconda
python xo2b.py
python xo2b_phot.py

```
