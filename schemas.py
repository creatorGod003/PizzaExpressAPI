from pydantic import BaseModel
from typing import Optional


class SignUpModel(BaseModel):
    id:Optional[int]
    username:str
    email:str
    password:str
    is_staff:Optional[bool]
    is_active:Optional[bool]

    # 
    class Config: 
        orm_mode=True
        schema_extra={
            'example':{
                "username":"johndoe",
                "email":"johndoe@gmail.com",
                "password":"password",
                "is_staff":False,
                "is_active":True
            }
        }

class Settings(BaseModel):
    authjwt_secret_key:str = 'eb642a0ebaf6500e0fc17a7a3e076413d2e2e993a549b8020f683dd9167fb938'

class LoginModel(BaseModel):
    username:str
    password:str
    class Config: 
        schema_extra={
            'example':{
                "username":"johndoe",
                "password":"password",
            }
        }


class OrderModel(BaseModel):
    id:Optional[int]
    quantity:int
    order_status:Optional[str] = "PENDING"
    pizza_size: Optional[str] = "SMALL"
    user_id:Optional[int]
    class Config: 
        orm_mode=True
        schema_extra={
            'example':{
                "quantity":9,
                "pizza_size":"SMALL",
            }
        }


class OrderStatusModel(BaseModel):
    order_status : Optional[str] = "PENDING"

    class Config:
        orm_mode = True
        schema_extra:{
            'example':{
                "order_status":"PENDING"
            }
        }