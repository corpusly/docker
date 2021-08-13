# 21-6-8
import json,  redis, time, traceback, os,sys, pymysql
r = redis.Redis(host="172.17.0.1", port=6379, db=0, decode_responses=True)
my_conn = pymysql.connect(host='172.17.0.1',port=3306,user='root',password='cikuutest!',db='penly')
cursor = my_conn.cursor()

def pen_stroke(msg):  # ap,page,pen,tm,stroke
	try:
		#print (msg['data'], flush=True)
		ap,page,pen,tm,stroke = msg['data'].strip().split(":")[0:5]
		cursor.execute("insert ignore into pen_stroke(pen,page,ap,stroke,tm) values(%s,%s,%s,%s,from_unixtime(%s))", (pen,page,ap,stroke, float(tm) ))
		my_conn.commit() 
	except Exception as ex:
		print ( ">>pen_stroke to mariadb ex:", ex, "\t", msg, flush=True) 

def listen(): 
	print ('>>listen channels: pen_stroke ', r, my_conn, flush=True)
	ps = r.pubsub(ignore_subscribe_messages=True)  #https://pypi.org/project/redis/
	ps.subscribe(**{'pen_stroke':pen_stroke}) 
	thread = ps.run_in_thread(sleep_time=0.001)
	#thread.stop()

if __name__ == '__main__': 
	listen()