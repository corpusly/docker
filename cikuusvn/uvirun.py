# 2021-2-6, 
import uvicorn,fire,os
#app = FastAPI()

def run(pyfile='/home/cikuu/uvirun/hello.py', svn='/home/cikuu', svnup=True, port=80, host='0.0.0.0', pip=None, wgeturl=None, wgetfile=None, mkdir=None, tar=None, **kwargs):
	try:
		if tar: 
			os.system(f"wget {tar} -O /tmp.tar.gz")
			os.system(f"tar zxvf /tmp.tar.gz")
			os.system(f"rm /tmp.tar.gz")
		if mkdir: os.system(f"mkdir {mkdir}") # mkdir /sidb
		if wgeturl: os.system(f"wget {wgeturl} -O {wgetfile}") # /wget.py, or bnc.sidb 
		if pip: [ os.system(f"pip install {name.strip()}") for name in pip.split(",")] # pygtrie
		if svnup: os.system(f"svn up {svn} --username zhangyue --password zhangy1235") # to a certain version ? 

		code = open(pyfile).read()
		scope = {}
		exec(code, scope)
		uvicorn.run(scope['app'], host=host, port=port)
	except Exception as e: 
		print ("ex:", e) 

if __name__ == '__main__': 
	fire.Fire(run)