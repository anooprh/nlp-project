#! /bin/bash
while read x; do
    r=$RANDOM
    cat tag-id/$x | awk -v m=100 -v r=$r '
	      BEGIN{
		  count = 0
		  s = 0
		  srand(r)
	      }
	      {
		  if(count < m){
		      d[count] = $1
		  }else{
		      k = int(rand() * count)
		      if(k < m)
			  d[k] = $1
		  }
		  ++count
	      }
	      END{
		  for(i in d){
		      print d[i]
		  }
	      }
	      ' > train-id/$x
done
