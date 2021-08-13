#!/bin/sh

if [[ $tarfile ]]; then
cd /
wget $tarfile -O tmp.tar.gz
tar zxvf tmp.tar.gz 
rm tmp.tar.gz 
fi

if [[ $svnup ]]; then
cd /home/cikuu/app
svn up $svnup --username zhangyue --password zhangy1235
fi

if [[ $pip ]]; then
pip install $pip
fi

if [[ $wget ]]; then
wget $wget
fi

# This will exec the CMD from your Dockerfile, i.e. "npm start"
exec "$@"
