# redis stream consumer, 2021-6-18 | python xrecog.py en_US recog --http_port 8461
import fire, json, redis, socket, os, time, requests
r		= redis.Redis(host="172.17.0.1", port=6379, db=0, decode_responses=True)
now		= lambda: time.strftime('%Y.%m.%d %H:%M:%S',time.localtime(time.time()))
xyt		= lambda tups: { "x": [int(tup[0]) for tup in tups] ,  "y": [int(tup[1]) for tup in tups],  "t": [int(tup[-1]) for tup in tups]}
xyts	= lambda stroke: xyt([ s.split(',')  for s in stroke.split(' ')])
events	= lambda listkey: {"events": [xyts(s) for s in r.lrange(listkey, 0,-1)] }
recog	= lambda listkey, port=8461: requests.post(f"http://127.0.0.1:{port}/",data=json.dumps(events(listkey))).json()

def process(id,params, http_port, pid):  #{ap}:{page}:{pen}:{item}
	try:
		key = params['key']
		llen = r.llen(key) 
		bbox = recog(key, http_port)
		label = bbox['label']
		r.zadd( f"{key}:label", {label:llen})
		if len(bbox['words']) > 0:  
			r.hset( f"{key}:cands", llen, json.dumps(bbox['words'][0]['candidates']) )
		r.publish("pen_label", json.dumps({'key':key, 'label': label , 'llen': llen}) )
		r.publish(f"log_xrecog_{pid}",f"{id},{key}/{llen},{now()} -> {label}")
	except Exception as ex:
		print ("recog exception:", ex, key)

def consume(stream, group, http_port=8461, waitms=3600000):
	try:
		r.xgroup_create(stream, group,  mkstream=True)
	except Exception as e:
		print(e)

	pid = os.getpid()
	consumer_name = f'consumer_{socket.gethostname()}_{pid}'
	print(f"Started: {consumer_name}|{stream}|{group}\t{now()}| ", r, flush=True)
	while True:
		item = r.xreadgroup(group, consumer_name, {stream: '>'}, count=1, noack=True, block= waitms )
		try:
			if not item: break
			id,params = item[0][1][0]  #[['_new_snt', [('1583928357124-0', {'snt': 'hello worlds'})]]]
			process(id,params, http_port, pid)
		except Exception as e:
			print(">>[xconsumeEx]", e, "\t|", item, "\t|",  now())

	r.xgroup_delconsumer(stream, group, consumer_name)
	r.close()
	print ("Quitted:", consumer_name, "\t",now())

if __name__ == '__main__': 
	print (recog("test:overcome"), flush=True)
	fire.Fire(consume) 