docker run --name eev -v /raid/pigai_data/docker_data/mysql_eev:/var/lib/mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=cikuutest! -d mysql:5.7.26
#mysql --port 3306 -uroot -pcikuutest! -h 172.17.0.1
