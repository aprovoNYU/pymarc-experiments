#!/usr/bin/env python3

import pymarc
from pymarc import Record
import copy
import csv

#getting unique items in a list in a fast way, courtesy of https://www.peterbe.com/plog/uniqifiers-benchmark

def f5(seq, idfun=None): 
   # order preserving
   if idfun is None:
       def idfun(x): return x
   seen = {}
   result = []
   for item in seq:
       marker = idfun(item)
       # in old Python versions:
       # if seen.has_key(marker)
       # but in new ones:
       if marker in seen: continue
       seen[marker] = 1
       result.append(item)
   return result

''' create readers for both input files '''
oclc_file = open('180322-oclc_records.mrc', 'rb')
oclc_reader = pymarc.MARCReader(oclc_file, to_unicode=True, force_utf8=True, utf8_handling='strict')

local_file = open('aco_in_oclc.mrc', 'rb')
local_reader = list(pymarc.MARCReader(local_file, to_unicode=True, force_utf8=True, utf8_handling='strict'))

inst_code = input('Enter the institutional code: ')

field_list = []
#unique_field_list = 0
count1=0
#open the OCLC mrc file
for record in oclc_reader:
	#get the 24, which has institutional codes in it
	record24 = record.get_fields("024")
	for field24 in record24:
		# field24a = field24.get_subfields("a")
		# print(field24.get_subfields("a"))
		#work just with records from one institution
		if inst_code in field24.value():
			print(field24.value())
			#count how many records are in that institution;
			#this can be compared to the number returned using MARCEdit's extract records feature
			count1 +=1
			#turn the records into a dictionary, so it's easier to just get the field names
			record_dict = record.as_dict()
			#get all the fields and put them in a list
			for field_dict in record_dict['fields']:
				for field_key in field_dict:
					print(field_key)
					field_list.append(field_key)
count2=0
for record in local_reader:
	#get the 24, which has institutional codes in it
	record003 = record.get_fields("003")
	for field003 in record003:
		# field24a = field24.get_subfields("a")
		#print(field003)
		#work just with records from one institution
		if inst_code in field003.value():
			print(field003.value())
			#count how many records are in that institution;
			#this can be compared to the number returned using MARCEdit's extract records feature
			count2+=1
			#turn the records into a dictionary, so it's easier to just get the field names
			record_dict = record.as_dict()
			#get all the fields and put them in a list
			for field_dict in record_dict['fields']:
				for field_key in field_dict:
					print(field_key)
					field_list.append(field_key)
#NEXT UP: I want to do this for the local reader, because i want a comprehensive list of fields.
#might need to make some more lists!
print(field_list)
#dedupe the field list so you just get them listed one time
unique_field_list = f5(field_list)
unique_field_list_sorted = sorted(unique_field_list)
print(unique_field_list_sorted)
print("number of",inst_code,"records: ", "oclc= ",count1, "local= ",count2)

#NEXT UP: I want to write these reports to CSVs so I can put them in my spreadsheet.

with open ("field_report_%s.csv" %inst_code, 'w') as file:
	writer = csv.writer(file)
	writer.writerow(['MARC_fields'])
	for field in unique_field_list_sorted:
		#with help from: https://stackoverflow.com/questions/6916542/writing-list-of-strings-to-excel-csv-file-in-python
		writer.writerow([field],)
print("good job!")
