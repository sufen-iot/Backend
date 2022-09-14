from math import cos, tan
from time import time
from uuid import uuid1, uuid4
from fastapi import FastAPI, Depends
from schema import RequestModel, RequestHardwareModel, ResponseModel, PutModel
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from models import DataModel
from db import SessionLocal
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

origins = [
    "http://localhost:8080",
    "http://localhost:3000",
    "http://localhost",
    "https://sufen.sunrin.in"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
   db = SessionLocal()
   try:
       yield db
   finally:
       db.close()

#
# 방위각과 위도 경도를 가지고 위치를 대략적으로 계산하는 함수
# 
# 방위각이 90보다 작으면 북쪽으로 100미터, 
# 방위각의 탄젠트 값 * 100미터만큼 동쪽으로 이동한 곳을 사고 예상 위치로 설정 
# 
# 방위각이 90보다 같거나 크고 180보다 작으면 서쪽으로 100미터, 
# 방위각 -90도의 탄젠트 값 * 100미터만큼 남쪽으로 이동한 곳을 사고 예상 위치로 설정 
# 
# 방위각이 180보다 같거나 크고 270보다 작으면 남쪽으로 100미터, 
# 방위각 -180도의 탄젠트 값 * 100미터만큼 서쪽으로 이동한 곳을 사고 예상 위치로 설정 
# 
# 방위각이 270보다 같거나 크면 서쪽으로 100미터, 
# 방위각 -270도의 탄젠트 값 * 100미터만큼 북쪽으로 이동한 곳을 사고 예상 위치로 설정 
# #
def calculate(heading, latitude, longitude):
    latitude_meter = latitude * 111132.954 
    longitude_meter  = 40075000 * cos(latitude) / 360 * longitude
    if heading < 90:
        longitude_meter += 100
        latitude_meter += tan(heading) * 100
        pass
    elif heading < 180:
        heading -= 90
        latitude_meter += 100
        longitude_meter -= tan(heading) * 100
        pass
    elif heading < 270:
        heading -= 180
        longitude_meter -= 100
        latitude_meter -= tan(heading) * 100
        pass
    else:
        heading -= 270
        latitude_meter -= 100
        longitude_meter += tan(heading) * 100
        pass
    
    return (latitude_meter / 111132.954 , longitude_meter / (40075000 * cos(latitude) / 360))

@app.post("/accident") # 하드웨어에서 보내는 요청 데이터를 받아 가공해서 데이터베이스에 저장
async def postData(data: RequestModel, db: Session = Depends(get_db)):
    data_dict = data.dict()
    # 위에 있는 계산함수로 계산한 위도 경도 값을 저장하는 부분
    new_latitude, new_longitude = calculate(data_dict["heading"], data_dict["latitude"], data_dict["longitude"]) 
    new_data = DataModel(id=str(uuid4()), time=func.now(), status=None, 
                        latitude=new_latitude, 
                        longitude=new_longitude, 
                        image=data_dict["img"])
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    return {"data": new_data, "status": "success"}

@app.post("/hardware") # 하드웨어 보내주는 하드웨어 정보를 저장
async def postHardwareData(data: RequestHardwareModel):
    data_dict = data.dict()
    f = open("./hardware.json", "w")
    f.truncate()
    f.write(json.dumps(data_dict))
    f.close()
    return {"data": data_dict, "status": "success"}

@app.get("/hardware") # 프론트엔드에서 하드웨어 정보를 요청 시 데이터를 보냄
async def getHardwareData():
    f = open("./hardware.json", "r")
    data = f.read()
    f.close()
    return {"data": json.loads(data), "status": "success"}

@app.get("/accident") # 사고 데이터 전체를 보내줌
async def getAllAccidentData(db: Session = Depends(get_db)):
    data = db.query(DataModel).filter(DataModel.status==None).order_by(DataModel.time.desc()).all()
    return {"history": data, "totalCount": len(data)}


@app.get("/accident/{id}") # id 값에 맞는 사고 데이터 하나만 보냄
async def getOneAccidentData(id: str, db: Session = Depends(get_db)):
    return db.query(DataModel).filter(DataModel.id == id).first()

@app.put("/accident") # 프론트에서 보낸 id 값에 맞는 데이터의 status를 변경해 저장
async def updateStatus(data: PutModel, db:Session = Depends(get_db)):
    up_data = db.query(DataModel).filter(DataModel.id == data.id).first()
    up_data.status = data.status
    db.commit()
    db.refresh(up_data)
    return up_data
