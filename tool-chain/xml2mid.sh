#!/bin/bash

# I mean, mid sequentialized
[ ! -d ../mid_seq/ ] && mkdir ../mid_seq

cd jmusic
for fname in `ls ../../seq/`
do
    name=`echo $fname|cut -d . -f 1`.mid
    ./deprocess ../../seq/$fname ../../mid_seq/$name
done
