from sqlalchemy import create_engine
from src.config.conf import config_server
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime
import uuid

DATABASE_URL = config_server.db_build
engine = create_engine(DATABASE_URL)


Base = declarative_base()

# class Image(Base):
#     __tablename__ = "images"
#     id = Column(String(50), primary_key=True, index=True, default= lambda: str(uuid.uuid4()))
#     url = Column(String(250))
#     time_saved = Column(DateTime, default=datetime.now)

#     def __repr__(self):
#         return f"Image(id={self.id}, url={self.url}, time_saved={self.time_saved})"
    
# Base.metadata.create_all(engine)