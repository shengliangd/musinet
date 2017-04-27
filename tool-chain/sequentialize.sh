#!/bin/bash

[ ! -d ../seq ] && mkdir ../seq

cd xmlseq

for fname in `ls ../../xml`
do
    name=`echo $fname|cut -d . -f 1`.xml
    ./xml2seq.py ../../xml/$fname ../../seq/$name
    echo $fname
done
