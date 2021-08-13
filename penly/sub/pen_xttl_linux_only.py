# 21-5-24  __keyevent@0__:set
import json,  redis, time, os,sys, requests
now	= lambda: time.strftime('%Y.%m.%d %H:%M:%S ',time.localtime(time.time()))
r = redis.Redis(host="172.17.0.1", port=6379, db=0, decode_responses=True)

def ttl_expired(msg):  #en_US=testap:1713.537.31.86:BP2-1A3-03I-HG:collocation-15-2
	msg = msg['data']
	if '=' in msg: 
		idx = msg.find('=') # en_US={ap}:{page}:{pen}:{item}
		name = msg[0:idx]
		key = msg[idx+1:]
		r.xadd(name, {'key':key})  	#process(key)

def listen(): 
	print ('start to listen : __keyevent@0__:expired', r, now(), flush=True)
	ps = r.pubsub(ignore_subscribe_messages=True)  #https://pypi.org/project/redis/
	ps.subscribe(**{'__keyevent@0__:expired': ttl_expired})
	thread = ps.run_in_thread(sleep_time=0.001)
	#thread.stop()

if __name__ == '__main__': 
	listen()
	#ttl_expired({'type': 'message', 'pattern': None, 'channel': '__keyevent@0__:expired', 'data': 'test=config:unittest:B'})

'''
recog = lambda listkey,port=8461: requests.get(f"http://win1.penly.cn:{port}/",params={"listkey":listkey}).json()
def process(key):  #{ap}:{page}:{pen}:{item}
	try:
		print ("ttl key: ", key, flush=True)
		llen = r.llen(key) 
		bbox = recog(key)
		r.zadd( f"{key}:label8461", {bbox['label']:llen})
		r.hset( f"{key}:cands8461", llen, json.dumps(bbox['words'][0]['candidates']) )
		#r.publish("pen_label", json.dumps({'key':key, 'label': bbox['label'] , 'llen': llen}) )
	except Exception as ex:
		print ("recog 8461 exception:", ex, key)

	elif msg.startswith("penseg:"): #penseg:hjzx0511:1713.536.33.63:BP2-1A3-03I-HH
		try:
			key = msg[7:]
			lastkey = r.zrevrange(f"{key}:seg",0,0)
			r.zadd(f"{key}:seg", {r.llen(key): int(lastkey[0]) if lastkey else 0}) 
		except Exception as ex:
			print ("penseg: ex", ex)

'''