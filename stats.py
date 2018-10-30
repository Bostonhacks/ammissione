#! /usr/local/bin python

'''
Created by Lucas Watson (@lkwatson)
Requires Python >=3.6

Script for running stats on registrant data from Quill.
'''

import sys
import load


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
        val = load.get_val_for_field(data[i], field)
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

        total = complete

        print(f"{cat}, {total} applicants \n")
        print(f"Admit: {admit}, {100*admit/total:.2f}% \n\
Confm: {confirm}, {100*confirm/total:.2f}% \n\
Decln: {decl}, {100*decl/total:.2f}% ")
        print(f"––––")


if __name__ == '__main__':
    '''
    -f : path to json file of mongo export
    -filt : filter for a field and attribute,
            ex `-filt profile/busLocation=Toronto`
    -fieldstat : Get admissions stats sorted by a given field
    -out : print the resulting field for filtered data (or unfiltered)
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

    all_data = load.load_mongo_json(received_args['-f'])

    procd_data = all_data
    if '-filt' in received_args.keys():
        raw_filts = received_args['-filt'].split(',')
        for f in raw_filts:
            assert len(f.split('=')) == 2, "Malformed filter string"
            field, attr = f.split('=')

            procd_data = load.filter_for_attr(procd_data, field, attr)

            print(f"Filtered to {len(procd_data)} entries")

    if '-fieldstat' in received_args.keys():
        admits_by_field(procd_data, received_args['-fieldstat'])

    if '-out' in received_args.keys():
        for ent in procd_data:
            print(ent[received_args['-out']])
