# 21-6-22
import json,  redis, time, os,sys, requests,json
now	= lambda: time.strftime('%Y.%m.%d %H:%M:%S',time.localtime(time.time()))
r = redis.Redis(host="172.17.0.1", port=6379, db=0, decode_responses=True)

def ttl_expired(msg):  
	msg = msg['data']
	if msg.startswith("penseg:"): #penseg:hjzx0511:1713.536.33.63:BP2-1A3-03I-HH
		try:
			key = msg[7:]
			iend = r.llen(key)
			ibeg = r.zscore(f"{key}:seg",iend)
			if ibeg is None: 
				lastkey = r.zrevrange(f"{key}:seg",0,0)
				ibeg = int(lastkey[0]) if lastkey else 0
			r.zadd(f"{key}:seg", {iend : int(ibeg) }) 
			r.publish("pen_stroke_seg", json.dumps({"key":key, "ibeg":int(ibeg), "iend":iend, "tm": now()}))
		except Exception as ex:
			print ("penseg: ex", ex)

def listen(): 
	print ('start to listen : __keyevent@0__:expired', r, now(), flush=True)
	ps = r.pubsub(ignore_subscribe_messages=True)  #https://pypi.org/project/redis/
	ps.subscribe(**{'__keyevent@0__:expired': ttl_expired})
	thread = ps.run_in_thread(sleep_time=0.001)

if __name__ == '__main__': 
	listen()
	#ttl_expired({'type': 'message', 'pattern': None, 'channel': '__keyevent@0__:expired', 'data': 'test=config:unittest:B'})