# 21-8-4   1.24,  kvrocks 6666,  zset 
import pika,json, sys, time,  redis, pymysql,fire

# eng_essay_version, 35 in all
eev_fields	= "id,essay_id,request_id,author_id,internal_idx,title,essay,essay_html,tm,user_id,sent_cnt,token_cnt,len,ctime,stu_number,stu_name,stu_class,type,score,qw_score,sy_score,pigai,pigai_time,gram_score,is_pigai,version,cate,src,tid,fid,tag,is_chang,jianyi,anly_cnt,mp3".split(",")
eev_list	= lambda arr:  ( int(arr['id']),int(arr['essay_id']),int(arr['request_id']),int(arr['author_id']),int(arr['internal_idx'] if arr['internal_idx'] else 0),arr['title'],arr['essay'],arr['essay_html'], arr['tm'],int(arr['user_id']),int(arr['sent_cnt']),int(arr['token_cnt']),int(arr['len']),int(arr['ctime']),arr['stu_number'],arr['stu_name'],arr['stu_class'], int(arr['type']),float(arr['score']),float(arr['qw_score']),float(arr['sy_score']),arr['pigai'],int(arr['pigai_time']),float(arr['gram_score']), int(arr['is_pigai']),int(arr['version']),int(arr['cate']),arr['src'],int(arr['tid']),int(arr['fid']),arr['tag'],int(arr['is_chang']),arr['jianyi'],int(arr['anly_cnt']),arr['mp3'] )
#Ex: int() argument must be a string, a bytes-like object or a number, not 'NoneType'

def callback(ch, method, properties, body):
	r = redis.r
	try:
		ch.basic_ack(delivery_tag = method.delivery_tag)
		line = body.decode()
		arr = json.loads(line.replace('"internal_idx":null,','"internal_idx":0,'))
		eid = arr['essay_id'] 
		rid = arr['request_id']
		uid = arr['user_id']

		if eid: r.zadd(eid, { json.dumps( eev_list(arr)) : int(arr.get('version',0))} )
		if rid and int(rid) != 10: r.zadd(f"rid:{rid}", {eid: arr.get('score',0)})
		if uid: r.zadd(f"uid:{uid}", {eid: arr.get('score',0)})

		r.set("maxid", arr["id"]) # added 2021.8.2
		r.publish("log", line ) 

		with redis.my_conn.cursor() as cursor:
			cursor.execute("insert ignore into eng_essay_version_2020_6(id,essay_id,request_id,author_id,internal_idx,title,essay,essay_html,tm,user_id,sent_cnt,token_cnt,len,ctime,stu_number,stu_name,stu_class,type,score,qw_score,sy_score,pigai,pigai_time,gram_score,is_pigai,version,cate,src,tid,fid,tag,is_chang,jianyi,anly_cnt,mp3) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (arr['id'],arr['essay_id'],arr['request_id'],arr['author_id'],arr['internal_idx'],arr['title'],arr['essay'],arr['essay_html'],arr['tm'],arr['user_id'],arr['sent_cnt'],arr['token_cnt'],arr['len'],arr['ctime'],arr['stu_number'],arr['stu_name'],arr['stu_class'],arr['type'],arr['score'],arr['qw_score'],arr['sy_score'],arr['pigai'],arr['pigai_time'],arr['gram_score'],arr['is_pigai'],arr['version'],arr['cate'],arr['src'],arr['tid'],arr['fid'],arr['tag'],arr['is_chang'],arr['jianyi'],arr['anly_cnt'],arr['mp3']))

	except Exception as ex:
		print(">>Ex:", ex, body.decode())

def run( QUEUE_NAME , host='172.17.0.1',port=3306,user='root',password='cikuutest!',db='eev', redis_port=6666, redis_db=0, mq_host='192.168.1.214', mq_port=5672, mq_user='pigai', mq_pwd='NdyX3KuCq'):
	''' consume to redis-kvrocks/6666 and myeev/3306 , essay_version_kvrocks_6666, 2021.8.4 '''
	redis.my_conn = pymysql.connect(host=host,port=port,user=user,password=password,db=db)
	redis.r = redis.Redis(host=host, port=redis_port, db=redis_db, decode_responses=True) #redis_host='192.168.1.23',

	credentials = pika.PlainCredentials(mq_user, mq_pwd)  
	connection = pika.BlockingConnection(pika.ConnectionParameters(host = mq_host,port = mq_port,virtual_host = '/',credentials = credentials))
	channel=connection.channel()

	### global variable modified ?   my_host and redis_host is the same

	result = channel.queue_declare(queue = QUEUE_NAME, durable=True)
	print("queue is :", QUEUE_NAME, flush=True)

	channel.basic_consume(QUEUE_NAME, callback)
	channel.start_consuming()

if __name__ == '__main__':
	fire.Fire(run)


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