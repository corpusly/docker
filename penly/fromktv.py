# python fromktv.py config:% --rdb 1 --host 172.21.0.17   | 21-7-29
import redis ,fire, pymysql,json

def load(pattern, rhost = '172.17.0.1', rport=6379, rdb=0, host='172.17.0.1',port=3306,user='root',password='cikuutest!',db='penly', tab='redis_ktv'):
	'''   pattern:   config:%  ,  restore data from mysql -> redis '''
	r = redis.Redis(host=rhost, port=rport, db=rdb, decode_responses=True)
	my_conn = pymysql.connect(host=host,port=port,user=user,password=password,db=db)
	print (pattern, r, my_conn, flush=True) # config:*
	with my_conn.cursor() as cursor: 
		cursor.execute(f"select * from {tab} where k like '{pattern}'")
		for row in cursor.fetchall(): # config:%
			try:
				k, type, v =  row
				r.delete(k) ##
				if type == 'hash': 
					r.hmset(k, json.loads(v))
				elif type == 'zset': 
					r.zadd(k, json.loads(v))
				elif type == 'list': 
					for s in json.loads(v):
						r.rpush(k, s)
				elif type == 'set': 
					for s in json.loads(v):
						r.sadd(k, s)
				elif type == 'string': 
					r.hset(k, v) 
			except Exception as e: 
				print("ex:", e, row)
	my_conn.commit()
	print(">> finished: ",  pattern)

if __name__ == '__main__':
	fire.Fire(load)
