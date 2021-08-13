#2020-8-20
import redis
import pandas as pd
rdic = redis.Redis(host='dev.werror.com', port=4328, db=0,  decode_responses=True)

excelFile = 'errant-type.xlsx'
df = pd.DataFrame(pd.read_excel(excelFile)) 
print(df.columns)

for index, row in df.iterrows(): #{ 'error': '冠词缺失', 'explanation':f'建议添加冠词<b>{edit.c_str}</b>'}
	try:
		value = "{ 'error': '" + row.error + "', 'explanation':f'" + row.explanation + "'}"
		#print(row.type,row.error, row.explanation, value)
		rdic.hset("errant:type", row.type, value)
	except Exception as e:
		print("ex", e)
