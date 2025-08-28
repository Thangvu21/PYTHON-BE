import os
from dotenv import load_dotenv

load_dotenv()

host_redis = os.environ.get('host_redis')
backend_redis = os.environ.get('backend_redis')
host_redis_build = os.environ.get('host_redis_build')

host_redis_not_docker = os.environ.get('host_redis_not_docker')
backend_redis_not_docker = os.environ.get('backend_redis_not_docker')

db = os.environ.get('DB_URL_DOCKER')
db_not_docker = os.environ.get('DB_URL_NOT_DOCKER')
db_build = os.environ.get('DB_URL_BUILD')

key_pexel = os.environ.get('KEY_PEXELS')

host_local_redis = os.environ.get('host_local_redis')
host_local_redis_docker = os.environ.get('host_local_redis_docker')

# print(host_redis)

class Configuration():
    def __init__(self):
        self.host_redis = host_redis
        self.backend_redis = backend_redis
        self.host_redis_build = host_redis_build

        self.host_redis_not_docker = host_redis_not_docker
        self.backend_redis_not_docker = backend_redis_not_docker


        self.db = db
        self.db_not_docker = db_not_docker
        self.db_build = db_build
        
        self.key_pexels = key_pexel

        self.host_local_redis = host_local_redis
        self.host_local_redis_docker = host_local_redis_docker

        
config_server = Configuration()  