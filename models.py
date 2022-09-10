from time import time
import uuid
from db import Base, engine
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import BIGINT, VARCHAR, TIMESTAMP, LONGTEXT, INTEGER, DOUBLE, BOOLEAN

class DataModel(Base):
    __tablename__ = "sufen"
    
    id = Column(VARCHAR(length=100), primary_key=True, default=lambda : uuid.uuid1().int, index=True)
    time = Column(TIMESTAMP, default=lambda :time())
    image = Column(LONGTEXT)
    status = Column(BOOLEAN, nullable=True)
    latitude = Column(DOUBLE, nullable=False)
    longitude = Column(DOUBLE, nullable=False)
    
    
    def __init__(self, id, time, image, status, latitude, longitude):
        self.id = id
        self.time = time
        self.image = image
        self.status = status
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return f"<sufen('{self.id}', '{self.time}', '{self.image}', '{self.status}', '{self.latitude}', '{self.longitude}')>"
    
Base.metadata.create_all(bind=engine)
