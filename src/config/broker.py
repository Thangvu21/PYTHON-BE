import redis
from src.config.conf import config_server
r = redis.Redis(host=config_server.host_local_redis, port=6379, password='123456')
print(r.ping())