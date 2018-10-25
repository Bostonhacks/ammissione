# Ammissione scripts

Scripts used for processing applicants and running stats.

## Usage
### Run basic stats
#### Example
```
python3 stats.py -f 2018-xx-xx-usersMongoExport.json -filt profile/school=Queens -fieldstat profile/graduationYear
```
#### Args
```
-f : path to json file of mongo export
-filt : filter for a field and attribute,
        ex `-filt profile/busLocation=Toronto`
-fieldstat : Get admissions stats sorted by a given field
-out : print the resulting field for filtered data (or unfiltered)
```
### Export to CSV (probably for mailchimp)
Example
```
python3 export.py -f xxx-usersMongoExport.json -filt status/completedProfile=true -fields email,namemagic,status/admitted,status/confirmed,status/declined,profile/busLocation -o my_little_csv_export.csv
```
#### Args
```
-f : path to json file of mongo export
-filt : filter for a field and attribute,
        ex `-filt profile/busLocation=Toronto`
-fields : list of fields, ex "profile/gender,name,age"
-o : Name of output file
```

## Useful application fields from Quill
```
email

status/completedProfile (Bool)
status/admitted (Bool)
status/confirmed (Bool)
status/declined (Bool)

status/checkedIn (Bool)
status/reimbursementGiven (Bool)

confirmation/ (Many sub fields)

profile/busLocation (String)
profile/resumeSubmitted (Bool)
profile/ethnicity (String, options)
profile/gender (String, options)
profile/graduationYear (String, options)
profile/major (String)
profile/name (String)
profile/school (String)
profile/adult (Bool)

teamCode (String)

_id (mongo)
```
