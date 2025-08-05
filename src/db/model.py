from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import datetime
import uuid
from src.db.db import engine

Base = declarative_base()

class Image(Base):
    __tablename__ = "images"
    id = Column(String(50), primary_key=True, index=True, default= lambda: str(uuid.uuid4()))
    url = Column(String(250))
    time_saved = Column(DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return f"Image(id={self.id}, url={self.url}, time_saved={self.time_saved})"
    
Base.metadata.create_all(engine)


