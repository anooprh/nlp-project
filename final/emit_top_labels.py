from itertools import izip
import operator


def main():
    N = 5
    match_count = 0
    temp_map = {}

    input_file_name = 'aggregate_out_onlytop200'
    # input_file_name = 'aggregate_out_onlytop200'
    input_file = open(input_file_name)

    out_file_name = 'top_'+str(N)+'_labels'
    # out_file_name = 'top_'+str(N)+'_labels_onlytop200'
    out_file = open(out_file_name, 'w')

    actual_tag_file_name = 'actual_tags'
    actual_tag_file = open(actual_tag_file_name, 'w')

    actual_input_file_name = '../jrae/data-set/test-set'
    actual_input_file = open(actual_input_file_name)

    NUM_LINES = 37935
    i = 1
    for line, line_from_train_file in izip(input_file, actual_input_file):
        labels = line.split(',')
        file_split = line_from_train_file.split('\t')
        splits = file_split[0].split(',')
        doc_id = splits[0]
        actual_tags = splits[1:]
        question_words = file_split[1].strip().split(' ')

        outfile_line = doc_id
        for label in labels:
            label = label.strip()
            if label == '':continue
            label_split = label.split(':')
            label_key = label_split[0].strip()
            label_prob = float(label_split[1].strip())
            temp_map[label_key] = label_prob

        sorted_x = sorted(temp_map.items(), key=operator.itemgetter(1), reverse=True)
        j = 0
        k=N
        pred_tags = []
        while(j < len(sorted_x)):
            if(sorted_x[j][0] in question_words):
                outfile_line+=','+sorted_x[j][0]
                pred_tags.append(sorted_x[j][0])
                k-=1
            if k == 0:
                break
            j+=1

        for pred_tag in pred_tags:
            if pred_tag in actual_tags:
                match_count +=1
        outfile_line = outfile_line+'\n'
        out_file.write(outfile_line)

        actual_tag_file_line = doc_id+','+','.join(actual_tags)+'\n'
        actual_tag_file.write(actual_tag_file_line)

        print("processed " + str(i) +" / "+str(NUM_LINES) + " documents")
        i = i + 1

    print match_count
    input_file.close()
    out_file.close()
    actual_input_file.close()
    actual_tag_file.close()

if __name__ == "__main__":
    main()
