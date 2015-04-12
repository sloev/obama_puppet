import psycopg2
DEC2FLOAT = psycopg2.extensions.new_type(
        psycopg2.extensions.DECIMAL.values,
        'DEC2FLOAT',
        lambda value, curs: float(value) if value is not None else None)
psycopg2.extensions.register_type(DEC2FLOAT)
conn = None

create_speech_function = "".join(open("create_speech_function.py").readlines())

try:
    conn = psycopg2.connect("dbname='postgres' user='johannes' host='localhost'")
    cur = conn.cursor()
    cur.execute("CREATE EXTENSION IF NOT EXISTS plpythonu")
    cur.execute(create_speech_function)

    #create config table
    cur.execute(""" CREATE TABLE IF NOT EXISTS
                    config_store(key VARCHAR(30) CONSTRAINT key_pk PRIMARY KEY,
                    value VARCHAR(100))
                    """)
    cur.execute("INSERT INTO config_store(key, value) VALUES(%s, %s)", ["root", "/Users/johannes/Documents/obama_puppet/segments"])
    #create original content table
    cur.execute(""" CREATE TABLE
                    raw_material(air_date DATE PRIMARY KEY,
                    text_relative_path VARCHAR(65),
                    video_relative_path VARCHAR(65))
                    """)
    #create dictionary table
    cur.execute(""" CREATE TABLE
                    dictionary(word VARCHAR(30) constraint word_pk PRIMARY KEY)
                    """)
    #create samples table
    cur.execute(""" CREATE TABLE
                    samples(index SERIAL PRIMARY KEY,
                    air_date DATE references raw_material(air_date),
                    seq_number INTEGER,
                    word VARCHAR(30) references dictionary(word),
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
