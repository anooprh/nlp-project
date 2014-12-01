
def main():
    test_file_name = '../jrae/data-set/train-set'
    test_file = open(test_file_name)
    out_file_name = 'conditional_prob'
    out_file = open(out_file_name, 'w')

    label_count = {}
    co_label_count = {}
    co_label_prob = {}
    for line in test_file:
        labels = line.split('\t')[0].split(',')[1:]
        for label in labels:
            if label in label_count:
                label_count[label] += 1
            else:
                label_count[label] = 1
            for label_sec in labels:
                key = [label,label_sec]
                key.sort()
                key = "\t".join(key)
                if key in co_label_count:
                    co_label_count[key] += 1
                else:
                    co_label_count[key] = 1

    for co_label in co_label_count:
        count = co_label_count[co_label]
        splits = co_label.split('\t')
        split0 = splits[0]
        split1 = splits[1]

        co_label_prob[co_label] = (count*1.0)/label_count[split0]
        text = co_label+'\t'+str(co_label_prob[co_label])+'\n'
        out_file.write(text)

    test_file.close()
    out_file.close()

if __name__ == "__main__":
    main()