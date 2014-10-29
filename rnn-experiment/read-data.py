import json
import sys
def read_data(f):
    label = []
    data = []
    for i in f:
        jd = json.loads(i)
        data.append(jd['data'])
        label.append(jd['label'])
    return data, label
if __name__ == '__main__':
    read_data(sys.stdin)
