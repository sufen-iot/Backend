import string
from turtle import st
from pydantic import BaseModel

class RequestModel(BaseModel):
    heading: int
    latitude: float
    longitude:float
    img: str

class RequestHardwareModel(BaseModel):
    cpu: str
    ram: str
    os: str
    kernel: str
    uptime: str

    class Config:
        orm_mode=True
        
class ResponseDataModel(BaseModel):
    id : str
    time : str
    image : str
    status : bool
    latitude : float
    longitude : float
    heading : int
        

class ResponseModel(BaseModel):
    data: ResponseDataModel
    status: str = "success"
    
    class Config:
        orm_mode=True
        
class PutModel(BaseModel):
    id: str
    status: bool
    
    class Config:
        orm_mode=True