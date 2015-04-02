
def normalize(filename):
    s = []
    with open(filename) as f:
        for line in f.readlines():
            s.append(line)
    delchars = ''.join(c for c in map(chr, range(256)) if not c.isalnum())
    ns = ""
    for index, l in enumerate(s):
        l = " ".join([i.translate(None, delchars) for i in l.split()])
        ns += " " + l

    ns = " ".join(ns.upper().split())
    with open(filename, "w") as f:
        f.write(ns)

if __name__ == "__main__" :
    import sys,os
    filename = os.path.abspath(sys.argv[1])
    print normalize(filename)
