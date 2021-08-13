# 21-5-24  __keyevent@0__:set
import json,  redis, time, os,sys, bisect
now	= lambda: time.strftime('%Y.%m.%d %H:%M:%S ',time.localtime(time.time()))
r = redis.Redis(host="172.17.0.1", port=6379, db=0, decode_responses=True)

def pen_line_stroke(msg):  #f"{ap}:{page}:{line_key}:{pen}:{tm}:{stroke}") 
	ap,page,line_key,pen,tm,stroke = msg.split(':')
	xarr = [int(s.split(',')[0]) for s in stroke.split(' ')]
	xmin = min(xarr)
	xmax = max(xarr)
	words = r.lrange(f"page:{page}:{line_key}",0,-1)
	list = [ int(w.split(':')[0]) for w in words]
	ibeg =  bisect.bisect(list, xmin)
	iend =  bisect.bisect(list, xmax) #['1000:use', '1200:of', '1450:the', '1650:book']
	print (ap, line_key, pen, words[ibeg:iend])
	answer = ' '.join(w.split(':')[-1] for w in words[ibeg:iend])
	r.publish("pen_line_storke_hitted", json.dumps({'ap':ap, 'page':page, 'pen':pen, 'line_key':line_key, 'tm':tm, 'answer': answer}) )

	r.hset(f"{ap}:pen:{line_key}", pen, answer) 
	r.hset(f"{ap}:pen:{line_key}:tm", f"{pen}:{tm}", answer) 
	r.zadd(f"{ap}:pen:{line_key}:answer", {f"{pen}:{line_key}:{answer}": float(tm)} ) 

def listen(): 
	print ('start to listen : pen_line_stroke', r, now(), flush=True)
	ps = r.pubsub(ignore_subscribe_messages=True)  #https://pypi.org/project/redis/
	ps.subscribe(**{'pen_line_stroke': pen_line_stroke})
	thread = ps.run_in_thread(sleep_time=0.001)
	#thread.stop()

if __name__ == '__main__': 
	pen_line_stroke("testap:1713.537.31.86:line-11:pen-ZZ:1622197997:884,3026,100,1622197997 883,3025,522,1622197997 882,3026,582,1622197997 885,3027,624,1622197997 890,3025,640,1622197997 902,3022,652,1622197997 913,3025,660,1622197997 919,3025,664,1622197997 932,3024,668,1622197997 941,3027,672,1622197997 954,3028,676,1622197997 993,3022,684,1622197997 1024,3023,688,1622197997 1057,3029,692,1622197997 1089,3027,688,1622197997 1125,3024,672,1622197997 1190,3013,688,1622197997 1225,3011,708,1622197997 1280,3009,712,1622197997 1318,3004,724,1622197997 1366,2997,724,1622197997 1421,2993,728,1622197997 1497,2993,736,1622197997 1555,2994,744,1622197997 1624,2994,748,1622197997 1703,2988,748,1622197997 1759,2987,740,1622197997 1837,2987,744,1622197997 1895,2987,740,1622197997 1946,2987,732,1622197997 1981,2988,728,1622197997 1992,2987,744,1622197997 1990,2984,748,1622197997 1985,2978,628,1622197997")
