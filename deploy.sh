#!/bin/bash

for func in categorize_faces movie-capture face-tags
do
    cd $func
    zip -r /tmp/$func.zip ./* > /dev/null 2>&1
    cd ..
    aws lambda update-function-code --function-name "$func" --zip-file "fileb:///tmp/$func.zip"
done
