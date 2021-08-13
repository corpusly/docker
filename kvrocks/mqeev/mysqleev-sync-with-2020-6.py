# 8-8 , 1.54.eng_essay to local eng_essay
import fire, pymysql,json, sys, time, datetime
#eev_conn = pymysql.connect(host='172.17.0.1',port=3306,user='root',password='cikuutest!',db='eev')

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

def dump( id_where , host='192.168.1.54',port=3306,user='cikuu',password='cikuutest!',db='pigai_org', eevhost='localhost',eevport=3306,eevuser='root',eevpassword='cikuutest!',eevdb='eev'):
	''' id > 773841099 , 2021.8.8 '''
	my_conn = pymysql.connect(host=host,port=port,user=user,password=password,db=db)
	eev_conn = pymysql.connect(host=eevhost,port=eevport,user=eevuser,password=eevpassword,db=eevdb)
	with my_conn.cursor(pymysql.cursors.SSDictCursor) as cursor:
		cursor.execute(f"select * from pigai_org.eng_essay_version_2020_6 where id {id_where}")
		row = cursor.fetchone()
		while row is not None: #for row in cursor.fetchall_unbuffered():
			try:
				arr = json.loads(json.dumps(row,cls=DateEncoder))
				with eev_conn.cursor() as eev_cursor:
					eev_cursor.execute("insert ignore into eev.eng_essay_version_2020_6(id,essay_id,request_id,author_id,internal_idx,title,essay,essay_html,tm,user_id,sent_cnt,token_cnt,len,ctime,stu_number,stu_name,stu_class,type,score,qw_score,sy_score,pigai,pigai_time,gram_score,is_pigai,version,cate,src,tid,fid,tag,is_chang,jianyi,anly_cnt,mp3) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (arr['id'],arr['essay_id'],arr['request_id'],arr['author_id'],arr['internal_idx'],arr['title'],arr['essay'],arr['essay_html'],arr['tm'],arr['user_id'],arr['sent_cnt'],arr['token_cnt'],arr['len'],arr['ctime'],arr['stu_number'],arr['stu_name'],arr['stu_class'],arr['type'],arr['score'],arr['qw_score'],arr['sy_score'],arr['pigai'],arr['pigai_time'],arr['gram_score'],arr['is_pigai'],arr['version'],arr['cate'],arr['src'],arr['tid'],arr['fid'],arr['tag'],arr['is_chang'],arr['jianyi'],arr['anly_cnt'],arr['mp3']))

				print(arr['id'])
				row = cursor.fetchone()
			except Exception as e:
				print("ex:", e, row['essay_id'])
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