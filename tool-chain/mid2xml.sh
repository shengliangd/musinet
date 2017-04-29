#!/bin/bash

ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"/..

[ ! -d $ROOT_DIR/xml/ ] && mkdir $ROOT_DIR/xml

for fname in `ls $ROOT_DIR/mid/`
do
    name=`echo $fname|cut -d . -f 1`.xml
    $ROOT_DIR/tool-chain/jmusic/process $ROOT_DIR/mid/$fname $ROOT_DIR/xml/$name
done
