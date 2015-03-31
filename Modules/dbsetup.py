import psycopg2
conn = None

try:
    conn = psycopg2.connect("dbname='postgres' user='johannes' host='localhost'")
    cur = conn.cursor()
    cur.execute("CREATE TABLE samples(Id INTEGER PRIMARY KEY, Name VARCHAR(20))")
    conn.commit()
    print "done"
except Exception, e:
    print "exception"
    print e
finally:
    if conn:
        conn.close()
