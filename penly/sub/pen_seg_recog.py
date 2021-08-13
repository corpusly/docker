# 21-6-22
import json,  redis, time, os,sys, requests,json
import numpy as np
now		= lambda: time.strftime('%Y.%m.%d %H:%M:%S',time.localtime(time.time()))
r		= redis.Redis(host="172.17.0.1", port=6379, db=0, decode_responses=True)
xyt		= lambda tups: { "x": [int(tup[0]) for tup in tups] ,  "y": [int(tup[1]) for tup in tups],  "t": [int(tup[-1]) for tup in tups]}
xyts	= lambda stroke: xyt([ s.split(',')  for s in stroke.split(' ')])
events	= lambda listkey, ibeg=0, iend=-1: {"events": [xyts(s) for s in r.lrange(listkey, ibeg,iend)] }
recog	= lambda listkey, ibeg=0, iend=-1, port=8461: requests.post(f"http://127.0.0.1:{port}/",data=json.dumps(events(listkey,ibeg,iend))).json()
diagram	= lambda listkey, ibeg=0, iend=-1: requests.post(f"http://iink.penly.cn:8464/",data=json.dumps(events(listkey,ibeg,iend))).json()
x_avg	= lambda s : round(np.average([int(tup.split(',')[0]) for tup in s.strip().split() if tup]),1)
y_avg	= lambda s : round(np.average([int(tup.split(',')[1]) for tup in s.strip().split() if tup]),1)
x_avg_list = lambda lkey, ibeg=0, iend=-1: round(np.average([x_avg(s) for s in r.lrange(lkey, ibeg,iend)]),1)
y_avg_list = lambda lkey, ibeg=0, iend=-1: round(np.average([y_avg(s) for s in r.lrange(lkey, ibeg,iend)]),1)

def pen_stroke_seg(msg):  #{\"key\": \"hjzx0511:1713.536.33.63:BP2-1A3-03I-HF\", \"ibeg\": 109, \"iend\": 131, \"tm\": \"2021.06.22 20:21:17\"}
	try:
		arr = json.loads(msg['data']) #r.publish("pen_stroke_seg", json.dumps({"key":key, "ibeg":int(ibeg), "iend":iend, "tm": now()}))
		lkey, ibeg, iend = arr['key'], arr['ibeg'], arr['iend']

		xyft = [ pair.split(',') for s in r.lrange(lkey, ibeg,iend-1) for pair in s.split(" ") ]
		key = f"{lkey}:seg:{ibeg},{iend}"
		x = round(np.average([ int(x) for x,y,f,t in xyft if x]), 1)
		r.hsetnx(key, "x", x )
		y = round(np.average([ int(y) for x,y,f,t in xyft if y]), 1)
		r.hsetnx(key, "y", y )
		r.hsetnx(key, "t", xyft[-1][-1] )
		xmin = min([ int(x) for x,y,f,t in xyft if x])
		r.hsetnx(key, "xmin", xmin )
		ymin = min([ int(y) for x,y,f,t in xyft if y])
		r.hsetnx(key, "ymin", ymin )
		xmax = max([ int(x) for x,y,f,t in xyft if x])
		r.hsetnx(key, "xmax", xmax )
		ymax = max([ int(y) for x,y,f,t in xyft if y])
		r.hsetnx(key, "ymax", ymax )

		en = output_en_US(lkey, ibeg, iend)
		zh = output_zh_CN(lkey, ibeg, iend)
		output_diagram(lkey, ibeg, iend)
		print (arr)
		r.publish("pen_seg", json.dumps({'key':key, 'x': x , 'y': y, 't':xyft[-1][-1], 'xmin':xmin, 'ymin':ymin, 'xmax':xmax, 'ymax':ymax, 'en_US':en, 'zh_CN':zh}) )

	except Exception as ex:
		print ("pen_stroke_seg: ex", ex)

def output_en_US(lkey, ibeg, iend):
	try:
		bbox = recog(lkey, ibeg, iend -1)
		r.hsetnx(f"{lkey}:seg:{ibeg},{iend}", "en_US", bbox['label'])
		return bbox['label']
	except Exception as ex:
		print ("output_zh_CN: ex", ex, lkey,ibeg,iend)

def output_zh_CN(lkey, ibeg, iend):
	try:
		bbox = recog(lkey, ibeg, iend -1, 8465)
		r.hsetnx(f"{lkey}:seg:{ibeg},{iend}", "zh_CN", bbox['label'])
		return bbox['label']
	except Exception as ex:
		print ("output_zh_CN: ex", ex, lkey,ibeg,iend)

def output_diagram(lkey, ibeg, iend):
	try:
		if iend - ibeg > 1 : return 
		bbox = diagram(lkey, ibeg, iend -1)
		if len(bbox['elements']) < 1 : return 
		a = bbox['elements'][0]
		if a.get('kind','') == 'line' :
			x1,y1,x2,y2 = round(a['x1'],1),round(a['y1'],1),round(a['x2'],1),round(a['y2'],1)
			r.hsetnx(f"{lkey}:seg:{ibeg},{iend}", "line", f"[{x1},{y1},{x2},{y2}]")
			r.hsetnx(f"{lkey}:seg:{ibeg},{iend}", "line_pixel", f"[{round(x1*3.78/0.07967172,1)},{round(y1*3.78/0.07967172,1)},{round(x2*3.78/0.07967172,1)},{round(y2*3.78/0.07967172,1)}]")
			print ( "line hitted", bbox , flush=True) 
	except Exception as ex:
		print ("output_diagram: ex", ex, lkey,ibeg,iend)

def listen(): 
	print ('start to listen : pen_stroke_seg', r, now(), flush=True)
	ps = r.pubsub(ignore_subscribe_messages=True)  #https://pypi.org/project/redis/
	ps.subscribe(**{'pen_stroke_seg': pen_stroke_seg})
	thread = ps.run_in_thread(sleep_time=0.001)

if __name__ == '__main__': 
	listen()

'''
{
 "type": "Diagram",
 "bounding-box": {
  "x": 1.20948315,
  "y": 1.45466518,
  "width": 14.0657768,
  "height": 2.11882091
 },
 "elements": [ {
   "type": "Edge",
   "kind": "line",
   "connected": [  ],
   "ports": [  ],
   "id": 61,
   "bounding-box": {
    "x": 1.20948315,
    "y": 1.45466518,
    "width": 14.0657768,
    "height": 2.11882091
   },
   "items": [ {
     "type": "line",
     "timestamp": "2021-06-21 09:09:40.270000",
     "x1": 2.20948315,
     "y1": 2.57348609,
     "x2": 14.27526,
     "y2": 2.45466518,
     "startDecoration": "none",
     "endDecoration": "none",
     "id": "0000200001000300ff00"
    } ],
   "x1": 2.20948315,
   "y1": 2.57348609,
   "x2": 14.27526,
   "y2": 2.45466518
  } ],
 "version": "2",
 "id": "MainBlock"
}
'''
