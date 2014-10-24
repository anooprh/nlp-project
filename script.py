#!/bin/python

import re
import numpy as np
import operator
import hashlib

# Not checking this file in github because data/ folder is 20Gb.Working on travel.stackexchange.com for now

filename = "questions"
NO_OF_TAGS_TO_CONSIDER = 5

num_of_posts = 0
post_properties = []
all_posts_words = []
idf = {}

questions = []
titles = []
tags_collection = []

test_data_file_name = "test_data_labels.csv"
predicted_file_name = "predicted_labels.csv" 

test_file = open(test_data_file_name, "w")
pred_file = open(predicted_file_name, "w")

with open(filename, "r") as file:
    # Each line is actually a question post in stackexchange
    for line in file:
        num_of_posts = num_of_posts + 1
        post_property = {}
        post_property['tf'] = {}
        post_property['idf'] = {} # Reduntant . . not needed

        question_match = re.search(r'Body=\"(.*?)\"', line)
        question_body = question_match.group(1)
        question_body = question_body.replace('&lt;p&gt;', '').replace('&lt;/p&gt;&#xA;', '')

        title_match = re.search(r'Title=\"(.*?)\"', line)
        title = title_match.group(1)

        words = question_body.split(" ")

        this_post_words = words

        for word in words:
            if word in post_property['tf']:
                post_property['tf'][word] = post_property['tf'][word] + 1
            else: post_property['tf'][word] = 1

        words = title.split(" ")
        this_post_words  += words

        for word in words:
            if word in post_property['tf']:
                post_property['tf'][word] = post_property['tf'][word] + 1
            else: post_property['tf'][word] = 1

        all_posts_words.append(this_post_words)

        tags_match = re.search(r'Tags=\"(.*?)\"', line)
        tags = tags_match.group(1)
        tags = tags.replace('&gt;&lt;', ',').replace('&lt;','').replace('&gt;','')
        tags = tags.split(',')

        post_properties.append(post_property)

        questions.append(question_body)
        titles.append(title)
        tags_collection.append(tags)
        # print "\nTitle = %s \nQuestion = %s\nTags=%s"%(title, question_body, tags)

for post_number, post_words in enumerate(all_posts_words):
    for word in post_words:
        if not word in idf:
            idf[word] = set()
        idf[word].add(post_number)

for word in idf.keys():
    idf[word] = np.log(num_of_posts / len(idf[word]))

for post_number, post_words in enumerate(all_posts_words):
    word_score = {}
    for word in post_words:
        word_score[word] = post_properties[post_number]['tf'][word] * idf[word]

    sorted_word_scores = sorted(word_score.items(), key=operator.itemgetter(1))[::-1]
    
    #print titles[post_number]+" "+questions[post_number]
    doc_hash = hashlib.sha256(titles[post_number]+" "+questions[post_number]).hexdigest()

    test_file_line = doc_hash
    tags = tags_collection[post_number]
    for tag in tags:
        test_file_line += ","+tag
    test_file.write(test_file_line+"\n")


    #print "Title: %s"%titles[post_number]
    #print "Question: %s"%questions[post_number]
    #print "Actual Tags: %s"%tags_collection[post_number]
    
    pred_file_line = doc_hash
    #print "Predicted Top %d tags with scores :"%NO_OF_TAGS_TO_CONSIDER
    for i in range(NO_OF_TAGS_TO_CONSIDER):
        pred_file_line += ","+next(iter(sorted_word_scores[i]))
        #print next(iter(sorted_word_scores[i]))
    #print("\n"+"*" * 160+"\n")
    pred_file.write(pred_file_line+"\n")

pred_file.close()
test_file.close()
pass

tag_set = set()
for tag_words in tags_collection:
    for tag in tag_words:
        tag_set.add(tag)
print len(tag_set)
print len(tags_collection)
