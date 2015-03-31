

s = []
with open("weekly2.new.txt") as f:
    for line in f.readlines():
        s.append(line)
delchars = ''.join(c for c in map(chr, range(256)) if not c.isalnum())

for index, l in enumerate(s):
    l = " ".join([i.translate(None, delchars) for i in l.split()])
    s[index] = l

s = " ".join(s.upper().split())
with open("weekly_processed.txt" , "w") as f:
        f.write(s)
