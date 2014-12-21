Large Binocular Telecope -- Large Binocular Camera
==================================================
Contents
--------
1. lc_extract.py
2. test_data

lc_extract.py
-------------
Usage: extract light curves from multi-epoch imaging using the LBC. It is assumed that all the data for each chip are contained in their own separate directory.  

Installation:  
Clone repository by executing: `git clone https://github.com/skylergrammer/LBT_LBC.git`


Required input:  

1. Info table file containing the reference data
2. Raw light curve output from ISIS  
3. File containing the zeropoints for each chip and each band  

Parameters:  
1. --info: Filename of info table.  
2. --source: Object(s) to extract. May be a file with a list.  
3. --zp: Filename containing the zeropoints.  
4. --dm: Distance modulus.  
5. --chip: Choose from 1 2 3 4.  
6. --verbose: If specified, will print some messages as it goes.  

Output:  
For each source, will output a file file for each bandpass.  Format is mjd (days), magnitude, and magnitude error.  
lc_<i>source</i>_<i>band</i>.txt
