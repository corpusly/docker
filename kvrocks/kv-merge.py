# 2021.8.3, merge zset -> string:  [[], [], ]
import redis ,fire, json
from tqdm import tqdm

def dump(pattern, host = 'localhost', port=6666,db=0, db1=1):
	r = redis.Redis(host=host, port=port, db=db, decode_responses=True)
	r1 = redis.Redis(host=host, port=port, db=db1, decode_responses=True)
	print (r, r1, flush=True)
	for k in tqdm(r.keys(pattern)): #.scan_iter(): 
		try:
			if r.type(k) == 'zset' and not ':' in k : 
				values = ",".join(r.zrevrange(k, 0, -1))
				r1.set(k, f"[{values}]")
		except Exception as e: 
			print("ex:", e, k )
	print ("finished:", dbfile)

if __name__ == '__main__':
	fire.Fire(dump)

'''
192.168.1.23:6666[1]> get 13305
"[[444485453, 13305, 10525, 0, 0, \"Create a Green Campus(2009-12 CET4)\", \"In ancient times, people lived a comfortable life. Before a bridge was invented, people used to ride on a piece of wood when they crossed a river. As time goes on, people began to feel inconvenient, so they cut down the trees, the connection on the trees on both sides of the river bridge, known as \\\"wooden bridge\\\", which not only make the traffic more convenient, but also fully demonstrate the wisdom of the ancients!\\nBut over time, people find that the bridge had more and more shortcomings, because the bridge is too easy to break. Therefore, the wise found a bridge built of stone, which was much stronger and wider than a wooden bridge, but is that enough? People found that the pressure of the tide might crush it, so they dug a few small bridge holes under the bridge, and dug a bridge hole in the middle, so that there is no pressure to crush it.\\nWith the development of science and technology, people began to build bridges across rivers. First, they put a large hollow column in the soil, and then they took out the soil and water from the columns. Finally, they poured reinforced concrete into the hollow columns, and then they made a few more piers. Finally do the deck, so, a huge project-across the river bridge completed! In order to facilitate the traffic, people built overpass on land again. Through the transference of overpasses, pedestrian bridges, the traffic in the world will have a new look. So that we can travel more smoothly! \\nThe bridge is not only a tool to facilitate communication, but also a crystallization of human\", \"\", \"2018-07-13 12:16:18\", 0, 8, 154, 1550, 1531455377, \"2009150012\", \"\", \"\\u82f1\\u8bedA\\u73ed\", 0, 88.878, 89.287, 0.0, \"\", 0, 21.0, 1, 1742, 0, \"ajax_postSave_v2_wri\", 0, 0, \"\", 0, \"\", 1, \"\"],[388619422, 13305, 10525, 9679, 0, \"How I celebrate Christmas\", \"How I celebrate Christmas\\n In fact Christmas is a western traditional festival.Seldom have l celebrated it at my young age.Recently,Christmas becomes more and more popular and I began to celebrate Christmas.\\n In this day people will send gifts to their families and friends, which usually are chocolates and flowers for girls.It seems is another Valentine's Day .Besides that, it is a special present in China that we give out apples at Christmas Eve.Because apple in Chinese is called \\\"ping guo\\\"which is similar to\\\" ping an\\\" so Chinese think apple is a great gift to bring fortune to the receiver.As the monitor of our class,I have prepare apples for every one in class 173.It's the first Christmas we will have at NCU.I'd like to leave a deep impression to my classmates \\n Though Christmas customs between China and west are quite different, one thing is in common which is stay together with friends and families .No matter staying at home with families or hanging out with friends is a good choice to celebrate Christmas .Sitting around ,singing songs ,playing games and giving our wishes to the people we love that's how I celebrate Christmas\", \"\", \"2017-12-24 10:56:36\", 0, 8, 154, 1147, 1514084187, \"2009150012\", \"\", \"\\u82f1\\u8bedA\\u73ed\", 0, 87.2523, 87.6567, 0.0, \"\", 0, 21.0, 1, 1356, 0, \"ajax_postSave_v2_wri\", 0, 0, \"\", 0, \"\", 1, \"\"]]"

every 180 days  ,scan  db0 (zset), merge to db1 (string) arc ,

'''