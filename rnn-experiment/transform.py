import sys
import json
data = sys.argv[1]
vec_data = sys.argv[2]
vec = {}
for l in open(vec_data):
    word, v = l.split(' ', 1)
    dv = [float(x) for x in v.strip().split(' ')]
    vec[word] = dv
for doc in open(data):
    darr = []
    for d in doc.split():
        if d in vec:
            darr.append(vec[d])
    x = {'data': darr}
    s = json.dumps(x)
    print s
