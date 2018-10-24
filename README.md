# Ammissione scripts

Scripts used for processing applicants and running stats.

## Example
```
python3 load.py -f 2018-xx-xx-usersMongoExport.json -filt profile/school=Queens -fieldstat profile/graduationYear
```

## Usage
```
-f : path to json file of mongo export
-filt : filter for a field and attribute,
        ex `-filt profile/busLocation=Toronto`
-fieldstat : Get admissions stats sorted by a given field
-out : print the resulting data
```
