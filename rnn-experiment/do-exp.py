import argparse
import json
import sys
import cPickle
import rae
import numpy as np
def read_data(f):
    label = []
    data = []
    for i in f:
        jd = json.loads(i)
        data.append(jd['data'])
        #label.append(jd['label'])
    return data, label

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--model', help="the file of model", required = True,
                        type=str)
    parser.add_argument('-t', '--train', help="train the model",
                        action="store_true")
    parser.add_argument("-d", "--data", help="data set", required = True,
                        type=str)
    parser.add_argument('--hidden-size', help='hidel dimension',
                        type=int)
    parser.add_argument('--input-size', help='input dimension',
                        type=int)
    parser.add_argument('--error-threshold', help='error-threshold',
                        type=float)
    args = parser.parse_args()
    print args
    data, label = read_data(open(args.data, 'rb'))
    print type(data)
    if args.train:
        print "Train the model now"
        print "Save to ", args.model
        print "Use the data-set", args.data
        data = np.array([np.matrix(d, dtype='float64') for d in data])
        f = file(args.model, 'wb')
        cPickle.dump(rae.train_model(data, args.input_size, args.hidden_size, args.error_threshold))
        f.close()
    else:
        f = file(args.model, 'rb')
        model = cPickle.load(f)
        for doc in data:
            hidden, hidden1_reproduction, input_reproduction, unrolled = model(np.array(doc, dtype='float64'))
            print hidden
    
