from db import get_individuals
from gedfile import add_line

def generate_individual_records(config,group=None):
    data = get_individuals(config['INDIVIDUALS'],group)
        
    for row in data:
        id_number = str(row[0])
        name = str(row[1]) + ' ' + str(row[2])
        birth_date = str(row[4])
        death_date = str(row[5])
        sex = str(row[3]).upper()

        add_line(0,"@I{}@".format(id_number),"INDI")
        add_line(1,"NAME","/{}/".format(name))
        add_line(1,"BIRT")
        add_line(2,"DATE",birth_date)
        add_line(1,"DEAT")
        add_line(2,"DATE",death_date)
        add_line(1,"SEX",sex)
    
    return data