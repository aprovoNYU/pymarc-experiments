#!/usr/bin/env python3

import pymarc
from pymarc import Record
import copy

#AAP to do: possibly add dates and times to file names?

''' reed's code to sort the fields in numerical order '''
def sort_record(record):
    new_record = Record()
    new_record.leader = copy.deepcopy(record.leader)

    for field in record:
        new_record.add_ordered_field(field)

    return new_record

''' create readers for both input files '''
oclc_file = open('180322-oclc_records.mrc', 'rb')
oclc_reader = pymarc.MARCReader(oclc_file, to_unicode=True, force_utf8=True, utf8_handling='strict')

local_file = open('mrc_out_all.mrc', 'rb')
local_reader = list(pymarc.MARCReader(local_file, to_unicode=True, force_utf8=True, utf8_handling='strict'))

''' create list of first aco handle id to appear in each oclc record '''
oclc_ids = []
#also sort the records and write them to a new file
oclc_sorted = pymarc.MARCWriter(open('180322-oclc_records_sorted.mrc', 'wb+'))
for record in oclc_reader:
    for field in record.get_fields('856'):
        try:
            if 'Arabic Collections' in field['y']:
                record_id = field['u'].split('/')[-1].strip()
                if record_id == '2bvq87gf':
                    record_id = '34tmpkff'
                oclc_ids.append(record_id)
                break
        except TypeError:
            pass
    new_oclc_rec = sort_record(record)
    oclc_sorted.write(new_oclc_rec)
oclc_sorted.close()
''' create dictionary of all handle ids present in local records where value is the pymarc record '''
local_records = {}
for record in local_reader:
    for field in record.get_fields('856'):
        try:
            record_id = field['u'].split('/')[-1].strip()
            local_records[record_id] = record
        except (AttributeError, TypeError):
            pass

''' write shared records to new file in same sequence as the oclc input file '''
in_oclc = pymarc.MARCWriter(open('aco_in_oclc.mrc', 'wb+'))
obj_ids = []
for record_id in oclc_ids:
    record = local_records.pop(record_id)
    obj_ids.append(id(record))
    new_rec = sort_record(record)
    in_oclc.write(new_rec)
in_oclc.close()

''' check ids and output all records that did not make it to oclc '''
local_only = pymarc.MARCWriter(open('aco_local_only.mrc', 'wb+'))
for record in local_reader:
    if id(record) not in obj_ids:
        local_only.write(record)
local_only.close()
