import psycopg2

from split_mp4 import split_to_list

conn = None

try:
    conn = psycopg2.connect("dbname='postgres' user='johannes' host='localhost'")
    cur = conn.cursor()
    print "done"
except Exception, e:
    print "exception"
    print e
finally:
    if conn:
        conn.close()

import sys

dir_name = sys.argv[1]
video_filename = dir_name + "/weekly.mp4"
grid_filename = dir_name + "/weekly.TextGrid"
root = "/Users/johannes/Documents/advanceret_database/segments/"
l = split_to_list(video_filename, grid_filename, root)
for a in l:
    print a["seq_number"]
