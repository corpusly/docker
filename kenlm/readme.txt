

ps@gpu24:~$ runlike kenlm
docker run --name=kenlm --hostname=7e00f895cf57 --mac-address=02:42:ac:11:00:03 --env=PATH=/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin --env=LANG=C.UTF-8 --env=GPG_KEY=0D96DF4D4110E5C43FBFB17F2D347EA6AA65421D --env=PYTHON_VERSION=3.7.6 --env=PYTHON_PIP_VERSION=20.0.2 --env=PYTHON_GET_PIP_URL=https://github.com/pypa/get-pip/raw/d59197a3c169cef378a22428a3fa99d33e080a5d/get-pip.py --env=PYTHON_GET_PIP_SHA256=421ac1d44c0cf9730a088e337867d974b91bdce4ea2636099275071878cc189e -p 7098:7098 --restart=always --detach=true cikuu_kenlm:7098 python -m cikuu.api.uvicorn.kenlm_api


--- add the supper large model  *.trie 

目标是想 计算出  discuss about the problem 中的 about 是多余的


ps@gpu24:~$ docker run -it --rm python:3.8-alpine3.10  /bin/sh
/ # apk add gcc
fetch http://dl-cdn.alpinelinux.org/alpine/v3.10/main/x86_64/APKINDEX.tar.gz
fetch http://dl-cdn.alpinelinux.org/alpine/v3.10/community/x86_64/APKINDEX.tar.gz
(1/10) Installing binutils (2.32-r0)
(2/10) Installing gmp (6.1.2-r1)
(3/10) Installing isl (0.18-r0)
(4/10) Installing libgomp (8.3.0-r0)
(5/10) Installing libatomic (8.3.0-r0)
(6/10) Installing libgcc (8.3.0-r0)
(7/10) Installing mpfr3 (3.1.5-r1)
(8/10) Installing mpc1 (1.1.0-r0)
(9/10) Installing libstdc++ (8.3.0-r0)
(10/10) Installing gcc (8.3.0-r0)
Executing busybox-1.30.1-r3.trigger
OK: 97 MiB in 44 packages
/ # apk add g++
(1/4) Upgrading musl (1.1.22-r3 -> 1.1.22-r4)
(2/4) Installing musl-dev (1.1.22-r4)
(3/4) Installing libc-dev (0.7.1-r0)
(4/4) Installing g++ (8.3.0-r0)
Executing busybox-1.30.1-r3.trigger
OK: 163 MiB in 47 packages
/ # pip install https://github.com/kpu/kenlm/archive/master.zip
Collecting https://github.com/kpu/kenlm/archive/master.zip
  Downloading https://github.com/kpu/kenlm/archive/master.zip
     / 540 kB 267 kB/s
Building wheels for collected packages: kenlm
  Building wheel for kenlm (setup.py) ... done
  Created wheel for kenlm: filename=kenlm-0.0.0-cp38-cp38-linux_x86_64.whl size=300567 sha256=d45c889f74566dc3793ac51d6e7a204d670bc7c8291334566e1bb0b95222204d
  Stored in directory: /tmp/pip-ephem-wheel-cache-vcf411y0/wheels/ff/08/4e/a3ddc0e786e0f3c1fcd2e7a82c4324c02fc3ae2638471406d2
Successfully built kenlm
Installing collected packages: kenlm
Successfully installed kenlm-0.0.0
WARNING: You are using pip version 20.1.1; however, version 21.0.1 is available.
You should consider upgrading via the '/usr/local/bin/python -m pip install --upgrade pip' command.



# 2021-2-11
FROM python:3.8-alpine3.10

LABEL maintainer="zy <zy@cikuu.com>"

RUN apk add --no-cache --virtual .build-deps gcc libc-dev make \
    && pip install --no-cache-dir uvicorn gunicorn \
    && pip install fastapi \
    && pip install https://github.com/kpu/kenlm/archive/master.zip \
    && mkdir /model \
    && wget http://ftp.werror.com:8021/tmp/nyt5.kenlm /model \
    && apk del .build-deps gcc libc-dev make

WORKDIR /
COPY kenlm.py /kenlm.py
EXPOSE 80
CMD python /kenlm.py



FROM python:3.7-slim AS BASE
ENV PYTHONUNBUFFERED 1
WORKDIR /usr/src/app/
RUN pip install --upgrade pip
RUN apt-get update
RUN apt-get install -y gcc



# 2021-2-11
FROM python:3.8-slim
LABEL maintainer="zy <zy@cikuu.com>"

RUN pip install --no-cache-dir uvicorn gunicorn \
    && pip install fastapi \
    && apt-get update \
    && apt-get install -y gcc \
    && pip install https://github.com/kpu/kenlm/archive/master.zip \
    && mkdir /model

WORKDIR /
COPY kenlm.py /kenlm.py
EXPOSE 80
CMD python /kenlm.py