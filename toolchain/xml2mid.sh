#!/bin/bash

ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"/..

# I mean, mid sequentialized
[ ! -d $ROOT_DIR/mid_seq/ ] && mkdir $ROOT_DIR/mid_seq

for fname in `ls $ROOT_DIR/seq/`
do
    name=`echo $fname|cut -d . -f 1`.mid
    $ROOT_DIR/tool-chain/jmusic/deprocess $ROOT_DIR/seq/$fname $ROOT_DIR/mid_seq/$name
done
