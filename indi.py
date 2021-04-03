from db import get_individuals, get_individual
from gedfile import add_line, already_exists

def generate_individual_records(config,group=None):
    data = get_individuals(config['INDIVIDUALS'],group)
        
    for row in data:
        id_number = str(row[0])
        name = (str(row[1]) + ' ' + str(row[2])).replace("/","-")
        birth_date = row[4]
        death_date = row[5]
        sex = row[3]

        add_line(0,"@I{}@".format(id_number),"INDI")
        add_line(1,"NAME","/{}/".format(name))
        if birth_date:
            add_line(1,"BIRT")
            add_line(2,"DATE",str(birth_date))
        if death_date:
            add_line(1,"DEAT")
            add_line(2,"DATE",str(death_date))
        if sex:
            add_line(1,"SEX",str(sex).upper())
    
    return data

def add_individual_record(config,id):
    if already_exists(id,"INDI") == False:
        individual = get_individual(config['INDIVIDUALS'],id)
        id_number = str(individual[0])
        name = (str(individual[1]) + ' ' + str(individual[2])).replace("/","-")
        birth_date = individual[4]
        death_date = individual[5]
        sex = individual[3]

        add_line(0,"@I{}@".format(id_number),"INDI")
        add_line(1,"NAME","/{}/".format(name))
        if birth_date:
            add_line(1,"BIRT")
            add_line(2,"DATE",str(birth_date))
        if death_date:
            add_line(1,"DEAT")
            add_line(2,"DATE",str(death_date))
        if sex:
            add_line(1,"SEX",str(sex).upper())