#2020-8-24
import redis,json
r = redis.Redis(host='dev.werror.com', port=4328, db=2,  decode_responses=True)

def restore(infile): 
	''' load file into db, 2020-8-23 '''
	for line in open(infile, 'r').readlines():
		arr = json.loads(line.strip())
		type =  arr['type'] 
		if type == 'hash': 
			r.hmset( arr['key'], arr['value'] ) 
		elif type == 'zset': 
			for k,v in arr['value'] : r.zadd(arr['key'], {k:v})
		elif type == 'string': 
			r.set( arr['key'], arr['value'] ) 
	print ("finished", infile)	

restore('4328-errant.json')