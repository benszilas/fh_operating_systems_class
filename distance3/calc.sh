#!/bin/bash
lockdir1="/tmp/.myscript.lock1.$USER"
lockdir2="/tmp/.myscript.lock2.$USER"
lockdir3="/tmp/.myscript.lock3.$USER"

mkdir "$lockdir3" 2> /dev/null
if mkdir "$lockdir1" 2> /dev/null
then
    rm -r "$lockdir1"
    echo $(($1 + 2))
    exit
elif mkdir "$lockdir2" 2> /dev/null
then
    echo $(($1 + 2))
    rm -r "$lockdir2"
    exit
else
    echo "Error"
    rm -r "$lockdir1"
    rm -r "$lockdir2"
    pkill calc.sh
    exit
fi
