#!/bin/bash

[ ! -d ../pkl ] && mkdir ../pkl

cd xmlpkl

for fname in `ls ../../seq`
do
    name=`echo $fname|cut -d . -f 1`.pkl
    ./xml2pkl.py ../../seq/$fname ../../pkl/$name
done
