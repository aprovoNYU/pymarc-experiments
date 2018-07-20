#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pymarc import MARCReader, marc8_to_unicode
import sys, getopt
import os.path

import time
start_time = time.time()

"""
This script will split a file in multiple files each containing a specificed number of records.
"""

def usage():
	print 'splitFile.py -i <inputfile> -o <outputfilename-format> -n <records-by-file>'

def main():
	inputfile = ''
	outputfile = ''
	numberInFile = ''
	try:
		opts, args = getopt.getopt(sys.argv[1:],"hi:o:n:",["ifile=","ofile="])
	except getopt.GetoptError:
		usage()
		sys.exit(2)

	for opt, arg in opts:
		if opt == '-h':
			usage()
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputfile = arg
		elif opt in ("-o", "--ofile"):
			outputfile = arg
		elif opt in ("-n"):
			numberInFile = int(arg)

	if inputfile == "" or numberInFile == "":
		print "******* Missing argument *******"
		usage()
		sys.exit()

	if outputfile == "":
		# we are going to use the basename of the file
		outputfile = "%s-%s" % (os.path.splitext(inputfile)[0], numberInFile)

	fileCpt = 1
	reader = MARCReader(open(inputfile));
	out = open("%s-%s.mrc" % (outputfile, fileCpt), 'wb');

	nb = 1
	for record in reader:
		out.write(record.as_marc())
		if (nb % numberInFile) == 0:
			out.close()
			fileCpt += 1
			out = open("%s-%s.mrc" % (outputfile, fileCpt), 'wb');
			print "Changement de fichier (%s)" % (nb)
		nb += 1
	out.close()

if __name__ == "__main__":
	main()
	print("--- %s seconds ---" % (time.time() - start_time))
		