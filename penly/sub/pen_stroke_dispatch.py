# 21-5-24
import json,  redis, time, traceback, fire, os,sys
import numpy as np

r = redis.Redis(host="172.17.0.1", port=6379, db=0, decode_responses=True)
now	= lambda: time.strftime('%Y.%m.%d %H:%M:%S ',time.localtime(time.time()))
geox = lambda x, xmax=5600 : ( max(0, min(x, xmax)) - xmax/2)* 180 * 2 / xmax 
geoy = lambda y, ymax=7920 : ( max(0, min(y, ymax)) - ymax/2)* 85.05112878 * 2 / ymax 
xy_avg	= lambda rows: (round(np.average([int(row[0]) for row in rows]),1), round(np.average([int(row[1]) for row in rows]),1)) 
y_avg	= lambda rows: np.average([int(row[1]) for row in rows])
ifnone	= lambda x,defau = 0 : x if x else defau #hget	= lambda key, hkey, defau =0: ( res:= r.hget(key, hkey), res if res else defau )[1]
keyscore = lambda answer, item ='select-1', page='1713.536.33.63': (res:=r.hget(f"page:{page}:keyscore", f"{item}:{answer}"), float(res) if res else 0)[1]
in_region = lambda x,y, four: len(four) > 3 and x >= four[0] and x<= four[2] and y >= four[1] and y <= four[3] # x1,y1,x2,y2

row_height = r.hget('config:page_info', 'row_height')
row_height = float(row_height) if row_height else 280
print (f"row_height = {row_height}", flush=True)


ITEM_RATIO=10
def pen_stroke(msg):  # ap,page,pen,tm,stroke
	try:
		ap,page,pen,tm,stroke = msg['data'].strip().split(":")[0:5]
		r.publish('pen_stroke', f"{ap}:{page}:{pen}:{tm}:{stroke}")
		( r.zincrby(f"{ap}:pen_strokenum", 1, pen), r.zincrby(f"{ap}:page_strokenum", 1, page),r.zincrby(f"{ap}:{page}:pen_strokenum", 1, pen))

		llen = r.rpush(f"{ap}:{page}:{pen}", stroke) 	
		r.setex(f"penseg:{ap}:{page}:{pen}", 2, "") # added 2021.6.22
		x,y = xy_avg([ trp.split(",")  for trp in stroke.strip().split(" ")])
		r.geoadd(f"{ap}:{page}:geo_stroke", geox(x), geoy(y), f"{pen}:{llen-1}:{tm}") #stroke_id  tm_end is float

		rowitem = f"row:{int(y/row_height)}"  #f"row-{int(y/row_height)}"
		r.rpush(f"{ap}:{page}:{pen}:{rowitem}", stroke)
		r.setex(f"row_{ap}:{page}:{pen}:{rowitem}", 2, "") # row_ is processed by c# recog, discardable, for reference only 
		r.setex(f"zh_CN={ap}:{page}:{pen}:{rowitem}", 2, "") # for testing zh_CN

		line_key = r.hget(f"page:{page}:xy_to_line", f"{int(x/ITEM_RATIO)},{int(y/ITEM_RATIO)}") #10,24 => line-11:overcome_3, line is crossed
		if line_key : 
			r.rpush(f"{ap}:{page}:{pen}:{line_key}", stroke) 
			r.publish('pen_line_stroke', f"{ap}:{page}:{line_key}:{pen}:{tm}:{stroke}") 

		item_key = r.hget(f"page:{page}:xy_to_item", f"{int(x/ITEM_RATIO)},{int(y/ITEM_RATIO)}") #10,24 => select-1:A   x/100?
		r.zadd(f"{ap}:pen_tm",  {f"{pen}:{x}:{y}:{item_key if item_key else ''}" : float(tm)}) 
		if not item_key : return
		r.zadd(f"{ap}:item_tm", {item_key : float(tm)})


		ar = item_key.split(':')
		item = ar[0].strip()
		cate = item.split("-")[0] #select, number, cross, zh_CN
		r.rpush(f"{ap}:{page}:{pen}:{item}", stroke) 
		r.publish('pen_item_stroke', f"{ap}:{page}:{item_key}:{pen}:{tm}:{stroke}") # for playback 

		if ':' in item_key:  
			answer = ar[-1].strip()
			score  = keyscore(answer,item,page)
			r.publish('pen_score', json.dumps({'item':item,'score': score,'ap':ap, 'page':page, 'pen':pen,  'answer': answer,  'tm': float(tm)})) 
			r.publish(f'pen_score_{cate}', json.dumps({'item':item,'score': score,'ap':ap, 'page':page, 'pen':pen,  'answer': answer,  'tm': float(tm)})) 

			r.geoadd(f"{ap}:{page}:geo_pen_label", geox(x), geoy(y), json.dumps({'key':f"{ap}:{page}:{pen}:{item}", "label":answer, 'tm': float(tm)}))
			( r.hset(f"{ap}:{cate}:{item}", pen, answer) , r.hset(f"{ap}:{cate}:{pen}", item, answer) )

			r.hset(f"{ap}:pen:{cate}", f"{pen}:{item}", answer) 
			r.hset(f"{ap}:pen:{cate}:tm", f"{pen}:{item}:{tm}", answer) 
			r.zadd(f"{ap}:pen:{cate}:answer", {f"{pen}:{item}:{answer}": float(tm)} ) 

			( r.hsetnx(f"{ap}:score:{pen}",item,score) , r.hsetnx(f"{ap}:score:{item}",pen,score) )
		else:
			stream = 'zh_CN' if item.startswith("zh_CN") else 'en_US' #r.setex(f"{cate}={ap}:{page}:{pen}:{item}", 2, "") # zh_CN
			r.setex(f"{stream}={ap}:{page}:{pen}:{item}", 2, "") 
	except Exception as ex:
		print ( ">>pen_stroke ex:", ex, "\t", msg, flush=True) 

def pen_label(msg):
	try:
		arr = json.loads(msg['data']) 
		key,answer,llen, tm = arr.get('key',''), arr.get('label',''), arr.get('llen',0) ,arr.get('tm',0)
		ar = key.split(":")  #hjzx0511:1713.536.33.64:BP2-1A3-03I-H0:fill-33-1
		ap,page,pen =ar[0:3]
		item = ar[-1] # fill-33-1
		score = keyscore(answer.lower(),item,page) 
		r.publish('pen_score', json.dumps({'item':item, 'score': score, 'ap':ap, 'page':page, 'pen':pen,  'answer': answer, 'tm': float(tm)}))

		cate = item.split("-")[0] # fill
		r.hset(f"{ap}:label:{item}", pen, answer)  # for chart show
		r.hset(f"{ap}:label:{pen}", item, answer)  
		r.hsetnx(f"{ap}:score:{pen}",item,score) 
		r.hsetnx(f"{ap}:score:{item}",pen,score) 

		r.hset(f"{ap}:pen:{cate}", f"{pen}:{item}", answer) 
		r.hset(f"{ap}:pen:{cate}:tm", f"{pen}:{item}:{tm}", answer) # (pen,item,answer, score,tm) 
		r.zadd(f"{ap}:pen:{cate}:answer", {f"{pen}:{item}:{answer}": float(tm)} ) #:{answer}:{page}, if exsits :  AA:fill-1:niche
	except Exception as ex:
		print ( ">>pen_label ex:", ex, "\t", msg, flush=True) 
		exc_type, exc_value, exc_obj = sys.exc_info()
		traceback.print_tb(exc_obj)

def listen(): 
	print ('>>listen channels: pen_stroke, pen_label', r, now(), flush=True)
	ps = r.pubsub(ignore_subscribe_messages=True)  #https://pypi.org/project/redis/
	ps.subscribe(**{'pen_label':pen_label, 'pen_stroke_pre':pen_stroke}) # , '__keyevent@0__:expired': ttl_expired'__keyevent@0__:expired': ttl_expired,   , '__keyevent@0__:set':label_set
	thread = ps.run_in_thread(sleep_time=0.001)
	#thread.stop()

if __name__ == '__main__': 
	listen()
	#ttl_expired({'type': 'message', 'pattern': None, 'channel': '__keyevent@0__:expired', 'data': 'test=config:unittest:B'})
