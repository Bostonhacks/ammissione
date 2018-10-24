#! /usr/local/bin python

'''
Created by Lucas Watson (@lkwatson)
Requires Python >=3.6

Script for running stats and processing the export of a mongo
database from Quill.
'''

import sys
import json


def load_mongo_json(filename):
    '''
    Given a path for a json file, load and return it.
    @param filename String representing name of json file
    @return json_data List of dicts for the json data
    '''
    with open(filename) as f:
        json_data = json.load(f)

        print(f"Loaded json with {len(json_data)} entries")

    return json_data


def get_val_for_field(entry, field, to_lower=True):
    '''
    Given an entry, get the value at field, which may be several levels
    @param entry Dict of the db entry
    @param field String representing field, of form `top/mid/lowest`, where
                 `lowest` is a key with a non-dict value.
    @return ent_level Value at field
    '''
    sub_fields = field.split('/')
    ent_level = entry
    for sub_f in sub_fields:
        if sub_f in ent_level.keys():
            ent_level = ent_level[sub_f]
        else:
            return None

    if to_lower:
        ent_level = ent_level.lower()

    return ent_level


def filter_for_attr(data, field, attr):
    '''
    Given a list of data entries, filter for entries which
    have acceptable attributes for a given field.
    @param data List representing entries of data
    @param field String for key in dict to filter for, levels split by "/"
    @param attr String acceptable value for the given field
    @return data List representing filtered entries
    '''
    filt_data = []
    attr = attr.lower()

    for i in range(len(data)):
        val = get_val_for_field(data[i], field)
        if val and (val in attr or attr in val):
            filt_data.append(data[i])

    return filt_data


def admits_by_field(data, field):
    '''
    Quill specific.
    Given a list of data entries, calculate admissions stats
    (waitlist/accept/confirm) for groups sorted by field.
    @param data List representing entries of data
    @param field Field to sort by
    @return None
    '''
    admit_stats = dict()
    group_stat = {'completedProfile': 0, 'admitted': 0,
                  'confirmed': 0, 'declined': 0}
    for i in range(len(data)):
        val = get_val_for_field(data[i], field)
        if not val:
            val = "No field"  # Keep track of accounts without the field

        if val not in admit_stats.keys():
            admit_stats[val] = {**group_stat}

        # TODO: make more clean
        for state in group_stat.keys():
            if data[i]['status'][state]:
                admit_stats[val][state] += 1

    # Output
    print(f"\nCategorized based on {field}\n")
    for cat, group in admit_stats.items():
        complete, admit, confirm, decl = group['completedProfile'], \
                                         group['admitted'], \
                                         group['confirmed'], \
                                         group['declined']

        total = complete + admit + confirm + decl

        print(f"{cat}, {total} applicants \n")
        print(f"Compl: {complete}, {100*complete/total}% \n\
Admit: {admit}, {100*admit/total}% \n\
Confm: {confirm}, {100*confirm/total}% \n\
Decln: {decl}, {100*decl/total}% ")
        print(f"––––")


if __name__ == '__main__':
    '''
    -f : path to json file of mongo export
    -filt : filter for a field and attribute,
            ex `-filt profile/busLocation=Toronto`
    -fieldstat : Get admissions stats sorted by a given field
    -out : print the resulting data
    '''
    cli_flags = ['-f', '-filt', '-fieldstat', '-out']

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

    all_data = load_mongo_json(received_args['-f'])

    procd_data = all_data
    if '-filt' in received_args.keys():
        raw_filts = received_args['-filt'].split(',')
        for f in raw_filts:
            assert len(f.split('=')) == 2, "Malformed filter string"
            field, attr = f.split('=')

            procd_data = filter_for_attr(procd_data, field, attr)

            print(f"Filtered to {len(procd_data)} entries")

    if '-fieldstat' in received_args.keys():
        admits_by_field(procd_data, received_args['-fieldstat'])
