# 2021-3-4  python mqrun.py essay_version_to_snts http://cikuu.werror.com/app/mq/callback.py 
import pika,json, sys, time, fire,requests,os
now	= lambda: time.strftime('%Y.%m.%d %H:%M:%S ',time.localtime(time.time()))

def consume(queue_name='test_queue', callback_url='http://cikuu.werror.com/app/mq/hello.py', host='192.168.1.214', port=5672, user='pigai', pwd='NdyX3KuCq', func_name='callback'): 

	queue_name = os.getenv('queue_name', 'test_queue')
	callback_url = os.getenv('callback_url', 'http://cikuu.werror.com/app/mq/hello.py')
	host = os.getenv('host', '192.168.1.214')
	port = os.getenv('port', 5672)
	user = os.getenv('user', 'pigai')
	pwd = os.getenv('pwd', 'NdyX3KuCq')
	func_name = os.getenv('func_name', 'callback')

	print(f"queue is : {queue_name}, callback_url = {callback_url}, host:{host}, port:{port}, {user}, {pwd}", flush=True)
	credentials = pika.PlainCredentials(user, pwd)  
	connection = pika.BlockingConnection(pika.ConnectionParameters(host = host,port = port,virtual_host = '/',credentials = credentials))
	channel=connection.channel()

	try:
		result = channel.queue_declare(queue = queue_name, durable=True) #'snts_by_gec'
	
		code = requests.get(callback_url).text
		scope = {}
		exec(code, scope)

		#x = __import__(func_path, fromlist=['callback'])
		channel.basic_consume(queue_name, scope[func_name])
		channel.start_consuming()
		#connection.close()

	except Exception as e: 
		print ("mqrun consume ex:", e) 
		channel.close()
		connection.close()

if __name__ == '__main__': 
	fire.Fire(consume)