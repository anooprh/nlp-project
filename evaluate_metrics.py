#!/bin/python

# Anoop : Script to calculate precision and recall between two files
# Usage:
# Please ensure both pred_labels and test_labels are in same order 
# Example:
# test_data_labels.csv
#   docid1_hash,label1,label2,label3
#   docid2_hash,label1,label2,label3
#   docid3_hash,label1,label2,label3
#   ''''''''''''''''''''''''''''''''
# pred_data_labels.csv
#   docid1_hash,pred_label1,pred_label2,pred_label3
#   docid2_hash,pred_label1,pred_label2,pred_label3
#   docid3_hash,pred_label1,pred_label2,pred_label3
#   ''''''''''''''''''''''''''''''''''''''''''''''
import sys
from itertools import izip

if(len(sys.argv) != 3):
    print "Correct usage : python evaluate_metric.py predictions_file actuals_file"
    print "Example :  python evaluate_metric.py test_data_labels.csv test_data_labels.csv"
    sys.exit(1)
test_file_name = sys.argv[1]
pred_file_name = sys.argv[2]
    #test_file_name = "test_data_labels.csv"
    #pred_file_name = "predicted_labels.csv"

precision = [];
recall = [];

def size_of_common_elements(list1, list2):
    return len(set(list1).intersection(list2))

def average(list):
    return sum(list)/float(len(list))

for pred_line, test_line in izip(open(pred_file_name), open(test_file_name)):

    pred_splits = pred_line.strip().split(',')
    test_splits = test_line.strip().split(',')
    if(pred_splits[0] != test_splits[0]):
        print "Wrong ordering in input files\nDocId of two files must be in same order"
    pred_labels = pred_splits[1:]
    test_labels = test_splits[1:]
    size_pred_label = len(pred_labels)
    size_test_label = len(test_labels)
    size_intersection = size_of_common_elements(pred_labels, test_labels)

    precision.append(size_intersection*1.0 / size_pred_label*1.0 )
    recall.append(size_intersection*1.0 / size_test_label*1.0 )
    
average_precision = average(precision)
average_recall = average(recall)
print "Average precision : " + str(average_precision * 100) + " %"
print "Average recall    : " + str(average_recall * 100) + " %"
