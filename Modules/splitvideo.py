import sys,os
import base64
import hashlib
import shutil
from textgrid import TextGrid
from moviepy.editor import *

if len(sys.argv)<3:
    sys.exit()

grid = os.path.abspath(sys.argv[1])
grid = TextGrid.fromFile(grid)
videofile = VideoFileClip(sys.argv[2])
tmpfile = "/tmp/tmp_obama.mp4"
anker = "/Users/johannes/Documents/advanceret_database/segments/"

grid=grid[len(grid)-1]
counter=0

def create_hash_from_file(filename):
    with open(filename, "rb") as f:
        m = hashlib.sha256()
        m.update(f.read())
        sha = m.digest()
        return base64.b32encode(sha)

print "files loaded"
for interval in grid: 
    intervalStr=str(interval)
    start,end,mark=intervalStr[intervalStr.find("(")+1:intervalStr.find(")")].split(',')
    print start,end,mark
    start = float(start)
    end = float(end)
    mark = mark.split()[0]
    if mark!='sil':
        if mark == 'sp':
            mark = 'SILENTSPACE'
        print "extracting :%s" %mark
        clip = videofile.subclip(start,end)

        clip.to_videofile(tmpfile)
        hash_string = create_hash_from_file(tmpfile).strip("=")
        dir1 = hash_string[:2]
        filename = hash_string[6:] + ".mp4"
        dirname = anker + dir1
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        shutil.move(tmpfile, dirname + "/" + filename)
        print "[**********]"
        print "length: %f", end-start
        print "sequence: %d", counter
        print "word: %s", mark
        print "dir 1: %s", dir1
        print "filename: %s", filename
        print "dirname: %s", dirname
        print "[**********]\n"
        counter += 1
    else:
        print mark

print "finnished"
