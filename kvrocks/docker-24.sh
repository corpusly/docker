
# kvrocks 2.2
docker run -itd --restart=always --name kveev -p 6666:6666 -v /home/cikuu/kvrocks-eev-128m:/tmp/kvrocks wrask/kvrocks:2.0.2

# mysql
docker run --name=mysqleev --env='MYSQL_ROOT_PASSWORD=cikuutest!'  --volume=/home/cikuu/mysqleev:/var/lib/mysql -p 3306:3306 --restart=always --detach=true wrask/mysql:5.5 --max_allowed_packet=100M --max_connections=1000
 
# mq consumer 
docker run -itd --restart=always --name mqeev wrask/mqeev python mqeev.py eev_to_kv_my_24 --host 192.168.1.24
