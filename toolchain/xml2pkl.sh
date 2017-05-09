#!/bin/bash

ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"/..

[ ! -d $ROOT_DIR/pkl ] && mkdir $ROOT_DIR/pkl

for fname in `ls $ROOT_DIR/seq`
do
    name=`echo $fname|cut -d . -f 1`.pkl
    $ROOT_DIR/tool-chain/xmlpkl/xml2pkl.py $ROOT_DIR/seq/$fname $ROOT_DIR/pkl/$name
    echo $fname
done
