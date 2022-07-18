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
    identifiant : str
    nom : str = Field(example="John")
    prenom : str = Field(example="John")
    email : str = Field(example="gsoulat31@gmail.com")
    hashed_password : str
    password_lost : str = Field(example="Oh tu as perdu ton mot de passe ? c'est pas grave")
    admin : bool = False  
    taille : str = Field(example= "170")
    poids : str = Field(example= "75")
    localisation : str = Field(example='https://www.oiseaux.net/maps/images/accenteur.a.gorge.noire.1.200.w.png')
    sexe : str = Field(example="Homme")
    
    
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
    username : str
    email : str
    
    class Config:
        orm_mode = True
         
class UserInDB(Users):
    hashed_password: str