#!/bin/python

'''
Helper python to get the data in correct format
Anoop
Preferred Usage :

python prepare_input_helper.py -i 7z_file -o questions_cleaned -w questions_cleaned_with_id -t tag_file
'''
from getopt import getopt
import os
import re
import shutil
import string
from nltk import word_tokenize
from nltk.corpus import stopwords
import hashlib
from nltk import stem
import sys
import subprocess
import xml.etree.ElementTree as ET

# Default File Names , if no arguments provided
# input_filename = "/home/anoop/Workspace/10701-project/data/stackexchange/apple.stackexchange.com.7z"
input_filename = None

temp_dir = "extracted"
questions_out_file_name = "questions_cleaned"
questions_with_id_out_file_name = questions_out_file_name +"_with_id"
tag_file_name = "question_labels"
new_file_name = "required_file"

opts, args = getopt(sys.argv[1:], 'i:o:w:t:n')
for opt , arg in opts:
    if opt in ('-i'):
        input_filename = arg
    if opt in ('-o'):
        questions_out_file_name = arg
    if opt in ('-w'):
        questions_with_id_out_file_name = arg
    if opt in ('-t'):
        tag_file_name = arg
    if opt in ('-n'):
        new_file_name = arg


if input_filename is None:
    print "Input file not specified"
    print "Usage: python -i <stackexchange.file.gz> [-o questions_file][-w question_with_id][-t tagfile]"
    sys.exit(1)

if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)

my_path = os.path.dirname(os.path.realpath(__file__))
subprocess.call(['7z', 'e', input_filename,'-o'+my_path+'/'+temp_dir])

tag_file = open(tag_file_name, "w")
questions_only_file = open(questions_out_file_name, 'w')
print questions_out_file_name
questions_with_id_file = open(questions_with_id_out_file_name, 'w')
print new_file_name
new_file = open(questions_out_file_name+'modified','w')

stopset = set(stopwords.words('english'))
# snowball = stem.snowball.EnglishStemmer()

tree = ET.parse(temp_dir+'/Posts.xml')
root = tree.getroot()
posts = root.getchildren()
count = 0
for post in posts:
    required_line = ''
    if post.get('PostTypeId') != '1':  # It is not a question
        continue
    count += 1
    # if count > 100: #Debug line
    #     break
    question_body = post.get('Body')
    question_body = re.sub('<[^>]+>', '',question_body).strip()

    title = post.get('Title')
    title = re.sub('<[^>]+>', '',title).strip()

    # Replace everythin in text with white space except -
    for c in string.punctuation.replace('-','').replace('.',''):
        question_body = question_body.replace(c,'')
    words = word_tokenize(question_body)
    # Stemming and stop word removal
    words = [w for w in words if not w in stopset]
    # words = [(snowball.stem(w)).lower() for w in words]

    this_post_words = words

    for c in string.punctuation.replace('-','').replace('.',''):
        title = title.replace(c,"")
    words = word_tokenize(question_body)
    # Stemming and stop word removal
    # words = [w for w in words if not w in stopset]
    # words = [(snowball.stem(w)).lower() for w in words]
    # this_post_words  += words


    doc_hash = hashlib.sha256(title.encode('utf-8')+" "+question_body.encode('utf-8')).hexdigest()
    questions_only_file_line = ''
    questions_id_file_line = doc_hash+': '

    # required_line += doc_hash
    for word in this_post_words:
        questions_only_file_line += word.lower()+' '
        # questions_id_file_line += snowball.stem(word).lower()+' '

    tags = post.get('Tags')
    tags = tags.replace('><',',').replace('<','').replace('>','')
    tags = tags.split(',')

    tag_file_line = doc_hash
    for tag in tags:
        tag_file_line += ","+tag.lower()

    questions_only_file.write(questions_only_file_line.encode('utf-8')+'\n')
    questions_with_id_file.write(questions_id_file_line.encode('utf-8')+'\n')
    tag_file.write(tag_file_line+'\n')
    required_line+=tag_file_line+'\t'+questions_only_file_line.encode('utf-8')+'\n'
    new_file.write(required_line)
    # print count

tag_file.close()
questions_only_file.close()
questions_with_id_file.close()
new_file.close()
# shutil.rmtree(temp_dir)
print "Done . . "
subprocess.call(['rm', '-rf', temp_dir])
print "Questions at " + questions_out_file_name
print "Questions with id's at " + questions_with_id_out_file_name
print "Labels at " + tag_file_name