# 21-8-7   1.24,  kvrocks 6666,  zset 
import fire, pymysql,json, redis, sys, time, datetime, spacy
eev_list	= lambda arr:  ( int(arr['id']),int(arr['essay_id']),int(arr['request_id']),int(arr['author_id']),int(arr['internal_idx']),arr['title'],arr['essay'],arr['essay_html'], arr['tm'],int(arr['user_id']),int(arr['sent_cnt']),int(arr['token_cnt']),int(arr['len']),int(arr['ctime']),arr['stu_number'],arr['stu_name'],arr['stu_class'], int(arr['type']),float(arr['score']),float(arr['qw_score']),float(arr['sy_score']),arr['pigai'],int(arr['pigai_time']),float(arr['gram_score']), int(arr['is_pigai']),int(arr['version']),int(arr['cate']),arr['src'],int(arr['tid']),int(arr['fid']),arr['tag'],int(arr['is_chang']),arr['jianyi'],int(arr['anly_cnt']),arr['mp3'] )
nlp			= spacy.load("en_core_web_sm")  
nlp.add_pipe(nlp.create_pipe('sentencizer'))

def snt_br(essay):  
	doc = nlp(essay.strip(), disable=['tagger','parser','ner'])
	return [snt.text.strip() for snt in doc.sents]

import hashlib
sntmd5 = lambda sntarr: " ".join([hashlib.md5(snt.strip().lower().encode("utf-8")).hexdigest() for snt in sntarr])

class DateEncoder(json.JSONEncoder): #https://blog.csdn.net/t8116189520/article/details/88657533
	def default(self, obj):
		try:
			if isinstance(obj,datetime.datetime):
				return obj.strftime("%Y-%m-%d %H:%M:%S")
			elif isinstance(obj, bytes):
				return str(obj, encoding='utf-8')
			else:
				return json.JSONEncoder.default(self,obj)
		except Exception as e:
			print ("DateEncoder ex:", e, obj)
			return ""

class util(object):

	def eev(self, tab , host='192.168.1.24',port=3306,user='root',password='cikuutest!',db='eev'):
		''' python sntbr.py  eev "select * from eng_essay_version_2018 limit 3" '''
		my_conn = pymysql.connect(host=host,port=port,user=user,password=password,db=db)
		sys.stderr.write(f">> started: {tab} \n")
		with my_conn.cursor(pymysql.cursors.SSDictCursor) as cursor:
			cursor.execute(tab if " " in tab else "select * from " + tab)
			row = cursor.fetchone()
			while row is not None: #for row in cursor.fetchall_unbuffered():
				try:
					arr = json.loads(json.dumps(row,cls=DateEncoder))
					eid = arr['essay_id'] 
					ver = arr.get('version',0)
					snts = snt_br(arr['essay'])

					print(f"{eid}\t{ver}\t{json.dumps(snts)}")
					row = cursor.fetchone()
				except Exception as e:
					sys.stderr.write(f">> ex: {e},{row['id']} \n")
					row = cursor.fetchone() # skip the abnormal row
		sys.stderr.write(f">> finished: {tab} \n")

	def my_to_kvr(self, tab , host='192.168.1.24',port=3306,user='root',password='cikuutest!',db='eev', topn=30, kvhost='192.168.1.24', kvport=6667, kvdb=0):
		''' python sntbr.py my_to_kvr "select * from eng_essay_version_2018 limit 2"  ,2021.8.7 '''
		my_conn = pymysql.connect(host=host,port=port,user=user,password=password,db=db)
		r = redis.Redis(host=kvhost, port=kvport, db=kvdb, decode_responses=True)
		print(tab, my_conn, r, flush=True)
		with my_conn.cursor(pymysql.cursors.SSDictCursor) as cursor:
			cursor.execute(tab if " " in tab else "select * from " + tab)
			row = cursor.fetchone()
			while row is not None: #for row in cursor.fetchall_unbuffered():
				try:
					arr = json.loads(json.dumps(row,cls=DateEncoder))
					eid = arr['essay_id'] 
					ver = arr.get('version',0)
					snts = snt_br(arr['essay'])
					smd5 = sntmd5(snts[0:topn])

					#r.zadd(eid, {smd5: ver})
					r.hsetnx(eid, ver, smd5)
					print(arr['id'])
					row = cursor.fetchone()
				except Exception as e:
					print("ex:", e, row['id'])
					row = cursor.fetchone() # skip the abnormal row
		print(">> finished:", tab)

if __name__ == '__main__':
	fire.Fire(util)

'''
{"essay_id":"106486692","request_id":"1537544","author_id":"0","internal_idx":"2","title":"\u7b2c1537544\u53f7 \u6d3b\u52a8","essay":"Last days, New coro
navirus outbreak, I can saw many good people, they can for people who don't care about themselves. Of course, I can saw many bad people too, they make mo
ney by hook or crook. I like these nice people and I hate these bad people.\n I think this thing is a good thing, because it help us to see real people, 
we can see those people true character. But I think this thing are not good enough, because the level are not big enough. I can't really see those people
 very real character.\n Although I don't think it's severe enough, I hope this incident can be reslolved quickly.","essay_html":"","tm":"2020-03-02 20:19
:58","user_id":"21580850","sent_cnt":"0","token_cnt":"0","len":"589","ctime":"1583151597","stu_number":"11780818","stu_name":"\u738b\u535a\u8f69","stu_cl
ass":"\u521d\u4e09(6)\u73ed","type":"0","score":"82.1407","qw_score":"60.8876","sy_score":"0","pigai":"","pigai_time":"0","gram_score":"0","is_pigai":"1"
,"version":"3","cate":"0","src":"ajax_postSave_v2_wri","tid":"0","fid":"0","tag":"","is_chang":"0","jianyi":"","anly_cnt":"1","mp3":"","id":613970630}

docker run -itd --name aa wrask/spacy224 python sntbr.py my_to_kvr "select * from eng_essay_version_2019_4 where id > 524637072"
docker logs aa

/var/lib/docker/containers/container-ID/container-ID-json.log

cikuu@server24:~/tmp$ ps avx | grep sntbr
 6266 pts/0    Ssl+   2:26    273     0 1025164 214996  0.1 python sntbr.py my_to_kvr select * from eng_essay_version_2019_4 where id > 524637072

cikuu@VM-0-7-ubuntu:~/cikuu/docker/spacy/spacy224$ docker run --rm -it wrask/spacy224 
NAME
    sntbr.py

SYNOPSIS
    sntbr.py COMMAND

COMMANDS
    COMMAND is one of the following:

     my_to_kvr
       python sntbr.py my_to_kvr "select * from eng_essay_version_2018 limit 2"  ,2021.8.7

'''