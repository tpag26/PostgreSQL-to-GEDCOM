ged_data = []

def initialize_file():
    global ged_data
    ged_data = []

def add_line(hierarchy,type,value=None):
    global ged_data
    if (value):
        ged_data.append(str(hierarchy) + ' ' + str(type) + ' ' + str(value))
    else:
        ged_data.append(str(hierarchy) + ' ' + str(type))

def append_record(parent,hierarchy,type,value=None):
    new_record = ""
    insert_before = None
    existing_key_index = None

    if (value):
        new_record = (str(hierarchy) + ' ' + str(type) + ' ' + str(value))
    else:
        new_record = (str(hierarchy) + ' ' + str(type))

    global ged_data
    try:
        existing_key_index = ged_data.index(parent)
    except:
        pass

    if existing_key_index:
        for i, elem in enumerate(ged_data[existing_key_index+1:]):
            if '0 @' in elem:
                insert_before = i+existing_key_index+1
                break
    
    if insert_before:
        ged_data.insert(insert_before,new_record)

def render_output():
    add_line(0,"TRLR")
    return "\n".join(ged_data)