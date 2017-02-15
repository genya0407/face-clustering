#!/bin/bash

for func in categorize_faces movie-capture face-tags
do
    ./deploy.sh $func
done
