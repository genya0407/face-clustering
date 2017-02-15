#!/bin/bash

zip -r /tmp/categorize_faces.zip ./categorize_faces/*
aws lambda update-function-code --function-name "categorize_faces" --zip-file "fileb:///tmp/categorize_faces.zip"
zip -r /tmp/movie-capture.zip ./movie-capture/*
aws lambda update-function-code --function-name "movie-capture" --zip-file "fileb:///tmp/movie-capture.zip"
