#!/usr/bin/env  -*- coding: utf-8	-*-  2021.2.12
import sqlite3,collections

class Fts5(collections.UserDict):  # key: str , value: int
	def	__init__(self, filename=":memory:"):
		self.filename = filename
		self.conn = sqlite3.connect(filename, check_same_thread=False) 
		self.conn.execute('''CREATE VIRTUAL TABLE if not exists fts USING fts5(snt, columnsize=0, detail=full,tokenize = "unicode61 remove_diacritics 0 tokenchars '-_'")''') #self.conn.execute('''CREATE VIRTUAL TABLE if not exists fts USING fts5(snt, terms, columnsize=0, detail=none,tokenize = "unicode61 remove_diacritics 0 tokenchars '-_'")''')
		self.conn.execute('PRAGMA synchronous=OFF')
		self.conn.commit()

	def index(self, snt):  self.conn.execute(f"insert or ignore into fts(snt) values(?)", (snt,)) 
	def search(self, query, topn=10): list(self.conn.execute(f"SELECT * FROM fts where fts match 'overcome' limit {topn}")) #order by rank desc 
	def clear(self): (self.conn.execute(f'drop TABLE IF EXISTS {self.tablename}'), self.conn.execute(f'drop TABLE IF EXISTS fts'))

	def	__str__(self): 	return "SqliteDict(%s)"	% (self.filename)
	def	__repr__(self): return str(self)  
	def	__len__(self):	return self.conn.execute('SELECT COUNT(*) FROM	fts').fetchone()[0]
	def	count(self):	return self.__len__()

	def	gramcnt(self, gram):	return self.conn.execute(f'''SELECT COUNT(*) FROM fts  where fts match '"{gram}"' ''').fetchone()[0]
	def	cooccur(self, w1,w2):	return self.conn.execute(f'''SELECT COUNT(*) FROM fts  where fts match '{w1} AND {w2}' ''').fetchone()[0]

def hello():
	db =  Fts5(":memory:") 
	db.index('I overcome the problem.')
	db.conn.commit()
	print (  list(db.conn.execute('''SELECT rowid,* FROM fts where fts match '"overcome the"' order by rank limit 3''')) )
	print (  list(db.conn.execute('''SELECT rowid,* FROM fts where fts match 'overcome AND problem' ''')) )
	print (db.gramcnt('overcome the'))
	print (db.search('overcome'))
	print (  list(db.conn.execute('''SELECT * FROM fts where fts match 'overcome' ''')) )

def load(sntfile):
	db =  Fts5(sntfile.split(".")[0].lower() + ".fts5") 
	for line in open(sntfile).readlines(): 
		if line: db.index(line.strip())
	db.conn.commit()
	print("finished", sntfile)

if __name__	== '__main__':
	hello()
	import fire
	fire.Fire(load)