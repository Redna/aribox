#!/bin/bash

scriptdir=`dirname "$BASH_SOURCE"`

cd $scriptdir

if [[ -f aribox.pid ]]; then
    kill -9 `cat aribox.pid`
    rm aribox.pid
    echo "Aribox stopped"
else 
    echo "Aribox not started"
fi
