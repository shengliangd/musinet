#!/bin/sh
CUR_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
javac -cp *:"$CUR_DIR" $@
