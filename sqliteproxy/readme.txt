
docker run -d -p 7098:2048 -v /home/cikuu/model/kp:/data/ assafmo/sqliteproxy --readonly --db /data/dic.db


Docker
https://hub.docker.com/r/assafmo/sqliteproxy

docker run -d -p 2048:2048 -v /path/to/my/db/dir/:/data/ assafmo/sqliteproxy --db /data/my.db
docker run -d -p 2048:2048 -v /path/to/my/db/dir/:/data/ assafmo/sqliteproxy --readonly --db /data/my.db

https://github.com/assafmo/SQLiteProxy

curl 'http://localhost:7098' -d sql='select * from dic_kp limit 3' 
http://dev.werror.com:7098/?sql=select%20*%20from%20dic_kp%20limit%203

http://dev.werror.com:7098/?sql=select%20*%20from%20dic_kp%20where%20kp%20=%20%27von/open%20*%27
[{"kp":"von/open *","mf":1592.95,"type":"*","arr":"door:17.72,window:5.97,eye:5.88,mouth:5.51,fire:5.14,account:2.02,letter:2.02,bottle:1.65,gate:1.56,bag:1.47,book:1.38,box:1.29,can:1.10,way:1.10,drawer:1.10,floodgate:0.92,store:0.92,present:0.92,mail:0.92,lid:0.92,file:0.83,heart:0.83,shutter:0.73,mind:0.73,envelope:0.73,restaurant:0.64,office:0.64,wardrobe:0.64,shop:0.55,branch:0.55,trunk:0.55,packet:0.55,umbrella:0.55,wallet:0.55,curtain:0.46,folder:0.46,arm:0.46,parcel:0.46,possibility:0.46,valve:0.46,cupboard:0.37,investigation:0.37,channel:0.37,cage:0.37,jar:0.37,border:0.37,meeting:0.37,factory:0.37,fridge:0.37,proceeding:0.37,throttle:0.37,school:0.37,handbag:0.37,discussion:0.28,attachment:0.28,newspaper:0.28,countryside:0.28,safe:0.28,couple:0.28,debate:0.28,nursery:0.28,briefcase:0.28,business:0.28,notebook:0.28,package:0.28,post:0.28,show:0.28,suitcase:0.28,tin:0.28,wine:0.28,wound:0.28,negotiation:0.18,case:0.18,centre:0.18,batting:0.18,option:0.18,oven:0.18,pack:0.18,gallery:0.18,leg:0.18,paper:0.18,parachute:0.18,lock:0.18,plant:0.18,pore:0.18,locker:0.18,back:0.18,bar:0.18,program:0.18,inquiry:0.18,route:0.18,game:0.18,"}]