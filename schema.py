from pydantic import BaseModel

# 하드웨어에서 보내는 데이터 형태
class RequestModel(BaseModel):
    heading: int
    latitude: float
    longitude:float
    img: str

# 하드웨어 보내는 하드웨어 정보 데이터 형태
class RequestHardwareModel(BaseModel):
    cpu: str
    ram: str
    os: str
    kernel: str
    uptime: str

    class Config:
        orm_mode=True
        
# 프론트엔드로 보내주기 위해 가공한 데이터 형태
class ResponseDataModel(BaseModel):
    id : str
    time : str
    image : str
    status : bool
    latitude : float
    longitude : float
    heading : int
        

# 프론트엔드로 보내는 데이터 형태
class ResponseModel(BaseModel):
    data: ResponseDataModel
    status: str = "success"
    
    class Config:
        orm_mode=True
        
# 프론트엔드에서 스테이터스를 수정하기 위한 요청을 보낼 때 받는 데이터 형태
class PutModel(BaseModel):
    id: str
    status: bool
    
    class Config:
        orm_mode=True
