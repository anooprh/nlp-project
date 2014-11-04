#!/bin/python

from getopt import getopt
import os
import re
import shutil
import string
import itertools
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
import hashlib
from nltk import stem
import sys
import subprocess
import xml.etree.ElementTree as ET
from nltk.corpus import wordnet as wn

# Default File Names , if no arguments provided
# input_filename = "/home/anoop/Workspace/10701-project/data/stackexchange/apple.stackexchange.com.7z"
input_filename = None

temp_dir = "extracted"

opts, args = getopt(sys.argv[1:], 'i:o:w:t:')
for opt , arg in opts:
    if opt in ('-i'):
        input_filename = arg

input_filename = '/home/anoop/Workspace/10701-project/data/stackexchange/academia.stackexchange.com.7z'

if input_filename is None:
    print "Input file not specified"
    print "Usage: python -i <stackexchange.file.gz>"
    sys.exit(1)

if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)

my_path = os.path.dirname(os.path.realpath(__file__))
subprocess.call(['7z', 'e', input_filename,'-o'+my_path+'/'+temp_dir])

stopset = set(stopwords.words('english'))
snowball = stem.snowball.EnglishStemmer()

tree = ET.parse(temp_dir+'/Posts.xml')
root = tree.getroot()
posts = root.getchildren()

count = 0
for post in posts:
    features = {}
    table = {}
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
    for c in string.punctuation.replace('-',''):
        question_body = question_body.replace(c,'')
    words = word_tokenize(question_body)
    # Stemming and stop word removal
    # words = [w for w in words if not w in stopset]
    # words = [(snowball.stem(w)).lower() for w in words]

    this_post_words = words
    nltk_pos_tag = nltk.pos_tag(words)
    nouns = []
    for pos in nltk_pos_tag:
        if 'NN'in pos[1]:
            nouns.append(pos[0])

    for noun in nouns:
        no_of_occurences = (words.count(noun) * 1.0) / len(words)
        first_occurence = (words.index(noun) * 1.0) / len(words)
        last_occurence = ((len(words) - words[::-1].index(noun) - 1) * 1.0) / len(words)

        wn_synsets = wn.synsets(noun, pos='n')

        features[noun] = {}
        features[noun]['no_of_occurences'] = no_of_occurences
        features[noun]['first_occurence'] = first_occurence
        features[noun]['last_occurence'] = last_occurence
        features[noun]['score'] = 0

        for wn_synset in wn_synsets:
            synset_lexname = wn_synset.lexname()
            if(not noun in wn_synset.name().encode('utf-8')):
                continue
            if not synset_lexname in table:
                table[synset_lexname] = set()
            table[synset_lexname].add(wn_synset.name())

    for key in table.keys():
        pairs  = set()
        table_row_set = table.get(key)
        for L in range(0, len(table_row_set)+1):
            for subset in itertools.combinations(table_row_set, 2):
                pairs.add(subset)
        print key,  pairs

        for pair in pairs:
            # Finding if two words are hypernyms
            word0 = pair[0].encode('utf-8').split('.')[0]
            word1 = pair[1].encode('utf-8').split('.')[0]
            if (not word0 in features) or (not word1 in features): continue

            if not 'hypernym' in features[word0] : features[word0]['hypernym'] = 0
            if not 'hypernym' in features[word1] : features[word1]['hypernym'] = 0
            if wn.synset(pair[0]).lowest_common_hypernyms(wn.synset(pair[0])) in pair:
                features[word0]['hypernym'] += 7 # Weight 7 for hypernyms
                features[word1]['hypernym'] += 7 # Weight 7 for hypernyms

            #Finding if two words are synonnyms
            if not 'synonym' in features[word0] : features[word0]['synonym'] = 0
            if not 'synonym' in features[word1] : features[word1]['synonym'] = 0
            if (wn.synset(pair[0]) in wn.synsets(word1)) or (wn.synset(pair[1]) in wn.synsets(word0)):
                features[word0]['synonym'] += 10 # Weight 10 for synonyms
                features[word1]['synonym'] += 10 # Weight 10 for synonyms

            # Finding morphemes
            if not 'morphemes' in features[word0] : features[word0]['morphemes'] = 0
            if not 'morphemes' in features[word1] : features[word1]['morphemes'] = 0
            if (word0 == wn.morphy(word1)) or (word1 == wn.morphy(word0)):
                features[word0]['morphemes'] += 2 # Weight 2 for 'morphemes'
                features[word1]['morphemes'] += 2 # Weight 2 for 'morphemes'


    tags = post.get('Tags')
    tags = tags.replace('><',',').replace('<','').replace('>','')
    tags = tags.split(',')


print "Done . . "
subprocess.call(['rm', '-rf', temp_dir])