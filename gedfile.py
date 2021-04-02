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

def render_output():
    return "\n".join(ged_data)