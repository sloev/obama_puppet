import psycopg2
conn = None

try:
    conn = psycopg2.connect("dbname='postgres' user='johannes' host='localhost'")
    cur = conn.cursor()
    cur.execute("DROP TABLE samples")
    cur.execute("DROP TABLE raw_material")
    cur.execute("DROP TABLE DICTIONARY")
    cur.execute("DROP TABLE config_store")
    cur.execute("DROP TABLE users")
    cur.execute("DROP TABLE tweets")
    conn.commit()
    print "done"
except Exception, e:
    print "exception"
    print e
finally:
    if conn:
        conn.close()
