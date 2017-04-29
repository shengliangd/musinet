#!/bin/bash

ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"/..

[ ! -d $ROOT_DIR/seq ] && mkdir $ROOT_DIR/seq

for fname in `ls $ROOT_DIR/xml`
do
    name=`echo $fname|cut -d . -f 1`.xml
    $ROOT_DIR/tool-chain/xmlseq/xml2seq2.py $ROOT_DIR/xml/$fname $ROOT_DIR/seq/$name
    echo $fname
done
