import psycopg2

from split_mp4 import split_to_list
import sys
import os
dir_name = sys.argv[1]
video_filename = None
grid_filename = None
for f in os.listdir(dir_name):
    if f.endswith(".TextGrid"):
        grid_filename = dir_name + "/" + f
    elif f.endswith(".mp4"):
        video_filename = dir_name + "/" + f
if not (video_filename and grid_filename):
    sys.exit()
print video_filename, grid_filename
root = "/Users/johannes/Documents/advanceret_database/segments/"
if len(sys.argv) > 2:
    root = sys.argv[2]
l = split_to_list(video_filename, grid_filename, root)


conn = None
try:
    conn = psycopg2.connect("dbname='postgres' user='johannes' host='localhost'")
    cur = conn.cursor()
    for query_list in l:
        print query_list
        cur.execute("INSERT INTO samples (seq_number, mark, start, stop, duration, relative_path) VALUES (%s, %s, %s, %s, %s, %s)", query_list)
    conn.commit()
    print "done"
except Exception, e:
    print "exception"
    print e
finally:
    if conn:
        conn.close()


