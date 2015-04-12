
CREATE OR REPLACE FUNCTION create_speech(text text)
RETURNS text AS $$
a = "SELECT s.word, s.air_date, s.seq_number, s.start, s.stop, s.duration, s.relative_path FROM samples s JOIN ( VALUES"

c = ") AS ordered(word, sort_order) ON ordered.word = s.word ORDER BY ordered.sort_order"
b = text.split()
for index, _b in enumerate(b):
    _z = "(\'%s\',\'%d\')" %(_b, (index+1))
    if index < len(b)-1:
        _z += ","
    b[index] = _z
rows = plpy.execute(a+" ".join(b)+c)
root = plpy.execute("SELECT * from config_store where key=\'root\'")[0]['value']
from moviepy.editor import *
import os
import base64
import hashlib

m = hashlib.sha256()
filename = ""
last_word = None
last_duration = 0
lines = []
for row in rows:
    word = row['word']
    duration = row['duration']
    path = row['relative_path']
    m.update(word)
    path = root + "/" + path
    if word == last_word:
        if last_duration < duration:
            last_duration = duration
            #lines[-1] = path
            #lines[-1] = "file \'" + path + "\'\n"
            #videos[-1] = [VideoFileClip(path)]
    else:
        last_duration = 0
        lines += [path]
        #lines += ["file \'" + path + "\'\n"]
        #videos += [VideoFileClip(path)]

    last_word = word 
sha = m.digest()
filename = base64.b32encode(sha).strip("=")


videos = []
final_video = None
for f in lines:
    videos += [VideoFileClip(f)]
    if len(videos) > 10:
        if not final_video:
            final_video = concatenate(videos)
        else:
            final_video = concatenate([final_video] + videos)
        final_video.write_videofile("/tmp/obamatmp.mp4")
        while videos:
            v = videos.pop()
            del v
        videos = []
        final_video = VideoFileClip("/tmp/obamatmp.mp4")
mov_filename = root + "/speeches/" + filename + ".mp4"  
         
final_video = concatenate([final_video] + videos)
final_video.write_videofile(mov_filename)
while videos:
    v = videos.pop()
    del v
del final_video


txt_filename = root + "/speeches/" + filename + ".txt"  


#import subprocess
#subprocess.call(["/usr/local/bin/ffmpeg", "-f", "-i", txt_filename, "-c", "copy", mov_filename])    

#final_video.write_videofile(filename)
return mov_filename

$$ LANGUAGE plpythonu

