# Discrete Sky Operator (DiSkO) Synthesis Imaging

[![Build Status](https://travis-ci.org/tmolteno/disko.svg?branch=master)](https://travis-ci.org/tmolteno/disko)

Author: Tim Molteno tim@elec.ac.nz

Its so cool its POINTLESS. Image by using the telescope operator keeping track of the telescope null-space and range-space. This software 
carries out a sparsity reduction by regularization and controls the volume of the sky solution. The result is an imaging algorithm that is sensitive to diffuse broad sources, and does not require restoration like CLEAN. Publications to appear :)

## Howto

    disko --display --show-sources

To load a data from a measurement set 

    disko --ms test_data/test.ms --tikhonov --nside 32 --PDF

## VLA imaging with DiSkO

Download the VLA 5GHZ continuum survey measurement set. AG733_A061209.xp1 from the NRAO site.

Calibrate and then split the measurement set, following the CASA tutorial [https://casaguides.nrao.edu/index.php/VLA_5_GHz_continuum_survey_of_Seyfert_galaxies]

    disko --fov 0.01 --ms NGC1194.split.ms --SVG --arcmin 0.0025 --tikhonov
## More challenging

This tutorial should generate a file with lots of diffuse radiation. 
[https://casaguides.nrao.edu/index.php/VLA_Continuum_Tutorial_3C391-CASA5.5.0]

    wget http://casa.nrao.edu/Data/EVLA/3C391/3c391_ctm_mosaic_10s_spw0.ms.tgz
    wget https://github.com/jaredcrossley/CASA-Guides-Script-Extractor/blob/master/extractCASAscript.py
    
    python extractCASAscript.py 'https://casaguides.nrao.edu/index.php?title=VLA_Continuum_Tutorial_3C391-CASA5.5.0'

Then in CASA

    execfile("VLAContinuumTutorial3C391-CASA5.5.0.py")
    
This should generate a suitable measurement set to image.

## TODO

* Add a --full-sphere option which fixes the sphere in celestial coordinates, and then points the phase center of an observation correctly. Requires a beam pattern to be specified (or at least a hemispherical beam). A beam is a sky vector mask. I.e., should fall to zero 'outside' the beam.

## Changelog

0.9.0b4 Improve measurement set reading. 
        Use the mean RMS value for a single noise estimate on visibilities.
        Use the correct rank value in overdetermined skies.
        Truncate the SVD to keep the condition number of the telescope less than 50.
0.9.0b3 Full Bayesian Inference is workin. Fix bug in meshio (after upgrade beyond 4)
0.9.0b2 Add a multivariate gaussian object. Fix ms_helper. Handle the case where the rank of the telescope operator is not full.
0.9.0b1 Move to a real telescope operator.
0.8.0b5 Allow FISTA to calculate its own largest eigenvalue if negative values are passed in.
0.8.0b4 Clean up code and avoid recalculating harmonics. 
        Added a DirectImagingOperator that performs the discrete Fourier Transform.
0.8.0b3 Add --fista command line option to use the FISTA solver.
0.8.0b2 Add an lsqr option to force the slightly slower lsqr algorithm in place of lsmr.
0.8.0b1 Add a matrix-free operator that actually works. Process UVW in meters.
0.7.0b10 Clean up tests. Rename the DiSkOOperator and get it going.  Fix up timestamp loading, use the correct frequency (based on channel parameter)
0.7.0b9 Fix up timestamp loading
0.7.0b8 Optimize mesh at each stage of refinement.
0.7.0b7 Better refinement.
0.7.0b6 Limit gradient calculation to cells above nyquist limit
0.7.0b5 Improve channel selection
0.7.0b4 Allow selection of the channel number
0.7.0b2 New adaptive meshing on gradient
0.7.0b1 Add adaptive meshing and --adaptive option
0.6.0b9 Report Nyquist resolution
0.6.0b7 MS were being read incorrectly - the UVW are measured in meters, not wavelengths!
0.6.0b6 Correct field pointing from measurement sets.
0.6.0b5 Reduce memory requirements by around 25%.
0.6.0b4 Report the r^2 value.
0.6.0b2  Use dask for very large jobs (use the --dask switch)
0.6.0b1  Get data from Measurement Sets!
0.5.0b5 Allow sources not to be shown.
0.5.0b4 Override plot in HPSubSphere to allow for non-normal pixels.
0.5.0b3 Added elliptical source circle projections in SVG.
0.5.0 Getting imaging logic better. Added L2 regularization, and cross-validation
