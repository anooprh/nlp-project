import hashlib
from itertools import izip
import numpy as np
import operator

__author__ = 'anoop'

data_location = '../preprocessing/cleaned_data/'


text_file_name = 'academia_questions'
tag_file_name = 'academia_tags'

NO_OF_TAGS_TO_CONSIDER = 5

text_file = open(data_location+text_file_name)
tag_file = open(data_location+tag_file_name)
tags_collection = []

all_posts_words = []
post_properties = []
idf = {}
hashes = []
num_of_posts = 0

for text_file_line, tag_file_line in izip(text_file, tag_file):
    num_of_posts += 1
    words = text_file_line.strip().split(' ')
    words = [word for word in words]
    all_posts_words.append(words)
    post_property = {}
    post_property['tf'] = {}

    for word in words:
        if word in post_property['tf']:
            post_property['tf'][word] = post_property['tf'][word] + 1
        else: post_property['tf'][word] = 1


    tags = tag_file_line.strip().split(',')
    tags = [tag.strip().decode('utf-8-sig').encode('utf-8') for tag in tags]
    hashes.append(tags[0])
    tags = tags[1:]
    # print(tags)

    post_properties.append(post_property)
    tags_collection.append(tags)

for post_number, post_words in enumerate(all_posts_words):
    for word in post_words:
        if not word in idf:
            idf[word] = set()
        idf[word].add(post_number)


for word in idf.keys():
    idf[word] = np.log(num_of_posts / len(idf[word]))
test_data_file_name = "test_data_labels.csv"
predicted_file_name = "predicted_labels.csv"

test_file = open(test_data_file_name, "w")
pred_file = open(predicted_file_name, "w")

for post_number, post_words in enumerate(all_posts_words):
    word_score = {}
    doc_hash = hashes[post_number]
    for word in post_words:
        word_score[word] = post_properties[post_number]['tf'][word] * idf[word]

    sorted_word_scores = sorted(word_score.items(), key=operator.itemgetter(1))[::-1]

    test_file_line = doc_hash
    tags = tags_collection[post_number]
    for tag in tags:
        test_file_line += ','+tag
    test_file.write(test_file_line+"\n")


    pred_file_line = doc_hash
    for i in range(NO_OF_TAGS_TO_CONSIDER):
        if  i < len(sorted_word_scores):
            print next(iter(sorted_word_scores[i])),
            pred_file_line += ","+next(iter(sorted_word_scores[i]))
    print("\n"+"*" * 160+"\n")
    pred_file.write(pred_file_line+"\n")