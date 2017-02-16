#!/bin/bash

for func in categorize-faces movie-capture face-tags list-movies
do
    ./deploy.sh $func
done
