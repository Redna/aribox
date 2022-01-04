#!/bin/bash

scriptdir=`dirname "$BASH_SOURCE"`

cd $scriptdir

if [[ -f aribox.pid ]]; then
    echo "Aribox already started - trying to stop.."
    ./stop.sh 
fi

echo "Starting Aribox"
nohup python3 -u src/main.py > aribox.log &
echo $! > aribox.pid
