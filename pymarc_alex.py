import pymarc
from pymarc import MARCReader
import csv
from datetime import datetime, date, time

filetime = datetime.now()
filetime = filetime.strftime("%Y-%m-%d_%I-%M_%p")
reader = MARCReader(open("180322-oclc_records.mrc", 'rb'))
count =0
bsn_list = []
for record in reader:
		bsn_subfield = record.get_fields("024")[0].get_subfields("a")[0]
		if "(NyNyUACO)" in bsn_subfield:
			print(bsn_subfield)
			just_bsn = bsn_subfield.replace("(NyNyUACO)","")
			print(just_bsn)
			bsn_list.append(just_bsn)
			count +=1
print(count)
print(bsn_list)
for x in bsn_list:
	print(x)


with open ("aco_IEs_in_worldcat_%s.csv" %filetime, 'w') as file:
	writer = csv.writer(file)
	writer.writerow(['bsn_number'])
	for x in bsn_list:
		#with help from: https://stackoverflow.com/questions/6916542/writing-list-of-strings-to-excel-csv-file-in-python
		writer.writerow([x],)
print("good job!")