
import redis
r = redis.Redis(host='dev.werror.com', port=4328, decode_responses=True) # combined to one db only , __formula:default

for k,v in r.hgetall("errant:type").items(): 
	print('"' + k+ '":' + v +",")