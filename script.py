#!/bin/python

import re

filename = "data/stackexchange/travel.stackexchange.com/questions"

with open(filename, "r") as file:
    for line in file:
        question_match = re.search(r'Body=\"(.*?)\"', line)
        question_body = question_match.group(1)
        question_body = question_body.replace('&lt;p&gt;', '').replace('&lt;/p&gt;&#xA;', '')

        title_match = re.search(r'Title=\"(.*?)\"', line)
        title = title_match.group(1)
        
        tags_match = re.search(r'Tags=\"(.*?)\"', line)
        tags = tags_match.group(1)
        tags = tags.replace('&gt;&lt;', ',').replace('&lt;','').replace('&gt;','')
        tags = tags.split(',')
        print "\nTitle = %s \nQuestion = %s\nTags=%s"%(title, question_body, tags)
        
