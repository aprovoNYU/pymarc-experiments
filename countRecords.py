#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymarc
import sys, getopt, os
import time
start_time = time.time()

"""
This script will count the number of marc records in an iso2709
The process used might not be error-proof but it should be fast enough. 
Use the --errorproof param to use pymarc which has better error handling
"""

def countRecords(filename, errorproof = False):
	with open(filename) as f:
		nb = 0
		if errorproof == True:
			# We are going to use pymarc process
			for rec in pymarc.MARCReader(file(filename)): 
				nb += 1
		else:
			first5 = f.read(5)
			
			while first5 != "" and len(first5) == 5:
				length = int(first5)
				chunk = f.read(length - 5)
				chunk = first5 + chunk
				first5 = f.read(5)
				nb += 1
	return nb

# Displaying how to use the program
def usage():
	print 'countRecords.py -i <inputfile> --errorproof'

def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hi:", ["errorproof"])
	except getopt.GetoptError:
		usage()
		sys.exit(2)	

	errorProof = False
	filename = ""

	for o, a in opts:
		if o == "-i":
			filename = a
		elif o in ("--errorproof"):
			errorProof = True
		else:
			print "Unknown parameter: %s" % o
	if filename == "" or not os.path.isfile(filename):
		usage()
		sys.exit()

	print countRecords(filename, errorProof), "records in %s" % filename

if __name__ == "__main__":
	main()
	print("--- %s seconds ---" % (time.time() - start_time))