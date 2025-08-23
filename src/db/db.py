from sqlalchemy import create_engine
from src.config.conf import config_server

DATABASE_URL = config_server.db_not_docker
engine = create_engine(DATABASE_URL)