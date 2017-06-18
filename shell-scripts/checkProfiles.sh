#!/bin/bash

for PROFILE in $(grep '^\[' ~/.aws/credentials | sed 's/\[\(.*\)\]/\1/g')
do 
    aws s3 ls --profile $PROFILE >/dev/null 2>/dev/null
    [ $? -ne 0 ] && RESULT="KO" || RESULT="OK"
    echo $PROFILE:$RESULT
done
