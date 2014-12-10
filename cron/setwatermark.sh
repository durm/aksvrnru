#!/bin/bash

SWMLOG="/home/aksvrnru/domains/aksvrn.ru/public_html/media/swmlog.log"
PREVIEWDIR="/home/aksvrnru/domains/aksvrn.ru/public_html/media/previews"

cd $PREVIEWDIR

cmd=""

if [ -z $SWMLOG ]
    then 
        cmd=`find . -name "*.medium.*"`
    else
        cmd=`find . -name "*.medium.*" -newer $SWMLOG` 
fi 

touch $SWMLOG

for l in $cmd 
    echo $l
done
