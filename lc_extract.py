#! /usr/bin/env python

missing_mods = []

import sys
import os
import argparse
try:
  import numpy as np
except:
  missing_mods.append("numpy")
try:
  import matplotlib.pyplot as plt
except:
  missing_mods("matplotlib")

if missing_mods:
  sys.exit("\n***ERROR! You must have the following modules installed: %s\n" 
           % ', '.join(missing_mods))


def get_info_table(filename, verbose=False):
  '''
  Reads the file that contains the reference information for each object 
  -- e.g. id, light curve filenames, reference mags, etc.
  '''

  # Header column names
  header = ['x_shifted','y_shifted','id',   
            'lcR','xR','yR','magR','emagR',
            'lcV','xV','yV','magV','emagV',
            'lcB','xB','yB','magB','emagB',
            'lcU','xU','yU','magU','emagU']

  # Format for each column
  fmt = ['f8','f8','S30', 
         'S40','f8','f8','f8','f8',
         'S40','f8','f8','f8','f8',
         'S40','f8','f8','f8','f8',
         'S40','f8','f8','f8','f8',]

  try:
    if verbose: print("\nReading info table %s." % filename)
    info_table = np.genfromtxt(filename, names=header, autostrip=True, dtype=fmt,
                               missing_values=("0.0","000"), filling_values=np.nan)
  except Exception as e:
    if verbose: print(e)
    sys.exit("***Error whiile reading %s. Verify filename or use --v to see error." % filename) 

  return info_table


class ZeroPoints: 
  def __init__(self, data, dm):
    self.U = data["U"]
    self.eU = data["eU"]
    self.B = data["B"]
    self.eB = data["eB"]
    self.V = data["V"]
    self.eV = data["eV"]
    self.R = data["R"]
    self.eR = data["eR"]
    self.dm = dm

    
    
def get_zeropoints(filename, verbose=False):
  '''
  Reads the zero point info from the zero point file.
  '''

  header = ["chip","U","eU","B","eB","V","eV","R","eR"]
  fmt = ['L', 'f8', 'f8', 'f8', 'f8', 'f8', 'f8', 'f8', 'f8']
 
  try:
    if verbose: print("Reading zeropoints file: %s" % filename)
    zeropoints = np.genfromtxt(filename, names=header)
  except Exception as e:
    if verbose: print(e)  
    sys.exit("***Error! Cannot read %s, verify that it exists and has 9 columns." % filename)

  return zeropoints


def get_lc_data(filename, verbose=False):
  '''
  Reads in the actual light curve info from the light curve filename provided
  in the info table.
  '''

  header = ['mjd', 'dCounts', 'edCounts']
  if verbose: print("Reading light curve file %s" % filename)
  lc_data = np.genfromtxt(filename, usecols=[0,1,2], names=header)

  return lc_data


class RefInfo:
  '''
  Class to hold all the reference info.  Includes reference mags for each 
  bandpass, errors, and the filename for the light curve.
  '''

  def __init__(self, data, source):
    self.id = source
      
    ref_info = [x for x in data if source in x]

    if not ref_info:
      print("***ERROR: %s does not exist within the info table." % source) 
      self.lcU = False
      self.refU = False
      self.erefU = False
      self.lcB = False
      self.refB = False
      self.erefB = False
      self.lcV = False
      self.refV = False
      self.erefV = False
      self.lcR = False
      self.refR = False
      self.erefR = False
    else:
      ref_info = ref_info[0]
    
      if os.path.isfile(ref_info["lcU"]):
        self.lcU = ref_info["lcU"]
        self.refU = ref_info["magU"]
        self.erefU = ref_info["emagU"]
      else:
        self.lcU = False
        self.refU = False
        self.erefU = False

      if os.path.isfile(ref_info["lcB"]):
        self.lcB = ref_info["lcB"]
        self.refB = ref_info["magB"]
        self.erefB = ref_info["emagB"]
      else:
        self.lcB = False
        self.refB = False
        self.erefB = False

      if os.path.isfile(ref_info["lcV"]):
        self.lcV = ref_info["lcV"]
        self.refV = ref_info["magV"]
        self.erefV = ref_info["emagV"]
      else:
        self.lcV = False
        self.refV = False
        self.erefV = False

      if os.path.isfile(ref_info["lcR"]):
        self.lcR = ref_info["lcR"]
        self.refR = ref_info["magR"]
        self.erefR = ref_info["emagR"]
      else:
        self.lcR = False
        self.refR = False
        self.erefR = False

  def lc_exist(self):
    '''
    Call to print the file name for each light curve.  If it exists, prints a 
    file name.  If it does not exist, then indicates no light curve exists.
    '''

    if self.lcU: 
      print("U-Band lightcurve filename: %s" % self.lcU)
    else: 
      print("No U light curve")
    if self.lcB:
      print("B-Band lightcurve filename: %s" % self.lcB)
    else: 
      print("No B light curve")
    if self.lcV:
      print("V-Band lightcurve filename: %s" % self.lcV)
    else: 
      print("No V light curve")
    if self.lcR:
      print("R-Band lightcurve filename: %s" % self.lcR)
    else: 
      print("No R light curve")


def convert_to_lc(lc, src_ref_info, zps, band=None, chip=1):
  '''
  This function will convert counts, with respect to reference magnitude, to 
  magnitudes for each epoch and determine the error.
  '''

  # chips values range 1:4 but chip indices 0:3
  chip = chip - 1

  # Set the reference mags based on the given bandpass  
  if band == "U":
    ref_mag = src_ref_info.refU
    e_ref_mag = src_ref_info.erefU
    zp = zps.U[chip]
    ezp = zps.eU[chip]

  elif band == "B":
    ref_mag = src_ref_info.refB
    e_ref_mag = src_ref_info.erefB
    zp = zps.B[chip]
    ezp = zps.eB[chip] 

  elif band == "V":
    ref_mag = src_ref_info.refV
    e_ref_mag = src_ref_info.erefV
    zp = zps.V[chip]
    ezp = zps.eV[chip] 

  elif band == "R":
    ref_mag = src_ref_info.refR
    e_ref_mag = src_ref_info.erefR
    zp = zps.R[chip]
    ezp = zps.eR[chip] 

  # Default offset is the zeropoint plus the IRAF 25.0
  offset = zp + 25.0

  # Convert ref_mag to counts
  ref_counts = 10**((ref_mag-offset + zps.dm)/-2.5)
  
  # Convert delta counts to a magnitude
  counts_i = [ref_counts - x if x < ref_counts else np.nan 
              for x in lc['dCounts']]
  mag_i = np.array([-2.5*np.log10(x)+offset for x in counts_i])
  
  # Factor to be used in error propagation
  Beta = (2.5*e_ref_mag)**2
  
  # Errors in magnitudes
  emag_i = [np.sqrt(Beta + (1.1*y/x)**2 + ezp**2) 
            for x,y in zip(counts_i,lc['edCounts'])]  
  
  # Output list to hold light curve
  output = [x for x in zip(lc["mjd"], mag_i, emag_i)]

  return output


def extract_light_curves(src_ref_info, zps, chip=None, verbose=False):
  '''
  Extracts the light curves for each band.  
  '''

  if src_ref_info.lcU:
    lcU_data = get_lc_data(src_ref_info.lcU, verbose=verbose)
    light_curve_U = convert_to_lc(lcU_data, src_ref_info, zps, band="U", chip=chip)
    write_to_file(light_curve_U, src_ref_info.id, band="U", verbose=verbose)

  if src_ref_info.lcB:
    lcB_data = get_lc_data(src_ref_info.lcB, verbose=verbose)
    light_curve_B = convert_to_lc(lcB_data, src_ref_info, zps, band="B", chip=chip)
    write_to_file(light_curve_B, src_ref_info.id, band="B", verbose=verbose)

  if src_ref_info.lcV:
    lcV_data = get_lc_data(src_ref_info.lcV, verbose=verbose)
    light_curve_V = convert_to_lc(lcV_data, src_ref_info, zps, band="V", chip=chip)
    write_to_file(light_curve_V, src_ref_info.id, band="V", verbose=verbose)

  if src_ref_info.lcR:
    lcR_data = get_lc_data(src_ref_info.lcR, verbose=verbose)
    light_curve_R = convert_to_lc(lcR_data, src_ref_info, zps, band="R", chip=chip)
    write_to_file(light_curve_R, src_ref_info.id, band="R", verbose=verbose)


def write_to_file(light_curve, sourceid, band, verbose=False):

  filename = "_".join(["lc",sourceid, band+".txt"])

  if verbose: print("Writing light curve to %s" % filename)

  with open(filename, "w") as f:
    f.write("   ".join(["# mjd", band, "error"])+"\n")
    for line in light_curve:
      pretty_line = "   ".join(["%0.4f" % x for x in line])
      f.write(pretty_line+"\n")
    

def main():
  
  parser = argparse.ArgumentParser()
  parser.add_argument("--i", dest="info", required=True, help="Filename containing reference magnitudes, coordinates, ids, and filenames for the light curves.")
  parser.add_argument("--s", dest="source", nargs="+", help="Source(s) to extract or filename containing list of sources.  Give the string 'list' to print all sources in info table.")
  parser.add_argument("--zp", required=True, help="Filename containing the zeropoints for each chip and filter.")
  parser.add_argument("--dm", type=float, default=0, help="Distance modulus in magnitudes.  If not specified, default is 0.")
  parser.add_argument("--c", dest="chip", type=int, choices=[1,2,3,4], default=2, help="Chip number.  Choose from 1 2 3 4.  If not specifed, default is chip 2.")
  parser.add_argument("--v", dest="verbose", action="store_true", default=False, help="If set, then will print lots of messages.")
  args = parser.parse_args()
  
  # Read info table
  info_table = get_info_table(args.info, verbose=args.verbose)
  all_sources = info_table["id"]

  # Check to see if provided source is a filename
  if os.path.isfile(args.source[0]):
    print("List of sources provided.")
    source_list = [x.strip("\n").strip("\r") for x in open(args.source[0], "r")]  
  else: 
    source_list = args.source

  # Read in the zeropoints table and put into ZeroPoints class
  raw_zp = get_zeropoints(args.zp, verbose=args.verbose)
  zps = ZeroPoints(raw_zp, args.dm)

  if args.source[0].lower() == "list":
    for each in all_sources: print(each)
    exit()

  for source in source_list:
    if args.verbose:
      print("\n***Getting light curve for %s***" % source)

    # Put reference data into object
    try:
      src_ref_info = RefInfo(info_table, source)
      
      # Check to see which bandpasses have data      
      if args.verbose: src_ref_info.lc_exist() 
 
    except Exception as e:
      if args.verbose: print(e)
      continue
   
    # Extract the light curve and write to a file
    try:
      extract_light_curves(src_ref_info, zps, chip=args.chip, verbose=args.verbose)
      plt.show()
    except Exception as e:
      if args.verbose: print(e)
      continue


if __name__ == "__main__":
  main()
