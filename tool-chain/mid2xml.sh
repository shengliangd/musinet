#!/bin/bash

[ ! -d ../xml/ ] && mkdir ../xml

cd jmusic
for fname in `ls ../../mid/`
do
    name=`echo $fname|cut -d . -f 1`.xml
    ./process ../../mid/$fname ../../xml/$name
done
