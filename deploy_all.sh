#!/bin/bash

for func in categorize-faces movie-capture face-tags
do
    ./deploy.sh $func
done
