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

@app.post("/accident")
async def postData(data: RequestModel, db: Session = Depends(get_db)):
    data_dict = data.dict()
    new_latitude, new_longitude = calculate(data_dict["heading"], data_dict["latitude"], data_dict["longitude"])
    new_data = DataModel(id=str(uuid4()), time=func.now(), status=None, 
                        latitude=new_latitude, 
                        longitude=new_longitude, 
                        image=data_dict["img"])
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    return {"data": new_data, "status": "success"}

@app.post("/hardware")
async def postHardwareData(data: RequestHardwareModel):
    data_dict = data.dict()
    f = open("./hardware.bin", "w")
    f.truncate()
    f.write(data_dict)
    f.close()
    return {"data": data_dict, "status": "success"}

@app.get("/hardware")
async def getHardwareData():
    f = open("./hardware.bin", "r")
    data = f.read()
    f.close()
    return {"data": data, "status": "success"}

@app.get("/accident")
async def getAllAccidentData(db: Session = Depends(get_db)):
    data = db.query(DataModel).filter(DataModel.status==None).order_by(DataModel.time.desc()).all()
    return {"history": data, "totalCount": len(data)}


@app.get("/accident/{id}")
async def getOneAccidentData(id: str, db: Session = Depends(get_db)):
    return db.query(DataModel).filter(DataModel.id == id).first()

@app.put("/accident")
async def updateStatus(data: PutModel, db:Session = Depends(get_db)):
    up_data = db.query(DataModel).filter(DataModel.id == data.id).first()
    up_data.status = data.status
    db.commit()
    db.refresh(up_data)
    return up_data
