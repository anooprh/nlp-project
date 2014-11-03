#! /bin/bash
if [ $# -ne 4 ]; then
    echo "Usage: train-set tag-freq train-num output_dir"
    exit 1
fi
train_set=$1
tag_freq=$2
train_num=$3
output=$4
awk -F "\t" '{
    l = split($1, a, ",")
    for(i=2;i<=l;++i){
	d[a[i]]++
    }
}
END{
    for(i in d){
	print i, d[i]
    }
}' $train_set | sort -k2gr > tag-freq
head -n $tag_freq tag-freq  > tag-freq-${tag_freq}
rm -rf $output
mkdir $output
cat tag-freq-${tag_freq} | awk '{print $1}' | while read tag; do
r=$RANDOM								  
awk -v out=$output -v t=$tag -v m=$train_num -v r=$r '
BEGIN{
    count=0
    s = 0
    srand(r)
}
{
    l = split($1, a, ",")
    $1 = ""
    sub(/^ /, "", $0)
    for(i=2;i<=l;++i){
	if(a[i] == t){
	    if(count < m){
		d[count] = $0
	    }else{
		k = int(rand() * count)
		if(k < m){
		    d[k] = $0
		}
	    }
	    ++count
	}
    }
}
END{
    for(i in d){
	print d[i]
    }
}' $train_set > $output/${tag}.txt
done
