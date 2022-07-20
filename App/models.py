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
    password_lost = Column(String)    
    admin = Column(String)    
    height = Column(String)    
    weight = Column(String)    
    localisation = Column(String)    
    sex = Column(String)    
    users = relationship("Exercises", secondary="association_table", back_populates="users")   
    
class Exercises(Base):
    lg.info('Class Exercises')
    __tablename__ = 'exercises'
    id = Column(Integer, primary_key=True, index=True)
    exercice_type = Column(String)
    reps = Column(String)
    day = Column(String)
    birds = relationship("Users", secondary="association_table", back_populates="exercises")   
    
class association_table(Base):
    lg.info('Class Users')
    __tablename__ = 'birds_users'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    exercises_id = Column(Integer, ForeignKey('exercises.id'), primary_key=True)
    

    