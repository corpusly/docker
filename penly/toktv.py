#  python toktv.py  config:* --host 172.21.0.17   | 21-7-29
import redis ,fire, pymysql,json

def insert(cursor, k, t, v, tab): 
	cursor.execute( f"replace into {tab}(k,t,v) values(%s,%s,%s)" , (k,t,v))

def dump(pattern, rhost = '172.17.0.1', rport=6379, rdb=0, host='172.17.0.1',port=3306,user='root',password='cikuutest!',db='penly', tab='redis_ktv'):
	'''   pattern:   config:*,  dump data from redis -> mysql   '''
	r = redis.Redis(host=rhost, port=rport, db=rdb, decode_responses=True)
	my_conn = pymysql.connect(host=host,port=port,user=user,password=password,db=db)
	print (pattern, r, my_conn, flush=True) # config:*
	with my_conn.cursor() as cursor: 
		cursor.execute(f"CREATE TABLE if not exists {tab}(k varchar(256) not null primary key, t varchar(32) not null, v MediumText not null) engine=myisam")
		for k in r.keys(pattern): #scan_iter
			try:
				type =  r.type(k)
				if type == 'hash': 
					insert(cursor, k, type, json.dumps(r.hgetall(k)), tab)
				elif type == 'zset': 
					insert(cursor, k, type, json.dumps(dict(r.zrevrange(k, 0,-1, True))), tab)
				elif type == 'list': 
					insert(cursor, k, type, json.dumps(r.lrange(k,0,-1)), tab)
				elif type == 'set': 
					insert(cursor, k, type, json.dumps(r.smembers(k)), tab)
				elif type == 'string': 
					insert(cursor, k, type, r.get(k), tab)
			except Exception as e: 
				print("ex:", e, "\t", k)
	my_conn.commit()
	print(">> finished: ",  pattern)

if __name__ == '__main__':
	fire.Fire(dump)