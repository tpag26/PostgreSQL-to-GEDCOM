import psycopg2

connstring = initialize(dbconfig)

def initialize(dbconfig):
    cs = "dbname=" + dbconfig['NAME'] + " "
    cs += "user=" + dbconfig['USERNAME'] + " "
    cs += "password=" + dbconfig['PASSWORD'] + " "
    cs += "host=" + dbconfig['HOST'] + " "
    cs += "port=" + dbconfig['PORT']
    return cs

def test_connection():
    try:
        conn = psycopg2.connect(connstring)
        cur = conn.cursor()
        return true
    except:
        return false