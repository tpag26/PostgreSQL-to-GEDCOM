from db import get_spouses, get_parents, get_individuals
from gedfile import add_line, append_record
from indi import add_individual_record

config = None
fam_map = []
fam_last_index = None

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
        
        #Resolve any referential integrity issues
        if str(config['OPTIONS']['ENFORCE_REFERENTIAL_INTEGRITY'].upper()) == 'TRUE':
            if str(person1) not in scope:
                add_individual_record(config,person1)
            if str(person2) not in scope:
                add_individual_record(config,person2)

        #Generate the GEDCOM FAM entries
        add_line(0,"@F{}@".format(idx),"FAM")
        add_line(1,person1_reltype,"@I{}@".format(person1))
        add_line(1,person2_reltype,"@I{}@".format(person2))
        add_line(1,"MARR","Y")

        #Append the INDI records with FAMS attribute if the INDI is in this family
        append_record("0 @I{}@ INDI".format(person1),1,"FAMS","@F{}@".format(idx))
        append_record("0 @I{}@ INDI".format(person2),1,"FAMS","@F{}@".format(idx))
      
        #Store the FAM mappings because we need it for generate_children
        global fam_map
        fam_map.append((idx,(person1,person2)))
        global fam_last_index
        fam_last_index = idx

def generate_children(individuals_in_group):
    #Get parent details for the individuals in the group
    scope = []
    for individual in individuals_in_group:
        scope.append(str(individual[0]))

    parent_data = get_parents(config['PARENTS'],scope)

    for individual in parent_data:
        #Find the FAM record for the parents.
        records = []
        fam_id = None

        if individual[1] and individual[2]:
            records = [fam for fam in fam_map if fam[1] == (individual[1],individual[2]) or fam[1] == (individual[2],individual[1])]
        
        if len(records)>0:
            fam_id = records[0][0]

        if fam_id:
            #Add them to the FAM record. 
            append_record("0 @F{}@ FAM".format(str(fam_id)),1,"CHIL","@I{}@".format(individual[0]))
        else:
            #Create a new FAM record for the child if one doesn't exist (as long as at least one parent is known)
            if individual[1] or individual[2]:
                global fam_last_index
                fam_id = fam_last_index+1
                fam_last_index=fam_id
                add_line(0,"@F{}@".format(fam_id),"FAM")
                if individual[1]:
                    add_line(1,"WIFE","@I{}@".format(individual[1]))
                if individual[2]:
                    add_line(1,"HUSB","@I{}@".format(individual[2]))
                add_line(1,"CHIL","@I{}@".format(individual[0]))

        if fam_id:
            #Append the INDI record with FAMC attribute
            append_record("0 @I{}@ INDI".format(individual[0]),1,"FAMC","@F{}@".format(str(fam_id)))
        
        #Resolve any referential integrity issues
        if str(config['OPTIONS']['ENFORCE_REFERENTIAL_INTEGRITY'].upper()) == 'TRUE':
            if individual[1] and (str(individual[1]) not in scope):
                add_individual_record(config,individual[1])
            if individual[2] and (str(individual[2]) not in scope):
                add_individual_record(config,individual[2])