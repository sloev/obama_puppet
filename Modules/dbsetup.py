import psycopg2
DEC2FLOAT = psycopg2.extensions.new_type(
        psycopg2.extensions.DECIMAL.values,
        'DEC2FLOAT',
        lambda value, curs: float(value) if value is not None else None)
psycopg2.extensions.register_type(DEC2FLOAT)
conn = None

try:
    conn = psycopg2.connect("dbname='postgres' user='johannes' host='localhost'")
    cur = conn.cursor()
    #create config table
    cur.execute(""" CREATE TABLE 
                    config_store(key VARCHAR(30) CONSTRAINT key_pk PRIMARY KEY, 
                    value VARCHAR(30))
                    """)
    #create original content table

    #create samples table
    cur.execute(""" CREATE TABLE 
                    samples(index SERIAL PRIMARY KEY,
                    seq_number INTEGER,
                    mark VARCHAR(30),
                    start DECIMAL(8,4),
                    stop DECIMAL(8,4),
                    duration DECIMAL(8,4),
                    relative_path VARCHAR(65))
                    """)
    conn.commit()
    print "done"
except Exception, e:
    print "exception"
    print e
finally:
    if conn:
        conn.close()
