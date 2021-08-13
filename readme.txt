
21-2-9
docker run --restart=always --name mysftp -p 7083:22 -v /home/cikuu/ftp/tmp:/home/admin/upload --privileged=true -d atmoz/sftp admin:admintest:::upload


docker É¾³ý exited ¾µÏñ

docker rm  $(docker ps -a | grep Exited | awk '{print $1}')

docker run -p 18888:8888 -e GRANT_SUDO=yes --user root --net=host -v /home/pigaiwang/rtm/pigai_data:/home/jovyan/cikuu/pigai_data jupyter:spacy3

docker run -p 18888:8888 -e GRANT_SUDO=yes --user root --net=host -v /home/pigaiwang/cikuu:/home/jovyan/cikuu jupyter:spacy4

docker run -d -p 18080:8080 -v /raid/pigai_data/docker_data/tiddly:/var/lib/tiddlywiki --name mywiki nicolaw/tiddlywiki

docker run -d -v /raid/pigai_data/docker_data/vsftpd:/home/vsftpd -p 20:20 -p 21:21 -p 21100-21110:21100-21110 -e PASV_ADDRESS=127.0.0.1 -e PASV_MIN_PORT=21100 -e PASV_MAX_PORT=21110 -e FTP_PASS=cikuutest! --name vsftpd --restart=always fauria/vsftpd


 kill  $(ps avx | grep eev-snts-bf | awk '{print $1}')

 ====
 https://fastapi.tiangolo.com/deployment/docker/

 ===
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
