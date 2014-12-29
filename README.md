Large Binocular Telecope -- Large Binocular Camera
==================================================
Contents
--------
1. lc_extract.py
2. test_data

Comments
--------
Script(s) are free to anyone to use but the data are intended for demonstrative purposes only.  
Comments, questions, requests may be sent to <i>skylergrammer</i> @ gmail.com.  

lc_extract.py
-------------
Usage: extract light curves from multi-epoch imaging using the LBC. It is assumed that all the data for each chip are contained in their own separate directory.  

Installation:  
1. Clone LBT_LBC repository by executing in home directory (or wherever you want): `git clone https://github.com/skylergrammer/LBT_LBC.git`  
2. Add repository to $PYTHONPATH in bash: `export PYTHONPATH=$PYTHONPATH:insert_path_to_respository`  
3. Make lc_extract.py executable: `chmod u+x lc_extract.py`

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

Example:  
`cd test_data`  
`lc_extract.py --info M101_chip1.txt --chip 1 --dm 29.03 --zp zeropoints.txt --verbose --source V9`  
Output Produced:  
`***Getting light curve for V9***`  
`U-Band lightcurve filename: Ulc00172.535.1624`  
`B-Band lightcurve filename: Blc00238.535.1624`  
`V-Band lightcurve filename: Vlc00098.535.1624`  
`R-Band lightcurve filename: Rlc00554.535.1624`  
`Reading light curve file Ulc00172.535.1624`  
`Writing light curve to lc_V9_U.txt`  
`Reading light curve file Blc00238.535.1624`  
`Writing light curve to lc_V9_B.txt`  
`Reading light curve file Vlc00098.535.1624`  
`Writing light curve to lc_V9_V.txt`  
`Reading light curve file Rlc00554.535.1624`  
`Writing light curve to lc_V9_R.txt`  
