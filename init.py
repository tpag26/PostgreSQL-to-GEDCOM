import os, json, configparser
from db import initialize_database, test_connection
from gedfile import add_line, render_output, initialize_file
from datetime import datetime
from indi import generate_individual_records
from fam import generate_family_records

config = configparser.ConfigParser()
config.read('config.ini')

def main():
    print('Validating configuration...')
    if config.sections() != ['DATABASE', 'OPTIONS', 'INDIVIDUALS', 'SPOUSES', 'PARENTS']:
        raise Exception("One or more required configuration sections are missing.")

    initialize_database(config['DATABASE'])

    print('Testing database connection...')
    conn_result = test_connection()
    if conn_result != True:
        raise Exception("Database connection failed. " + conn_result)

    if str(config['OPTIONS']['OUTPUT_MODE']).upper() == 'SIMPLE':
        #Simple Mode (single output with all records)
        process_file()
    elif str(config['OPTIONS']['OUTPUT_MODE']).upper() == 'ADVANCED':
        #Advanced Mode (separate output for each specified group)
        groups = json.loads(config['OPTIONS']['GROUPS'])
        for group in groups:
            process_file(group)
    else:
        raise Exception("Invalid output mode set in config.ini")

def process_file(group=None):    
    if group:
        print("Starting group '" + group + "'...")
    else:
        print("Starting processing...")

    initialize_file()

    #Set filename
    filename="output.ged"
    if group:
        filename = "output_" + str(group).lower() + '.ged'

    #Generate header
    try:
        print('Generating file header...')
        today = datetime.today()
        add_line(0,"HEAD")
        add_line(1,"SOUR",config['OPTIONS']['AUTHOR'])
        if group:
            add_line(2,"NAME",config['OPTIONS']['NAME'] + ' - ' + str(group))
        else:
            add_line(2,"NAME",config['OPTIONS']['NAME'])
        add_line(2,"VERS",config['OPTIONS']['VERSION'])
        add_line(1,"DATE",today.strftime("%d %b %Y"))
        add_line(2,"TIME",today.strftime("%H:%M:%S"))
        add_line(1,"FILE",filename)
        add_line(1,"GEDC")
        add_line(2,"VERS","5.5")
        add_line(2,"FORM","LINEAGE-LINKED")
        add_line(1,"CHAR","UTF-8")
    except Exception as e:
        raise Exception("Error generating header. " + str(e))

    #Generate individual records
    individuals = []
    try:
        print('Generating individuals records...')
        individuals = generate_individual_records(config,group)
    except Exception as e:
        raise Exception("Error generating individual records. " + str(e))

    #Generate family records
    try:
        print('Generating family records...')
        generate_family_records(config,individuals)
    except Exception as e:
        raise Exception("Error generating family records. " + str(e))

    #Save Output
    try:
        print('Saving to file...')
        text_file = open(os.path.join(config['OPTIONS']['OUTPUT_PATH'],filename), "w")
        text_file.write(render_output())
        text_file.close()
        print('GEDCOM file generated successfully.')
    except Exception as e:
        raise Exception("Error saving output file. " + str(e))

main()