#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, argparse
#reload(sys)
#sys.setdefaultencoding('utf8')

"""
This script will read an iso2709 and check if there might be problems (like carriage returns?).
"""

from pymarc import MARCReader, marc8_to_unicode

parser = argparse.ArgumentParser(description='Read an iso2709 file and display it in a mnemonic format.')

parser.add_argument('filename')

args = parser.parse_args()

filename = args.filename

print "Opening %s" % filename
nb = 1
reader = MARCReader(open(filename));

for record in reader:
	outputedLines = 0
	for field in record:
		fieldValue = field.__str__().encode("utf-8")
		if "\n" in fieldValue:
			print "Carriage return in record #%s (%s field)" % (nb, field.tag)

	nb += 1

print "%s records in file" % (nb - 1)