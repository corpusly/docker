# 21-8-6   1.24,  kvrocks 6666,  zset 
import fire, pymysql,json, redis, sys, time, datetime
eev_list	= lambda arr:  ( int(arr['id']),int(arr['essay_id']),int(arr['request_id']),int(arr['author_id']),int(arr['internal_idx']),arr['title'],arr['essay'],arr['essay_html'], arr['tm'],int(arr['user_id']),int(arr['sent_cnt']),int(arr['token_cnt']),int(arr['len']),int(arr['ctime']),arr['stu_number'],arr['stu_name'],arr['stu_class'], int(arr['type']),float(arr['score']),float(arr['qw_score']),float(arr['sy_score']),arr['pigai'],int(arr['pigai_time']),float(arr['gram_score']), int(arr['is_pigai']),int(arr['version']),int(arr['cate']),arr['src'],int(arr['tid']),int(arr['fid']),arr['tag'],int(arr['is_chang']),arr['jianyi'],int(arr['anly_cnt']),arr['mp3'] )

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

def dump( id_where , host='192.168.1.54',port=3306,user='cikuu',password='cikuutest!',db='pigai_org', redis_host='localhost', redis_port=6666, redis_db=0):
	'''  > 773841099 '''
	my_conn = pymysql.connect(host=host,port=port,user=user,password=password,db=db)
	r = redis.Redis(host=redis_host, port=redis_port, db=redis_db, decode_responses=True)
	with my_conn.cursor(pymysql.cursors.SSDictCursor) as cursor:
		cursor.execute(f"select * from pigai_org.eng_essay_version_2020_6 where id {id_where}")
		row = cursor.fetchone()
		while row is not None: #for row in cursor.fetchall_unbuffered():
			try:
				#print (row['tm'] )
				arr = json.loads(json.dumps(row,cls=DateEncoder))
				eid = arr['essay_id'] 
				rid = arr['request_id']
				uid = arr['user_id']

				if eid: r.zadd(eid, { json.dumps( eev_list(arr)) : int(arr.get('version',0))} )
				if rid and rid != 10: r.zadd(f"rid:{rid}", {eid: arr.get('score',0)})
				if uid: r.zadd(f"uid:{uid}", {eid: arr.get('score',0)})

				print(arr['id'])
				row = cursor.fetchone()
			except Exception as e:
				print("ex:", e, row['id'])
				row = cursor.fetchone() # skip the abnormal row
	print(">> finished:", id_where)

if __name__ == '__main__':
	fire.Fire(dump)

'''
{"essay_id":"106486692","request_id":"1537544","author_id":"0","internal_idx":"2","title":"\u7b2c1537544\u53f7 \u6d3b\u52a8","essay":"Last days, New coro
navirus outbreak, I can saw many good people, they can for people who don't care about themselves. Of course, I can saw many bad people too, they make mo
ney by hook or crook. I like these nice people and I hate these bad people.\n I think this thing is a good thing, because it help us to see real people, 
we can see those people true character. But I think this thing are not good enough, because the level are not big enough. I can't really see those people
 very real character.\n Although I don't think it's severe enough, I hope this incident can be reslolved quickly.","essay_html":"","tm":"2020-03-02 20:19
:58","user_id":"21580850","sent_cnt":"0","token_cnt":"0","len":"589","ctime":"1583151597","stu_number":"11780818","stu_name":"\u738b\u535a\u8f69","stu_cl
ass":"\u521d\u4e09(6)\u73ed","type":"0","score":"82.1407","qw_score":"60.8876","sy_score":"0","pigai":"","pigai_time":"0","gram_score":"0","is_pigai":"1"
,"version":"3","cate":"0","src":"ajax_postSave_v2_wri","tid":"0","fid":"0","tag":"","is_chang":"0","jianyi":"","anly_cnt":"1","mp3":"","id":613970630}
'''