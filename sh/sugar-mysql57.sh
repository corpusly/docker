#docker run --name sugar-mysql57 --volume=/home/cikuu/data/docker/data/mysql:/var/lib/mysql/data -p 3307:3306 -e MYSQL_ROOT_PASSWORD=cikuutest! -d sugar-mysql57:latest

docker run --name sugar-mysql57 --volume=/home/cikuu/data/docker/data/mysql:/var/lib/mysql -p 3307:3306 -e MYSQL_ROOT_PASSWORD=cikuutest! -d mysql:5.7.26

#docker run -it --link sugar-mysql:mysql --rm mysql:5.7 sh -c 'exec mysql -h"$MYSQL_PORT_3306_TCP_ADDR" -P"$MYSQL_PORT_3306_TCP_PORT" -uroot -p"$MYSQL_ENV_MYSQL_ROOT_PASSWORD"'
