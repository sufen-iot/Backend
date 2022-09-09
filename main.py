from time import time
from uuid import uuid1, uuid4
from fastapi import FastAPI, Depends
from schema import RequestModel, ResponseModel, PutModel
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from models import DataModel
from db import SessionLocal
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:8080",
    "http://localhost:3000",
    "http://localhost"
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

@app.post("/accident")
async def postData(data: RequestModel, db: Session = Depends(get_db)):
    data_dict = data.dict()
    new_data = DataModel(id=str(uuid4()), time=func.now(), status=False, 
                        latitude=data_dict["latitude"], 
                        longitude=data_dict["longitude"], 
                        heading=data_dict["heading"], image=data_dict["img"])
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    return {"data": new_data, "status": "success"}

@app.get("/accident")
async def getAllAccidentData(db: Session = Depends(get_db)):
    data = db.query(DataModel).all()
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