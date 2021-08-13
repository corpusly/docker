
if ! nc -v -z localhost 3306;  
then  
# mysql 5.5
docker run --name=mysqleev --env='MYSQL_ROOT_PASSWORD=cikuutest!'  --volume=/home/cikuu/mysqleev:/var/lib/mysql -p 3306:3306 --restart=always --detach=true wrask/mysql:5.5 --max_allowed_packet=100M --max_connections=1000
fi

if ! nc -v -z localhost 6666;  
then  
# kvrocks 2.2
docker run -itd --restart=always --name kveev -p 6666:6666 -v /home/cikuu/kvrocks-eev-128m:/tmp/kvrocks wrask/kvrocks:2.0.2
fi

while ! nc -v -z localhost 3306 || ! nc -v -z localhost 6666;
do
	echo "wait for mysqleev and kvrocks";
	sleep 1;
done;

echo "mysqleev & kvrocks are ready!";
echo "start now";
 
# mq consumer , eev_to_server23
#docker run -itd --restart=always --name mqeev wrask/mqeev python mqeev.py eev_to_kv_my_23 --host 192.168.1.23
docker run -itd --restart=always --name mqeev -v $(pwd):/app wrask/mqeev python /app/mqeev.py eev_to_$(hostname)
