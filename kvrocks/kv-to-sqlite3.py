# 2021.8.3
import redis ,fire, json, sqlite3,zlib
from tqdm import tqdm

def dump(pattern, dbfile, host = 'localhost', port=6666,db=0, type='zset'):
	conn = sqlite3.connect(dbfile, check_same_thread=False)  
	conn.execute(f'DROP TABLE IF EXISTS {type}')
	conn.execute(f'CREATE TABLE {type} (key varchar(512) PRIMARY KEY, value blob)')
	conn.execute('PRAGMA synchronous=OFF')
	conn.commit()

	r = redis.Redis(host=host, port=port, db=db, decode_responses=True)
	for k in r.keys(pattern): #.scan_iter(): 
		try:
			if r.type(k) == type : 
				v = zlib.compress(json.dumps( dict(r.zrevrange(k, 0, -1, True)) ).encode())
				conn.execute(f'REPLACE INTO {type} (key, value) VALUES (?,?)',	(k, v))
		except Exception as e: 
			print("ex:", e, k )
	conn.commit()
	print ("finished:", dbfile)

if __name__ == '__main__':
	fire.Fire(dump)