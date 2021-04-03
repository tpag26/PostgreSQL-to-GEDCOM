import psycopg2

connstring = ""

def initialize_database(dbconfig):
    cs = "dbname=" + dbconfig['NAME'] + " "
    cs += "user=" + dbconfig['USERNAME'] + " "
    cs += "password=" + dbconfig['PASSWORD'] + " "
    cs += "host=" + dbconfig['HOST'] + " "
    cs += "port=" + dbconfig['PORT']
    global connstring
    connstring = cs

def test_connection():
    try:
        conn = psycopg2.connect(connstring)
        cur = conn.cursor()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        return str(e)

def get_individuals(config,group=None):
    conn = psycopg2.connect(connstring)
    cur = conn.cursor()
    if group:
        cur.execute(("SELECT {} FROM {} WHERE {}='{}';").format(
            config['ID_COLUMN']+','+config['FIRSTNAME_COLUMN']+','+config['LASTNAME_COLUMN']+','+config['SEX_COLUMN']+','+config['BIRTHDATE_COLUMN']+','+config['DEATHDATE_COLUMN'],
            config['TABLE_NAME'],
            config['GROUP_COLUMN'],
            group))
    else:
        cur.execute(("SELECT {} FROM {};").format(
            config['ID_COLUMN']+','+config['FIRSTNAME_COLUMN']+','+config['LASTNAME_COLUMN']+','+config['SEX_COLUMN']+','+config['BIRTHDATE_COLUMN']+','+config['DEATHDATE_COLUMN'],
            config['TABLE_NAME']))
    individuals = cur.fetchall()
    cur.close()
    conn.close()
    return individuals

def get_individual(config,individual_id):
    conn = psycopg2.connect(connstring)
    cur = conn.cursor()
    cur.execute(("SELECT {} FROM {} WHERE {}={};").format(
        config['ID_COLUMN']+','+config['FIRSTNAME_COLUMN']+','+config['LASTNAME_COLUMN']+','+config['SEX_COLUMN']+','+config['BIRTHDATE_COLUMN']+','+config['DEATHDATE_COLUMN'],
        config['TABLE_NAME'],
        config['ID_COLUMN'],
        individual_id))
    individual = cur.fetchone()
    cur.close()
    conn.close()
    return individual

def get_spouses(config,individuals):
    conn = psycopg2.connect(connstring)
    cur = conn.cursor()
    cur.execute(("SELECT {} FROM {} WHERE ({} IN ({})) OR ({} IN ({}));").format(
        config['INDIVIDUAL1_COLUMN']+','+config['INDIVIDUAL2_COLUMN'],
        config['TABLE_NAME'],
        config['INDIVIDUAL1_COLUMN'],
        ','.join(individuals),
        config['INDIVIDUAL2_COLUMN'],
        ','.join(individuals)))
    spouses = cur.fetchall()
    cur.close()
    conn.close()
    return spouses

def get_parents(config,individuals):
    conn = psycopg2.connect(connstring)
    cur = conn.cursor()
    cur.execute(("SELECT {} FROM {} WHERE {} IN ({});").format(
        config['INDIVIDUALID_COLUMN']+','+config['MOTHERID_COLUMN']+','+config['FATHERID_COLUMN'],
        config['TABLE_NAME'],
        config['INDIVIDUALID_COLUMN'],
        ','.join(individuals)))
    parents = cur.fetchall()
    cur.close()
    conn.close()
    return parents