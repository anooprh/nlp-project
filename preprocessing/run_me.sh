#!/bin/bash
#declare -a topics=("academia" "android" "anime" "apple" "arduino" "askubuntu" "astronomy" "aviation" "avp" "beer" "bicycles" "biology" "bitcoin" "blender" "boardgames" "bricks" "chemistry" "chess" "chinese" "christianity" "codegolf" "codereview" "cogsci" "cooking" "crypto" "cs" "cstheory" "dba" "diy" "drupal" "dsp" "earthscience" "ebooks" "electronics" "ell" "english" "expatriates" "expressionengine" "fitness" "freelancing" "french" "gamedev" "gaming" "gardening" "genealogy" "german" "gis" "graphicdesign" "ham")
declare -a new_topics=("apple" "drupal" "english" "gaming" "gis")
#declare -a new_topics=("gis")


## now loop through the above array
for i in "${new_topics[@]}"
do
   echo "Processing $i questions"
   python prepare_input_helper.py -i /home/anoop/Workspace/10701-project-old/data/stackexchange/"$i".stackexchange.com.7z  -o cleaned_data/"$i"_questions -w cleaned_data/"$i"_questions_with_id -t cleaned_data/"$i"_tags -n cleaned_data/"$i"_new_requirements
done