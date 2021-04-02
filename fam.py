from db import get_spouses, get_parents, get_individuals
from gedfile import add_line

config = None

def generate_family_records(config_file,individuals_in_group): 
    global config
    config = config_file
    generate_spouses(individuals_in_group)
    generate_children(individuals_in_group)

def generate_spouses(individuals_in_group):
    #Get spouses for the individuals in the group
    scope = []
    for individual in individuals_in_group:
        scope.append(str(individual[0]))

    spouse_data = get_spouses(config['SPOUSES'],scope)

    #Get gender data for all individuals because we can't assume all spouses of inviduals_in_group are also in the same group
    all_individuals = get_individuals(config['INDIVIDUALS'])

    #Iterate through each spouse record
    for idx, row in enumerate(spouse_data):
        person1 = row[0]
        person2 = row[1]
        person1_gender = None
        person2_gender = None
        person1_reltype = None
        person2_reltype = None

        #Get the gender for both individuals
        for individual in all_individuals:
            if individual[0] == person1:
                person1_gender = individual[3]
            if individual[0] == person2:
                person2_gender = individual[3]

        #See if we have enough information to work out who will be the husband and who will be the wife
        if (str(person1_gender).upper() == "M") and (str(person2_gender).upper() == "F"):
            person1_reltype = 'HUSB'
            person2_reltype = 'WIFE'
        elif (str(person1_gender).upper() == "F") and (str(person2_gender).upper() == "M"):
            person1_reltype = 'WIFE'
            person2_reltype = 'HUSB'
        elif (str(person1_gender).upper() == "F") and (str(person2_gender).upper() == None):
            person1_reltype = 'WIFE'
            person2_reltype = 'HUSB'
        elif (str(person1_gender).upper() == "M") and (str(person2_gender).upper() == None):
            person1_reltype = 'HUSB'
            person2_reltype = 'WIFE'
        elif (str(person1_gender).upper() == None) and (str(person2_gender).upper() == "F"):
            person1_reltype = 'HUSB'
            person2_reltype = 'WIFE'
        elif (str(person1_gender).upper() == None) and (str(person2_gender).upper() == "M"):
            person1_reltype = 'WIFE'
            person2_reltype = 'HUSB'
        else:
            #If we don't have enough information, just make a guess as GEDCOM standard requires 1x HUSB and 1x WIFE record (even for same sex couples)
            person1_reltype = 'WIFE'
            person2_reltype = 'HUSB'        

        #Generate the GEDCOM FAM entries
        add_line(0,"@F{}@".format(idx),"FAM")
        add_line(1,person1_reltype,"@I{}@".format(person1))
        add_line(1,person2_reltype,"@I{}@".format(person2))
        add_line(1,"MARR")

        #Append the INDI records with FAMS attribute
        #TO DO ******************

def generate_children(individuals_in_group):
    #Get parental details for the individuals in the group
    scope = []
    for individual in individuals_in_group:
        scope.append(str(individual[0]))

    parent_data = get_spouses(config['PARENTS'],scope)

    #For each person, add them to the FAM record that exists for their mother/father. 
	#TO DO ******************
    
    #Create a new FAM for them if it doesn't exist
    #TO DO ******************
    
	#Append the INDI records with FAMC attribute
    #TO DO ******************