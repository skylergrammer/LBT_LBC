Large Binocular Telecope -- Large Binocular Camera
==================================================
Contents
--------
1. lc_extract.py  
2. test_data  
3. LBC data for M101, N2403, and M81  

Comments
--------
Script(s) are free to anyone to use but the data are intended for demonstrative purposes only.  
Comments, questions, requests may be sent to <i>skylergrammer</i> @ gmail.com.  

lc_extract.py
-------------
<b>Usage:</b>  
Extract light curves from multi-epoch imaging using the LBC. It is assumed that all the data for each chip are contained in their own separate directory.  

<b>Installation:</b>  
1. Clone LBT_LBC repository by executing in home directory (or wherever you want): `git clone https://github.com/skylergrammer/LBT_LBC.git`  
2. Add repository to $PATH in bash: `export PATH=$PATH:insert_path_to_respository`  
3. Make lc_extract.py executable: `chmod u+x lc_extract.py`

<b>Required input:</b>  
1. Info table file containing the reference data
2. Raw light curve output from ISIS  
3. File containing the zeropoints for each chip and each band  

<b>Parameters:</b>  
1. --i info: Filename of info table.  
2. --s source: Object(s) to extract. May be a file with a list.  
3. --zp zeropoints: Filename containing the zeropoints.  
4. --dm distance_modulus: Distance modulus.  
5. --c chip_number: Choose from 1 2 3 4.  
6. --v: If specified, code operates in verbose mode.  

<b>Calculations:</b>  
Each epoch is subtracted from the reference image to get differential light curves for each pixel. After subtraction, sources are then photometered to give the difference in counts with respect to the reference.  Thus the light curve files are give `MJD`, `delta_counts`, and an error. The reference images are photometered using <i>DAOPHOT</i> and magnitdues given by:  
`mag_ref = mag_instrumental + offset + distance_modulus`  
where `offset = zeropoint + 25.0`  

To get an apparent magnitude for each epoch, it is necessary to convert the reference magnitude to counts:  
`ref_counts = 10**(-0.4*(ref_mag-offset + distance_modulus))`  

Then, `delta_counts` are converted to total counts for a given epoch by subtracting `delta_counts` from `ref_counts`:  
`counts = ref_counts - delta_counts`  

Finally, apparent magnitudes are calculated for each epoch by the following formula:  
`mag = -2.5*np.log10(counts) + offset`  

<b>Output:</b>  
For each source, will output a file file for each bandpass.  Format is mjd (days), magnitude, and magnitude error.  
lc_<i>source</i>_<i>band</i>.txt

<b>Example:</b>  
`cd test_data`  
`lc_extract.py --i M101_chip1.txt --c 1 --dm 29.03 --zp zeropoints.txt --v --s V9`  
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
