from enum import unique
import logging as lg
from typing import List
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from App.database import Base
from sqlalchemy.orm import relationship



class Users(Base):
    lg.info('Class Users')
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    name = Column(String)
    first_name = Column(String)
    email = Column(String)    
    hashed_password = Column(String)       
    admin = Column(String, default=False)    
    height = Column(String, nullable=True)    
    weight = Column(String, nullable=True)      
    trainings = relationship("Trainings", secondary="link")     
    
class Trainings(Base):
    lg.info('Class Tranings')
    __tablename__ = 'trainings'
    id = Column(Integer, primary_key=True, index=True)
    training_type = Column(String)
    reps = Column(String)
    day = Column(String)
    users = relationship("Users", secondary="link") 
    
class Link(Base):
   __tablename__ = 'link'
   user_id = Column(Integer, ForeignKey('users.id'), primary_key = True)
   training_id = Column(Integer, ForeignKey('trainings.id'), primary_key = True)
        