import redis
r = redis.Redis(host='localhost', port=6379, password='123456')
print(r.ping())