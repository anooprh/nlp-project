#! /bin/bash
ls train-id | while read x; do
		  awk -v x=$x 'ARGIND == 1{d[$1 ":" ]} ARGIND >= 2{}' train-id/$x ../domain/*_with_id
	      done
