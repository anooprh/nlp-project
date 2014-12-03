label_map_file_name = '../exp-results/labels.map'
label_map_file = open(label_map_file_name)

label_map = {}

for line in label_map_file:
    file_split = line.strip().split(' ')
    label_map[file_split[0]] = file_split[1]
label_map_file.close()


def main():
    test_file_name = '../jrae/data-set/test-set'
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

            # if not label in label_map:
            #     continue

            for label_sec in labels:
                if label not in co_label_count:
                    co_label_count[label] = {}

                if label_sec in co_label_count[label]:
                    co_label_count[label][label_sec] += 1
                else:
                    co_label_count[label][label_sec] = 1

    for co_label in co_label_count:
        co_label_prob[co_label] = {}
        if co_label not in label_map:continue
        for label_sec in co_label_count[co_label]:
            co_label_prob[co_label][label_sec] = co_label_count[co_label][label_sec]*1.0 /label_count[co_label]
            out_file.write(label_sec+'\t'+co_label+'\t'+str(co_label_prob[co_label][label_sec])+'\n')

    test_file.close()
    out_file.close()

if __name__ == "__main__":
    main()