import configparser
from db import initialize, test_connection

#Configuration
config = configparser.ConfigParser()
config.read('config.ini')

if config.sections() != ['DATABASE', 'OPTIONS', 'MODULES', 'INDIVIDUALS', 'SPOUSES', 'PARENTS']:
    raise Exception("One or more required configuration sections are missing.")

initialize(config['DATABASE'])
if test_connection() == False:
    raise Exception("Database connection failed. Check your connection configuration and try again.")

#Create Individuals

#Create Families

#Save Output