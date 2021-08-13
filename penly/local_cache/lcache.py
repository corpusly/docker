# 2021-3-1, uvicorn app  | docker run -itd -p 7084:8000 --name sidb wrask/sidb:clecdic
import uvicorn,os,fire
from fastapi import FastAPI 
from fastapi.responses import HTMLResponse

import sqlite3,collections
class Ssdb(collections.UserDict): 
	def	__init__(self, filename, tablename='ss', keylen=128):
		self.filename	= filename
		self.tablename	= tablename
		self.conn		= sqlite3.connect(self.filename, check_same_thread=False) 
		self.conn.execute(f'CREATE TABLE IF NOT EXISTS {self.tablename} (key varchar({keylen}) PRIMARY KEY, value text)')
		self.conn.execute('PRAGMA synchronous=OFF')
		self.conn.commit()

	def	__str__(self): 	return "SqliteDict(%s)"	% (self.filename)
	def	__repr__(self): return str(self)  #	no need	of something complex
	def	__len__(self):	return self.conn.execute('SELECT COUNT(*) FROM	"%s"' %	self.tablename).fetchone()[0]
	def	count(self):	return self.conn.execute('SELECT count(*) FROM "%s"'% self.tablename).fetchone()[0]

	def	keys(self, start=0, len=-1):  
		for key in self.conn.execute(f'SELECT key FROM {self.tablename} ORDER BY rowid limit {start},{len}' ).fetchall(): yield key[0]
	def	values(self, start=0, len=-1): 
		for	value in self.conn.execute(f'SELECT value FROM {self.tablename} ORDER BY rowid  limit {start},{len}').fetchall(): yield value[0]
	def	items(self, start=0, len=-1): 
		for key, value in self.conn.execute(f'SELECT key, value FROM {self.tablename} ORDER BY rowid limit {start},{len}' ).fetchall(): 	yield key, value
	def	__contains__(self, key): return self.conn.execute('SELECT 1 FROM "%s" WHERE key = ?' %	self.tablename, (key,)).fetchone() is not None

	def	__getitem__(self, key):
		item = self.conn.execute(f'SELECT value FROM "{self.tablename}" WHERE key = ? limit 1', (key,)).fetchone()
		return None if item	is None else item[0] 
	def get(self, key, defau=None): return self[key] if self.__contains__(key) else defau
	def	__call__(self, key, topn=10): return self[key][0:topn] # ztop 

	def	__setitem__(self, key, value): 	self.conn.execute('REPLACE	INTO "%s" (key,	value) VALUES (?,?)' % self.tablename,	(key, value))
	def set(self, key, value): self[key] = value
	def	__delitem__(self, key): self.conn.execute('DELETE FROM	"%s" WHERE key = ?'	% self.tablename,	(key,))
	def	__iter__(self): return self.keys()
	def	close(self): 	self.conn.commit()
	def	commit(self): 	self.conn.commit()
	def	fetch(self, sql): 	return list(self.conn.execute(sql))

app = FastAPI()
map = {filename.lower().split(".")[0] : sidb.Sidb(f'/sidb/{filename}') for filename in os.listdir('/sidb') if filename.endswith(".sidb") }

@app.get('/')
def home(): return HTMLResponse(content=f"<h2> ssdb-based local cache </h2> <a href='/docs'> docs </a> | <a href='/redoc'> redoc </a> <br>2021-7-31")

@app.get('/sidb/{name}/{prefix}') 
def search_sidb_range_by_prefix(name: str='dic', prefix: str = 'dobj_VERB_NOUN:open:', topn:int=-1, divby:str=None):  
	''' name: dic/clec  prefix: ~dobj_VERB_NOUN:door: , divby: sum:dobj_VERB_NOUN:open, VERB:book, '''
	try:
		divsum = list(map[name].conn.execute(f"select value from si where key = '{divby}'"))[0][0] if divby else 1
		res = list(map[name].conn.execute(f"select * from si where key between '{prefix}' and '{prefix}~' order by value desc limit {topn}")) # ascii(~) is the second largest ascii char
		return [ (s.split(prefix)[-1], i/divsum) for s, i in res] #return JSONResponse(content=[ (s.split(prefix)[-1], i/divsum) for s, i in res])
	except Exception as e: 
		print ("ex:", e, name, prefix)
		return []

@app.get('/sidb/sql')
def run_sql(sql:str="select * from ss limit 3"):  return list(db.conn.execute(sql))

def start( dbfile, host='0.0.0.0', port=80):
	db =  Ssdb(dbfile)
	uvicorn.run(app, host='0.0.0.0', port=80)

if __name__ == '__main__':
	fire.Fire(start)

def hello():
	db =  Ssdb(":memory:") #"test.sidb")
	db['two'] = "world"
	db.commit()
	print (list(db.keys()))
	print (db.get('two'))
	db.close()

'''
import requests

from requests.adapters import HTTPAdapter

from requests.packages.urllib3.util import Retry

s = requests.Session()

s.mount('https://', HTTPAdapter(max_retries=Retry(total=5)))

resp_get = s.get(url=http_url, data={'key':'value'})
resp_post = s.post(url=http_url, data={'key':'value'})

'''