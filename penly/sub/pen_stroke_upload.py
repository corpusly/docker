# 21-6-8
import json,  redis, time, traceback, os,sys, requests, socket
r = redis.Redis(host="172.17.0.1", port=6379, db=0, decode_responses=True)
#http://penly.cn:9000/penly/publish?msg=hjzx-2-4%3A1713.536.33.70%3ABP2-1A3-03I-AA%3A1619167930.231%3A585%2C7530%2C507%2C1619167930%20591%2C7549%2C591%2C1619167930%20601%2C7564%2C672%2C1619167930%20610%2C7568%2C724%2C1619167930%20616%2C7567%2C748%2C1619167930%20619%2C7565%2C796%2C1619167930%20624%2C7556%2C816%2C1619167930%20648%2C7531%2C844%2C1619167930%20696%2C7495%2C880%2C1619167930%20798%2C7388%2C904%2C1619167930%20825%2C7365%2C924%2C1619167930%20832%2C7361%2C940%2C1619167930%20833%2C7362%2C672%2C1619167930%20833%2C7363%2C716%2C1619167930%20831%2C7362%2C289%2C1619167930%20827%2C7348%2C289%2C1619167930&channel=pen_stroke
hostname = socket.gethostname()
print ("my hostname :", hostname, flush=True)

def pen_stroke(msg):  # ap,page,pen,tm,stroke
	try:
		requests.get("http://penly.cn:9000/penly/publish", params={'msg':msg,'channel':'pen_stroke'})
	except Exception as ex:
		print ( ">>pen_stroke upload ex:", ex, "\t", msg, flush=True) 

def listen(): 
	if not hostname in ('VM-0-7-ubuntu'):# 138 can upload to itself
		print ('>>listen channels: pen_stroke ', r, flush=True)
		ps = r.pubsub(ignore_subscribe_messages=True)  #https://pypi.org/project/redis/
		ps.subscribe(**{'pen_stroke':pen_stroke}) 
		thread = ps.run_in_thread(sleep_time=0.001)
		#thread.stop()
	else:
		print ("CAN NOT upload to myself:", hostname, flush=True)

if __name__ == '__main__': 
	listen()