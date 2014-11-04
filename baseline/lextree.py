#!/bin/python

'''
Helper python to get the data in correct format
Anoop
Preferred Usage :

python prepare_input_helper.py -i 7z_file -o questions_cleaned -w questions_cleaned_with_id -t tag_file
'''
import copy
from getopt import getopt
import json
import os
import re
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
import networkx as nx
import matplotlib.pyplot as plt

# Default File Names , if no arguments provided
# input_filename = "/home/anoop/Workspace/10701-project/data/stackexchange/apple.stackexchange.com.7z"
input_filename = None

temp_dir = "extracted"

opts, args = getopt(sys.argv[1:], 'i:o:w:t:')
for opt , arg in opts:
    if opt in ('-i'):
        input_filename = arg

input_filename = '/home/anoop/Workspace/10701-project/data/stackexchange/academia.stackexchange.com.7z'
feature_file_name = 'lextree_features_1.txt'
feature_file = open(feature_file_name, 'w')

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

def get_plain_word(complex_str):
    return complex_str.split('.')[0]

count = 0
for post in posts:
    features = {}
    table = {}
    table_with_set = {}
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
    words = [w for w in words if not w in stopset]
    # words = [(snowball.stem(w)).lower() for w in words]

    this_post_words = words
    nltk_pos_tag = nltk.pos_tag(words)
    nouns = []
    for pos in nltk_pos_tag:
        if 'NN'in pos[1]:
            nouns.append(pos[0])

    for noun in nouns:
        no_of_occurences = (nouns.count(noun) * 1.0) / len(nouns)
        first_occurence = (nouns.index(noun) * 1.0) / len(nouns)
        last_occurence = ((len(nouns) - nouns[::-1].index(noun) - 1) * 1.0) / len(nouns)
        wn_synsets = wn.synsets(noun, pos='n')
        features[noun] = {}
        features[noun]['no_of_occurences'] = no_of_occurences
        features[noun]['first_occurence'] = first_occurence
        features[noun]['last_occurence'] = last_occurence
        features[noun]['lexChainSpanScore'] = 0
        features[noun]['directLexChainSpanScore'] = 0
        features[noun]['lexChainScore'] = 0
        features[noun]['directLexChainScore'] = 0


        for wn_synset in wn_synsets:
            synset_lexname = wn_synset.lexname()
            if(not noun in wn_synset.name().encode('utf-8')):
                continue
            if not synset_lexname in table:
                table[synset_lexname] = set()
            add_flag = True
            for element in table[synset_lexname]:
                if noun in element:
                    add_flag = False
            if add_flag:
                table[synset_lexname].add(wn_synset.name())

    for key in table.keys():
        pairs  = set()
        table_row_set = table.get(key)
        for L in range(0, len(table_row_set)+1):
            for subset in itertools.combinations(table_row_set, 2):
                pairs.add(subset)
        # print key,  pairs
        table_with_set[key] = pairs

    score_table = {}
    graph_table = {}
    for key in table_with_set.keys():
        graph = nx.Graph()
        score_table[key] = []
        set_of_pairs = table_with_set[key]
        for pair in set_of_pairs:
            # Process each pair individually

            word0 = pair[0]
            word1 = pair[1]

            element0 = {}
            element0[get_plain_word(word0)] = 0
            score_table[key].append(element0)
            element1 = {}
            element1[get_plain_word(word1)] = 0
            score_table[key].append(element1)

            # Check if they are synonyms
            synonyms = False
            for syn in  wn.synsets(get_plain_word(word0)):
                if word1 in syn.name():
                    synonyms = True
            for syn in  wn.synsets(get_plain_word(word1)):
                if word0 in syn.name():
                    synonyms = True
            if synonyms:
                for word_dict in score_table[key]:
                    if get_plain_word(word0) in word_dict:
                        word_dict[get_plain_word(word0)] += 10
                    if get_plain_word(word1) in word_dict:
                        word_dict[get_plain_word(word1)] += 10

            # Check for hypernyms
            hypernyms = False
            lowest_common_hypernyms = wn.synset(word0).lowest_common_hypernyms(wn.synset(word1))
            for lch in lowest_common_hypernyms:
                if get_plain_word(lch.name()) == get_plain_word(word0) or get_plain_word(lch.name()) == get_plain_word(word1):
                    hypernyms = True
            if hypernyms:
                for word_dict in score_table[key]:
                    if get_plain_word(word0) in word_dict:
                        word_dict[get_plain_word(word0)] += 7
                    if get_plain_word(word1) in word_dict:
                        word_dict[get_plain_word(word1)] += 7

            # Check for Morphys
            morphys = False
            if (get_plain_word(word0) == wn.morphy(get_plain_word(word1))) or (get_plain_word(word1) == wn.morphy(get_plain_word(word0))):
                morphys = True
                for word_dict in score_table[key]:
                    if get_plain_word(word0) in word_dict:
                        word_dict[get_plain_word(word0)] += 2
                    if get_plain_word(word1) in word_dict:
                        word_dict[get_plain_word(word1)] += 2

                print pair

            if synonyms or hypernyms or morphys:
                graph.add_edge(get_plain_word(word0), get_plain_word(word1))
                # plt.figure()
                # nx.draw(graph)
                # plt.show()
        graph_table[key] = graph

        for key in graph_table.keys():
            graph = graph_table[key]
            nodes = graph.nodes()
            edges = graph.edges()
            if len(edges) > 0:
                pass
            for node in nodes:
                node_utf = node.encode('utf-8')
                if node_utf not in nouns:
                    continue
                pos1 = words.index(node_utf)
                direct_span_score = 0
                features[node_utf]['lexChainSpanScore'] = 0
                features[node_utf]['directLexChainSpanScore'] = 0
                for word_dict in score_table[key]:
                    if node_utf in word_dict:
                        features[node_utf]['lexChainScore'] = word_dict[node_utf] #Get initial score from score table
                        features[node_utf]['directLexChainScore'] = word_dict[node_utf]

                # Computing Direct Lex chain score of all nddes
                for edge in edges:
                    if node_utf in edge:
                        edge_node1 = edge[0].encode('utf-8')
                        edge_node2 = edge[1].encode('utf-8')
                        pos_of_this_word = -1
                        if edge_node1 in words:pos_of_this_word   = words.index(edge_node1)
                        if pos_of_this_word != -1:
                            possible_direct_span_score = abs(pos1 - pos_of_this_word)
                            if possible_direct_span_score > direct_span_score: direct_span_score = possible_direct_span_score

                        pos_of_this_word = -1
                        if edge_node2 in words:pos_of_this_word   = words.index(edge_node2)
                        if pos_of_this_word != -1:
                            possible_direct_span_score = abs(pos1 - pos_of_this_word)
                            if possible_direct_span_score > direct_span_score: direct_span_score = possible_direct_span_score
                        if edge_node1 == node_utf:
                            for word_dict in score_table[key]:
                                if edge_node1 in word_dict:
                                    features[node_utf]['directLexChainScore'] += word_dict[edge_node1]
                        if edge_node2 == node:
                            for word_dict in score_table[key]:
                                if edge_node2 in word_dict:
                                    features[node_utf]['directLexChainScore'] += word_dict[edge_node2]
                features[node_utf]['lexChainSpanScore'] = direct_span_score

                # Computing Lex chain score of all connected nddes
                successors = nx.dfs_successors(graph, node_utf)
                lex_chain_score = 0
                span_score = 0
                for successor in successors.keys():
                    if successor == node_utf: continue

                    pos_of_this_word = -1
                    if successor in words: pos_of_this_word = words.index(successor)
                    if pos_of_this_word != -1:
                        possible_span_score = abs(pos1 - pos_of_this_word)
                        if possible_span_score > direct_span_score: direct_span_score = possible_span_score

                    for word_dict in score_table[key]:
                        if successor in word_dict:
                            lex_chain_score += word_dict[successor]
                    for t_successor in successors[successor]:
                        if t_successor == node_utf: continue

                        pos_of_this_word = -1
                        if t_successor in words: pos_of_this_word = words.index(t_successor)
                        if pos_of_this_word != -1:
                            possible_span_score = abs(pos1 - pos_of_this_word)
                            if possible_span_score > direct_span_score: direct_span_score = possible_span_score

                        for word_dict in score_table[key]:
                            if t_successor in word_dict:
                                lex_chain_score += word_dict[t_successor]

                features[node_utf]['lexChainSpanScore'] = lex_chain_score


    tags = post.get('Tags')
    tags = tags.replace('><',',').replace('<','').replace('>','')
    tags = tags.split(',')

    features_for_print = copy.deepcopy(features)
    for noun in nouns:
        features_for_print[noun]['noun'] = noun
        if noun in tags:
            features_for_print[noun]['tag'] = 'True'
        else:
            features_for_print[noun]['tag'] = 'False'
        feature_file.write(features_for_print[noun]['noun'].encode('utf-8')+",")
        feature_file.write(str(features_for_print[noun]['no_of_occurences'])+",")
        feature_file.write(str(features_for_print[noun]['first_occurence'])+",")
        feature_file.write(str(features_for_print[noun]['last_occurence'])+",")
        feature_file.write(str(features_for_print[noun]['lexChainSpanScore'])+",")
        feature_file.write(str(features_for_print[noun]['lexChainScore'])+",")
        feature_file.write(str(features_for_print[noun]['directLexChainSpanScore'])+",")
        feature_file.write(str(features_for_print[noun]['directLexChainScore'])+",")
        feature_file.write(features_for_print[noun]['tag'])
        feature_file.write("\n")

feature_file.close()
print "Done . . "
subprocess.call(['rm', '-rf', temp_dir])