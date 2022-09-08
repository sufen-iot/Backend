from time import time
import uuid
from db import Base, engine
from sqlalchemy import Column, Text, String, Float, TIMESTAMP, BigInteger, Boolean, Integer

class DataModel(Base):
    __tablename__ = "sufen"
    
    id = Column(String(length=100), primary_key=True, default=lambda : uuid.uuid1().int, index=True)
    time = Column(TIMESTAMP, default=lambda :time())
    image = Column(Text)
    status = Column(Boolean, default=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    heading = Column(Integer, default=0)
    
    
    def __init__(self, id, time, image, status, latitude, longitude, heading):
        self.id = id
        self.time = time
        self.image = image
        self.status = status
        self.latitude = latitude
        self.longitude = longitude
        self.heading = heading

    def __repr__(self):
        return f"<sufen('{self.id}', '{self.time}', '{self.image}', '{self.status}', '{self.latitude}', '{self.longitude}', '{self.heading}')>"
    
Base.metadata.create_all(bind=engine)