import os
from dotenv import load_dotenv

load_dotenv()

host_redis = os.environ.get('host_redis')
broker_url = os.environ.get('broker_url')
db_url = os.environ.get('DB_URL_DOCKER')
db_not_docker = os.environ.get('DB_URL_NOT_DOCKER')
host_redis_not_docker = os.environ.get('host_redis_not_docker')
key_pexel = os.environ.get('KEY_PEXELS')

# print(host_redis)

class Configuration():
    def __init__(self):
        self.host_redis = host_redis
        self.broker_url = broker_url
        self.db_url = db_url
        self.db_not_docker = db_not_docker
        self.host_redis_not_docker = host_redis_not_docker
        self.key_pexels = key_pexel
        
        