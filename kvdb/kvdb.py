#!/usr/bin/env  -*- coding: utf-8	-*-  2021.2.1
import sqlite3,json,zlib,collections
class Kvdb(collections.UserDict): 
	def	__init__(self, filename, tablename='kv', keylen=256, 
				compress	= lambda obj: sqlite3.Binary(zlib.compress(json.dumps(obj).encode())), 
				decompress	= lambda obj: json.loads(bytes.decode(zlib.decompress(bytes(obj))))):
		self.filename	= filename
		self.tablename	= tablename
		self.compress	= compress
		self.decompress = decompress
		self.conn		= sqlite3.connect(self.filename, check_same_thread=False) 
		self.conn.execute(f'CREATE TABLE IF NOT EXISTS {self.tablename} (key varchar({keylen}) PRIMARY KEY, value blob)')
		self.conn.execute('''CREATE VIRTUAL TABLE if not exists fts USING fts5(snt, terms, columnsize=0, detail=none,tokenize = "unicode61 remove_diacritics 0 tokenchars '-_'")''')
		self.conn.execute('PRAGMA synchronous=OFF')
		self.conn.commit()

	def index(self, snt, termlist):  self.conn.execute(f"insert or ignore into fts(snt,terms) values(?,?)", (snt, termlist)) # one,two,three
	def search(self, query, topn=10): list(self.conn.execute(f"SELECT rowid,* FROM fts where fts match 'overcome' order by rank limit {topn}"))

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
		return None if item	is None else self.decompress(item[0]) # else json.loads(...)
	def get(self, key, defau=None): return self[key] if self.__contains__(key) else defau
	def	__call__(self, key, topn=10): return self[key][0:topn] # ztop 

	def	__setitem__(self, key, value): 	self.conn.execute('REPLACE	INTO "%s" (key,	value) VALUES (?,?)' % self.tablename,	(key, self.compress(value)))
	def set(self, key, value): self[key] = value
	def	__delitem__(self, key): self.conn.execute('DELETE FROM	"%s" WHERE key = ?'	% self.tablename,	(key,))
	def	__iter__(self): return self.keys()
	def	close(self): 	self.conn.commit()
	def	commit(self): 	self.conn.commit()

def hello():
	db =  Kvdb("test.kvdb")
	db['one'] = {'one':3, 'two':5}
	db['two'] = 1.234
	db.index('I overcome the problem.', 'love/v you/n')
	db.commit()
	print (list(db.keys()))
	print (db.get('two'))
	print (db.search("overcome"))
	print (  list(db.conn.execute("SELECT rowid,* FROM fts where fts match 'overcome' order by rank limit 3")) )
	db.close()

def index(docbsfile, kvdb):  
	''' clec.docbs -> clec.kvdb, 2021.2.1 '''
	from cikuu.api import docf, docbs, zset
	db = docbs.Docbs(docbsfile)
	zs = zset.Zset() #zs = docf.indexdocs( db.docs() )
	dbout = Kvdb(kvdb) 
	for doc in db.docs() :
		try:
			docf.index_doc(zs, doc)
			terms = [ f"{t.lemma_}_{t.pos_}" for t in doc]
			[ terms.append( f"{t.dep_}_{t.head.pos_}_{t.pos_}_{t.head.lemma_}_{t.lemma_}" ) for t in doc if t.pos_ not in ('PRON','PUNCT') and t.dep_ in ('dobj','nsubj','advmod','acomp','amod','compound','xcomp','ccomp')]
			dbout.index(doc.text, " ".join(terms))
		except Exception as e:
			print ("ex:", e, doc)
	for k,v in zs.items():  dbout[k] = v.most_common()
	for s,i in zs['sum'].items(): dbout[f"sum:{s}"] = i # sum:LEX, sum:NOUN, dobj, snt, is there any overwrite ? 
	dbout.commit()
	print (f"[kvdb-index] finished, {docbsfile} -> {kvdb}")

if __name__	== '__main__':
	import fire
	fire.Fire(index)