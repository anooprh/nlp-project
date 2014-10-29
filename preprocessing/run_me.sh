#!/bin/bash
declare -a topics=("academia" "android" "anime" "apple" "arduino" "askubuntu" "astronomy" "aviation" "avp" "beer" "bicycles" "biology" "bitcoin" "blender" "boardgames" "bricks" "chemistry" "chess" "chinese" "christianity" "codegolf" "codereview" "cogsci" "cooking" "crypto" "cs" "cstheory" "dba" "diy" "drupal" "dsp" "earthscience" "ebooks" "electronics" "ell" "english" "expatriates" "expressionengine" "fitness" "freelancing" "french" "gamedev" "gaming" "gardening" "genealogy" "german" "gis" "graphicdesign" "ham")


## now loop through the above array
for i in "${topics[@]}"
do
   echo "Processing $i questions"
   python prepare_input_helper.py -i ../data/stackexchange/"$i".stackexchange.com.7z  -o cleaned_data/"$i"_questions -w cleaned_data/"$i"_questions_with_id -t cleaned_data/"$i"_tags
done