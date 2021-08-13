# 21-5-24
import redis
def dump(pattern, host='172.17.0.1', port=6379,db=0):
        r       = redis.Redis(host=host, port=port, db=db, decode_responses=True)
        ps = r.pubsub()
        ps.psubscribe(pattern)
        for item in ps.listen():
                if item['type'] == 'pmessage' and isinstance(item['data'], str):
                        print (item['channel'] + "=" + item['data'],flush=True)

if __name__ == '__main__':
        dump("pen_*")


