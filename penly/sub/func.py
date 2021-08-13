# 21-5-21 
import json,  redis, time, traceback, fire, os,sys,builtins
import numpy as np

builtins.r = redis.Redis(host="172.17.0.1", port=6379, db=0, decode_responses=True)
now	= lambda: time.strftime('%Y.%m.%d %H:%M:%S ',time.localtime(time.time()))
geox = lambda x, xmax=5600 : ( max(0, min(x, xmax)) - xmax/2)* 180 * 2 / xmax 
geoy = lambda y, ymax=7920 : ( max(0, min(y, ymax)) - ymax/2)* 85.05112878 * 2 / ymax 
xy_avg	= lambda rows: (round(np.average([int(row[0]) for row in rows]),1), round(np.average([int(row[1]) for row in rows]),1)) 
y_avg	= lambda rows: np.average([int(row[1]) for row in rows])
ifnone	= lambda x,defau = 0 : x if x else defau #hget	= lambda key, hkey, defau =0: ( res:= r.hget(key, hkey), res if res else defau )[1]
keyscore = lambda answer, item ='select-1', page='1713.536.33.63': (res:=r.hget(f"page:{page}:keyscore", f"{item}:{answer}"), float(res) if res else 0)[1]
in_region = lambda x,y, four: len(four) > 3 and x >= four[0] and x<= four[2] and y >= four[1] and y <= four[3] # x1,y1,x2,y2

def listen(channel): 
	ps = r.pubsub() 
	ps.subscribe(channel) 
	print (f"start to listen: {channel}, at {now()} | ", r, flush=True)
	for item in ps.listen(): 
		if item['type'] == 'message' and isinstance(item['data'], str): #print ('item:', item) # item: {'type': 'pmessage', 'pattern': 'pen:*', 'channel': 'pen:apdata', 'data': 'hello'}
			try:
				redis.process(item['data']) # must be set in advance
			except Exception as ex:
				print(f">>pubsub listen {channel} ex:", ex, item)
	print (f" *** {channel}* is quitted! ")

mapf = {}
def myexec(code, mapf):
	try:
		exec(code, mapf)
	except Exception as ex:
		print ("myexec ex", ex, "\t|", code)

def config_pubsub(channel): 
	ps = r.pubsub() 
	ps.subscribe(channel) 
	funcs = r.hkeys(f"config:pubsub:{channel}")
	[myexec(code, mapf) for name, code in r.hgetall(f"config:pubsub:{channel}").items() ]
	func_list = [mapf[f] for f in funcs if f in mapf]
	print (f"start to config_pubsub: {channel}, at {now()}\n", funcs, func_list, r, flush=True)
	for item in ps.listen(): 
		if item['type'] == 'message' and isinstance(item['data'], str): 
			for f in func_list:
				try:
					f(item['data'])
				except Exception as ex:
					print(f">>config_pubsub {channel} ex:", ex, item, f)
	print (f" *** {channel}* is quitted! ")


if __name__ == '__main__': 
	fire.Fire(config_pubsub) 
