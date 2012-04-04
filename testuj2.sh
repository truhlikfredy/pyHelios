#!/bin/sh

while :
do
    pid=`pidof -x parser.py`
    kill -9 $pid
    sleep 6
#    echo pustam znova
#    ./parser.py &
#    sleep 1
    inotifywait parser.py
done
