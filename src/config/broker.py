import redis
from src.config.conf import config_server
import os

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")   # default localhost
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "123456")

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)

# r = redis.Redis(host=config_server.host_local_redis, port=6379, password='123456')

print(r.ping())