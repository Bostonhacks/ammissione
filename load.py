#! /usr/local/bin python

'''
Created by Lucas Watson (@lkwatson)
Requires Python >=3.6

Script for loading and processing the export of a mongo
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
        ent_level = str(ent_level).lower()

    return ent_level


def filter_for_attr(data, field, attr):
    '''
    Given a list of data entries, filter for entries which
    have acceptable attributes for a given field.

    Does everything with string comparison.

    @param data List representing entries of data
    @param field String for key in dict to filter for, levels split by "/"
    @param attr String acceptable value for the given field
    @return data List representing filtered entries
    '''
    filt_data = []
    attr = str(attr).lower()

    for i in range(len(data)):
        val = str(get_val_for_field(data[i], field))
        if val and (val in attr or attr in val):
            filt_data.append(data[i])

    return filt_data
