from dataclasses import Field
import logging as lg
from pydantic import BaseModel, Field
from typing import List
from fastapi_jwt_auth import AuthJWT

class Settings(BaseModel):
    authjwt_secret_key :str = 'bbf7959edfdc5fa450632afd936e45782be6f5aae8a0ed2ae9cb6c4a34735f56'
    
@AuthJWT.load_config
def get_confgi():
    return Settings()

class Users(BaseModel):
    lg.info('Class Users')
    id : int
    name : str = Field(example="John")
    first_name : str = Field(example="John")
    email : str = Field(example="gsoulat31@gmail.com")
    hashed_password : str
    admin : bool = False
    
    
class Trainings(BaseModel):
    lg.info('Class Trainings')
    __tablename__ = 'Trainings'
    id : int
    exercice_type : str = Field(example ="Pushups")
    reps : str = Field(example = "10")
    day : datetime
    
    
    
class UserLogin(BaseModel): 
    email : str = Field(example="gsoulat31@gmail.com")
    hashed_password : str = Field(example="devine") 
    
    class Config:
        schema_extra={
            "exemple": {
                "email": "gsoulat31@gmail.com",
                "password": "password"
            }
        }

class DisplayUsers(BaseModel):
    first_name : str 
    last_name : str
    email : str
    
    class Config:
        orm_mode = True
        
class DisplayTrainings(BaseModel):
    training_type : str
    reps: str
    day : datetime
    
    class Config:
        orm_mode = True
         
class UserInDB(Users):
    hashed_password: str
