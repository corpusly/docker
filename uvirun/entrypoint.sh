#!/bin/sh

if [[ $tarfile ]]; then
cd /
wget $tarfile -O tmp.tar.gz
tar zxvf tmp.tar.gz 
rm tmp.tar.gz 
fi

if [[ $pyfile ]]; then
cd /
wget $pyfile 
fi

if [[ $pymain ]]; then
cd /
wget $pymain -O /main.py
fi

if [[ $pip ]]; then
pip install $pip
fi

if [[ $wget ]]; then
wget $wget
fi

# This will exec the CMD from your Dockerfile, i.e. "npm start"
exec "$@"
