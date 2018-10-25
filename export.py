#! /usr/local/bin python

'''
Created by Lucas Watson (@lkwatson)
Requires Python >=3.6

Script for exporting registrant data with options.
'''

import sys
import load
import csv


def export_to_csv(data, fields, filename, namemagic=True):
    '''
    Quill specific
    Exports the given data to a csv with the requested fields.
    @param data List representing entries of data
    @param fields String comma separated fields ex "name,age,profile/birth"
    @param filename File to write to
    @return None
    '''
    field_list = fields.split(',')

    csv_data = list()
    if 'namemagic' in field_list:
        inx = field_list.index('namemagic')
        label_list = [*field_list]
        label_list[inx] = 'First Name'
        label_list.insert(inx + 1, 'Last Name')

        csv_data.append(label_list)
    else:
        csv_data.append(field_list)

    print(f"Exporting {len(data)} entries to csv")

    for i in range(len(data)):
        new_row = list()

        for fld in field_list:
            if fld == 'namemagic':
                fullname = load.get_val_for_field(data[i], 'profile/name')
                if fullname:
                    fullname = fullname.split(' ')
                    first = ''.join(fullname[:1]).title()
                    last = ''.join(fullname[1:]).title()

                    new_row.extend([first, last])
                else:
                    new_row.extend([None, None])
            else:
                new_row.append(load.get_val_for_field(data[i], fld))

        csv_data.append(new_row)

    # csv_data is a list of lists
    with open(filename, 'w+') as out:
        writer = csv.writer(out, lineterminator='\n')
        writer.writerows(csv_data)


if __name__ == '__main__':
    '''
    -f : path to json file of mongo export
    -filt : filter for a field and attribute,
            ex `-filt profile/busLocation=Toronto`
    -fields : list of fields, ex "profile/gender,name,age"
              **Special fields**
              namemagic: will take a full name and split at
              the first space, returning two fields (first and last name)
    -o : Name of output file
    '''
    cli_flags = ['-f', '-filt', '-fields', '-o']

    assert len(sys.argv[1:]) % 2 == 0, \
        "Incorrect number of args"

    received_args = dict()
    for i in range(1, len(sys.argv), 2):
        flag = sys.argv[i]
        arg = sys.argv[i+1]

        if flag in cli_flags:
            received_args[flag] = arg
        else:
            raise ValueError(f"Invalid flag: {flag}")

    all_data = load.load_mongo_json(received_args['-f'])

    procd_data = all_data
    if '-filt' in received_args.keys():
        raw_filts = received_args['-filt'].split(',')
        for f in raw_filts:
            assert len(f.split('=')) == 2, "Malformed filter string"
            field, attr = f.split('=')

            procd_data = load.filter_for_attr(procd_data, field, attr)

            print(f"Filtered to {len(procd_data)} entries")

    export_to_csv(procd_data, received_args['-fields'], received_args['-o'])
