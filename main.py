#!/bin/python

import pandas as pd
import numpy as np
import sys
import os.path
import logging
import math

logging.basicConfig(format='%(levelname)s: %(message)s',level=logging.INFO)

def printUsage():
	print("Usage: ./main.py <inputCSVFile> <outputCSVFile>")

# Checking for the correct arguments
if len(sys.argv) <= 2:
	print(len(sys.argv))
	printUsage()
	exit(-1)

INPUTFILE = sys.argv[1]
OUTPUTFILE = sys.argv[2]

# Do some basic checks
if not os.path.isfile(INPUTFILE):
	logging.error("%s is no file!" % (INPUTFILE))
	exit(-1)


logging.info("Running exportVolksbank_GNUCash")
logging.info("inputCSVFile: %s" % (INPUTFILE))
logging.info("outputCSVFile: %s" % (OUTPUTFILE))

# Read INPUTFILE without header
try:
	logging.info("Reading inputfile...")
	dat = pd.read_csv(INPUTFILE, header=None)
except Exception as e:
	logging.error("Failed to read csv-file %s" % (INPUTFILE))
	logging.error(repr(e))
	exit(-1)

# Drop first 16 lines
try:
	logging.info("Dropping first 16 lines")
	dat.drop(np.arange(15), axis=0, inplace=True)
except Exception as e:
	logging.error("Failed drop  the first 15 lines")
	logging.error(repr(e))
	exit(-1)


# Export temporary to OUTPUTFILE
try:
	dat.to_csv(OUTPUTFILE, index=False, header=None)
except Exception as e:
	logging.error("Failed to write temporary csv-file %s" % (OUTPUTFILE))
	logging.error(repr(e))
	exit(-1)

# Read OUTPUTFILE with correct header
try:
	dat = pd.read_csv(OUTPUTFILE)
except Exception as e:
	logging.error("Failed to read temporary csv-file %s back in. This was written befor by this tool." % (OUTPUTFILE))
	logging.error(repr(e))
	exit(-1)

try:
	# Drop datarows with no Valuta (the lines at the bottom)
	logging.info("Dropping lines with empty Valuta")
	idx = dat.loc[pd.isna(dat["Valuta"]), :].index
	dat.drop(idx, axis=0, inplace=True)


	# Insert column "Beschreibung"
	logging.info("Inserting new column \"Beschreibung\"")
	dat.insert(10,"Beschreibung", dat["Vorgang/Verwendungszweck"] + ";" + dat.fillna("")["Zahlungsempf�nger"])

	# Add columns Soll/Haben
	logging.info("Inserting new columns \"Soll\" and \"Haben\"")
	dat.insert(15,"Soll",dat["Umsatz"]*(dat["Soll/Haben"]=="S"))
	dat.insert(16,"Haben",dat["Umsatz"]*(dat["Soll/Haben"]=="H"))
except Exception as e:
	logging.error("Failed to add one of the columns Beschreibung, Soll and Haben.")
	logging.error(repr(e))
	exit(-1)

# Exporting to OUTPUTFILE
try:
	logging.info("Saving outputfile %s" % (OUTPUTFILE))
	dat.to_csv(OUTPUTFILE, index=False)	
except Exception as e:
	logging.error("Failed write outputfile %s" % (OUTPUTFILE))
	logging.error(repr(e))
	exit(-1)
