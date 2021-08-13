# 21-5-11
import redis ,fire, pymysql,json

def process(tab, rhost = '172.17.0.1', rport=6379, rdb=0, host='172.17.0.1',port=3306,user='root',password='cikuutest!',db='penly'):
	'''   tab:   hjzx0511  '''
	r = redis.Redis(host=rhost, port=rport, db=rdb, decode_responses=True)
	my_conn = pymysql.connect(host=host,port=port,user=user,password=password,db=db)
	print (tab, r, my_conn, flush=True) # config:*
	[r.delete(k) for k in r.keys(f"{tab}:*")]
	with my_conn.cursor() as cursor: 
		cursor.execute(f"select * from {tab} where k like '{pattern}'")
		for row in cursor.fetchall(): # config:%
			try:
				r.publish('pen_stroke', row[0].strip())
			except Exception as e: 
				print("ex:", e, "\t", k)
	my_conn.commit()
	print(">> finished: ",  tab)

if __name__ == '__main__': 
	fire.Fire(process) 
