#!/bin/bash

mkdir -p build_image/src/

find src/ \( -name "*.py" -or -name "*.html" -or -name "*.js" \) -exec cp -r --parents {} build_image/src/ \;

cp setup.py build_image/
cp docker/Dockerfile build_image/
cp LICENSE build_image/