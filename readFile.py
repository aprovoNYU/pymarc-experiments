#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, argparse
#reload(sys)
#sys.setdefaultencoding('utf8')

"""
This script will read an iso2709 file and display it using mnemonics codes. This hasn't been widely tested and there should be issues with encodings.
"""

from pymarc import MARCReader, marc8_to_unicode

parser = argparse.ArgumentParser(description='Read an iso2709 file and display it in a mnemonic format.')

parser.add_argument('filename')
parser.add_argument('-tag',  default="", help='A tag to filter the output')
parser.add_argument('-num',  default="", help='The number of the item we want to show')
parser.add_argument('-max',  default="", help='Max number of items to display, after that we exit')

args = parser.parse_args()

filename = args.filename
tagFilter = args.tag
recordNumber = args.num

if args.max == "": maxRecords = float("inf")
else: maxRecords = int(args.max)

print "Opening %s" % filename
nb = 1
reader = MARCReader(open(filename));

for record in reader:
	outputedLines = 0
	if recordNumber == "" or recordNumber == str(nb):
		for field in [x for x in record if (tagFilter == "" or x.tag == tagFilter)]:
			if outputedLines == 0:
				print "\n##### RECORD %s #####" % nb
				outputedLines += 1
			fieldValue = field.__str__().encode("utf-8")
			print fieldValue


	if recordNumber == str(nb) or (nb >= maxRecords):
		exit()
	nb += 1

print "%s records in file" % (nb - 1)