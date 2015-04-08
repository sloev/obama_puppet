import psycopg2

from split_mp4 import split_to_list
from hash_helper import file_to_b32_hash
import shutil
import sys
import os
import time
from datetime import datetime

dir_name = sys.argv[1]
root = "/Users/johannes/Documents/obama_puppet/segments"
if len(sys.argv) > 2:
    root = sys.argv[2]

def hash_and_copy(filename, root):
    ending = os.path.splitext(filename)[1]
    hashf = file_to_b32_hash(filename)
    hashf = hashf[:2] + "/" + hashf[2:]+ending
    abshashf = os.path.join(root, hashf)
    if not os.path.exists(root + "/" + hashf[:2]):
        os.makedirs(root + "/" + hashf[:2])
    shutil.copy(filename, abshashf)
    print "[!] copied %s to %s\n" %(filename, abshashf)
    return (abshashf, hashf)

rel_video_path = None
video_path = None
rel_grid_path = None
grid_path = None

air_date = None

for f in os.listdir(dir_name):
    absf = os.path.abspath(dir_name + "/" + f)
    if f.endswith(".TextGrid"):
        grid_path, rel_grid_path = hash_and_copy(absf, root)
    elif f.endswith(".mp4"):
        air_date = datetime.fromtimestamp(time.mktime(time.strptime(f[:6], "%m%d%y")))
        video_path, rel_video_path = hash_and_copy(absf, root)
if not (grid_path and video_path):
    sys.exit()
print video_path, grid_path, air_date
l = split_to_list(video_path, grid_path, air_date, root)

conn = None
try:
    conn = psycopg2.connect("dbname='postgres' user='johannes' host='localhost'")
    cur = conn.cursor()
#    cur.execute("INSERT INTO raw_material(air_date, text_relative_path, video_relative_path) VALUES (%s, %s, %s)", [air_date, rel_grid_path, rel_video_path])
    for query_list in l:
        print query_list
        cur.execute("""INSERT INTO dictionary(word)
            SELECT %s
            WHERE NOT EXISTS (
            SELECT word FROM dictionary WHERE word = %s
            )""", [query_list[2], query_list[2]])
        cur.execute("INSERT INTO samples (air_date, seq_number, word, start, stop, duration, relative_path) VALUES (%s, %s, %s, %s, %s, %s, %s)", query_list)
    conn.commit()
    print "done"
except Exception, e:
    print "exception"
    print e
finally:
    if conn:
        conn.close()


