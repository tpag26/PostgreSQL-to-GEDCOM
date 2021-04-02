# PostgreSQL to GEDCOM

> **Generate basic GEDCOM files using genealogy data in a relational PostgreSQL database**

A configurable Python-based GEDCOM file generator that creates Lineage-Linked GEDCOM-compliant (v5.5) genealogy data files from a relational PostgreSQL database. At this point in time, only `FAM` (Family) and `INDI` (Individual) record types are supported.

## Usage
After defining your configuration file (see below) simply run init.py. This utility is purposefully designed not to require interactive user inputs so that it can be executed as part of automated pipelines. For example, you could deploy this to an Azure Function App / AWS Lambda and run it on a schedule to maintain an up-to-date GEDCOM representation of your database.

## Configuration File
Define a config.ini file with the following information:
```
[DATABASE]
HOST=127.0.0.1
PORT=5432
NAME=xxxx
USERNAME=postgres
PASSWORD=xxxx

[OPTIONS]
AUTHOR=Thomas Pagram
NAME=Family Tree
VERSION=0.1.0
OUTPUT_PATH=./
OUTPUT_MODE=ADVANCED
GROUPS=["Smith","Turner"] 
#OUTPUT_MODE can be set as 'SIMPLE' or 'ADVANCED'. 'SIMPLE' will output a single GEDCOM file with all records. 'ADVANCED' will output a separate GEDCOM file for each item in 'GROUPS', based on the values in 'GROUP_COLUMN'
#GROUPS only required if OUTPUT_MODE is 'ADVANCED'

[INDIVIDUALS]
TABLE_NAME=persons
ID_COLUMN=id
FIRSTNAME_COLUMN=first_name
LASTNAME_COLUMN=last_name
SEX_COLUMN=gender
SEX_MALE_VALUE=m
SEX_FEMALE_VALUE=f
BIRTHDATE_COLUMN=year_birth
DEATHDATE_COLUMN=year_death
GROUP_COLUMN=family_group
#GROUP_COLUMN required if OUTPUT_MODE is 'ADVANCED'

[SPOUSES]
TABLE_NAME=spouses
INDIVIDUAL1_COLUMN=first_person_id
INDIVIDUAL2_COLUMN=second_person_id

[PARENTS]
TABLE_NAME=persons
INDIVIDUALID_COLUMN=id
MOTHERID_COLUMN=mother_id
FATHERID_COLUMN=father_id
```