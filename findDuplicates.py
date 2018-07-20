#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, argparse

"""
This script will read n iso2709 files and find any record that is present in multiple
files
"""

from pymarc import MARCReader, marc8_to_unicode

parser = argparse.ArgumentParser(description='Read an iso2709 file and display it in a mnemonic format.')

parser.add_argument('filename', nargs='*')
args = parser.parse_args()

files = {}

common = {}
recs = {}
bsns_in_worldcat = []
for f in args.filename:
	print "******************************\nOpening %s" % f
	files[f] = {}
	files[f]['name'] = f
	files[f]['identifiers'] = {}
	files[f]['bsns'] = {}
	nb = 0
	reader = MARCReader(open(f));
	for record in reader:
		nb += 1
		#f001 = record.get_fields("856")[0]
		f001 = record["856"]["u"]
		try:
			f001 = f001.rstrip()
			if "hdl" in f001:
				#print(f001)
				f001_hdl = f001
		except:
			pass
	
		#print(f001_hdl)

		v001 = f001_hdl
		#print(v001)
		if v001 in common:
			common[v001][f] = 1
		else:
			common[v001] = {}
			common[v001][f] = 1
		files[f]['identifiers'][v001] = 1

		recs[v001] = {}

		try:
			bsn = record.get_fields("001")[0]
			print bsn
			bsn_value = bsn.value()
			files[f]['bsns'][v001] = {}
			files[f]['bsns'][v001]['bsn']=bsn_value
		except:
			pass
		try:
			bsn = record["024"]['a']
			bsn_value = bsn
			files[f]['bsns'][v001] = {}
			files[f]['bsns'][v001]['bsn']=bsn_value
		except:
			pass
	#	print(bsn)

		
	#print(recs)
	print "> %s records" % nb
#print(files[f]['bsns'][v001]['bsn'])

# Store the number of records at the begining

for f in files:	
	files[f]['count_orig'] = len(files[f]['identifiers'])
	
	
print "\n***   Analyze duplicates   ***"
nb = 0
for v001 in common:
	# Clean the values in files to be able to identify uniqueness of each file
	if len(common[v001]) > 1:
		for f in files:
			if v001 in files[f]['identifiers']:
				del(files[f]['identifiers'][v001])
			if v001 in files[f]['bsns'] and "_" not in files[f]['bsns'][v001]['bsn']:
				print(v001, files[f]['bsns'][v001]['bsn'])

	#	print nb, ":", v001, len(common[v001])
		nb += 1

	#elif len(common[v001]) <= 1:
	#	print v001, len(common[v001])


print "> Total number of ID: %s" % len(common)
print "> ID common between at least 2 files: %s" % nb

print "> Uniqueness for each file :"
for f in files:
	print "\t%s : %s record(s) [out of %s]" % (f, len(files[f]['identifiers']), files[f]['count_orig'])
	#print(common)
#	print(files)