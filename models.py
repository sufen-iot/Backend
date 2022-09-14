from time import time
import uuid
from db import Base, engine
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import BIGINT, VARCHAR, TIMESTAMP, LONGTEXT, INTEGER, DOUBLE, BOOLEAN

# 데이터베이스 메인테이블
class DataModel(Base):
    __tablename__ = "sufen" # 테이블이 하나밖에 필요 없을 것 같아 테이블 이름을 팀명으로 함
    
    # 고유한 아이디
    id = Column(VARCHAR(length=100), primary_key=True, default=lambda : uuid.uuid4().int, index=True)
    # 데이터가 들어온 시간
    time = Column(TIMESTAMP, default=lambda :time())
    # base64 형태의 이미지 데이터를 저장하는 칼럼 
    # base64가 크기가 클 수 있기 때문에 최대한 긴 텍스트로 칼럼을 설정
    image = Column(LONGTEXT)
    # 사고가 났는지 안 났는지 판단한 결과를 저장하는 칼럼
    status = Column(BOOLEAN, nullable=True)
    # 헤딩 값으로 계산한 값을 저장하는 위도 경도 칼럼
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
    
# 데이터베이스를 생성하는 부분
Base.metadata.create_all(bind=engine)
