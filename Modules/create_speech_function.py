
CREATE OR REPLACE FUNCTION create_speech(text text)
RETURNS text AS $$

import os
import base64
import hashlib
import os.path


a = "SELECT s.word, s.air_date, s.seq_number, s.start, s.stop, s.duration, s.relative_path FROM samples s JOIN ( VALUES"

c = ") AS ordered(word, sort_order) ON ordered.word = s.word ORDER BY ordered.sort_order"
words = text.replace (" ", " SILENT_SPACE ").upper().split()
values = []
for index, _b in enumerate(words):
    _z = "(\'%s\',\'%d\')" %(_b, (index+1))
    if index < len(words)-1:
        _z += ","
    values += [_z]
rows = plpy.execute(a+" ".join(values)+c)
root = plpy.execute("SELECT * from config_store where key=\'root\'")[0]['value']
m = hashlib.sha256()
filename = ""
lines = []
target = words.pop(0)
for row in rows:
    if not words:
        break
    word = row['word']
    if not word == target:
        continue
    path = root + "/" + row['relative_path']
    m.update(word)
    lines += [path]
    target = words.pop(0)

sha = m.digest()
filename = base64.b32encode(sha).strip("=")

txt_filename = root + "/speeches/" + filename + ".txt"
mov_filename = root + "/speeches/" + filename + ".mp4"

if os.path.isfile(mov_filename):
    return mov_filename

with open(txt_filename, 'w') as f:
    for l in lines:
        f.write('file \'%s\'\n' % l)

import subprocess
try:
    subprocess.check_call(["/usr/local/bin/ffmpeg", "-f", "concat", "-i", txt_filename, "-c", "copy", mov_filename])
    return mov_filename
except subprocess.CalledProcessError, e:
    return "ERROR"

$$ LANGUAGE plpythonu

