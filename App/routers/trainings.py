from fastapi import APIRouter, status, HTTPException

from sqlalchemy.orm import Session, joinedload
from fastapi.params import Depends
from App.database import get_db
from .. import schemas, models
from passlib.context import CryptContext

router = APIRouter(tags=['trainings'], prefix="/training")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.delete('/{id}')
def training_delete(id, db: Session = Depends(get_db)):
    db.query(models.Trainings).filter(models.Trainings.id == id).delete(synchronize_session=False)
    db.commit()
    return {'training Deleted'}

@router.get('/')
async def get_all_trainings(db: Session = Depends(get_db)):
    """_summary_
       Get a json with all training 
    """
    training = db.query(models.Trainings).all()
    if not training:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail='training not found')
    return training


@router.get('/{id}}')
async def get_one_training(id, db: Session = Depends(get_db)):
    """_summary_
       Get a json with one training 
    """
    training = db.query(models.Trainings).filter(models.Trainings.id == id).first()
    if not training:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail='training not found')
    return training

@router.get('/get_training_view/{id}}', response_model=schemas.Trainings)
async def get_one_training_view(id, db: Session = Depends(get_db)):
    """_summary_
       Get a json with one training 
    """
    training = db.query(models.Trainings).options(joinedload(models.Trainings.birds)).filter(models.Trainings.id == id).first()
    if not training:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail='training not found')
    return training


@router.put('/{id}')
def update_training(id, request : schemas.Trainings, db: Session = Depends(get_db)):
    """_summary_
       Update a json with one training 
    """
    training = db.query(models.Trainings).filter(models.Trainings.id == id)
    if not training.first():
        pass
    if not training:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail='training not found')
    training.update(request.dict())
    db.commit()    
    return {'bird updated'}


@router.post('/', response_model=schemas.DisplayTrainings ,status_code=status.HTTP_201_CREATED)
def add_training(request : schemas.Trainings, db: Session = Depends(get_db)):
    """_summary_
       Save a json with one training 
    """
    hashed_password = pwd_context.hash(request.hashed_password)
    new_training = models.Trainings(first_name=request.first_name, last_name=request.last_name, trainingname=request.trainingname, email=request.email, hashed_password=hashed_password, password_lost=request.password_lost,
                           admin=request.admin)
    db.add(new_training)
    db.commit()
    db.refresh(new_training)
    return new_training

