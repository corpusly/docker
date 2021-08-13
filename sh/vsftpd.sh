
docker run -d -v /data1/ftp:/home/vsftpd \
-p 20:20 -p 30021:21 -p 21100-21110:21100-21110 \
-e FTP_USER=cikuu -e FTP_PASS=cikuutest! \
-e PASV_ADDRESS=127.0.0.1 -e PASV_MIN_PORT=21100 -e PASV_MAX_PORT=21110 \
--name vsftpd --restart=always fauria/vsftpd