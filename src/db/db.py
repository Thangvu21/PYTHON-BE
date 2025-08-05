from sqlalchemy import create_engine
from src.config.conf import Configuration

config = Configuration()

DATABASE_URL = config.db_not_docker
engine = create_engine(DATABASE_URL)