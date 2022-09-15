from fastapi import APIRouter, status, HTTPException

from sqlalchemy.orm import Session, joinedload
from fastapi.params import Depends
from App.database import get_db
from .. import schemas, models
from passlib.context import CryptContext

router = APIRouter(tags=['trainings'], prefix="/training")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.delete('/{training_type}')
def training_delete(training_type, db: Session = Depends(get_db)):
    db.query(models.Trainings).filter(
        models.Trainings.training_type == training_type).delete(synchronize_session=False)
    db.commit()
    return {'training Deleted'}


@router.get('/')
async def get_all_trainings(db: Session = Depends(get_db)):
    """_summary_
       Get a json with all training 
    """
    training = db.query(models.Trainings).all()
    if not training:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail='training not found')
    return training


@router.get('/{training_type}}')
async def get_one_training(training_type, db: Session = Depends(get_db)):
    """_summary_
       Get a json with one training 
    """
    training = db.query(models.Trainings).filter(
        models.Trainings.training_type == training_type).first()
    if not training:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail='training not found')
    return training


@router.get('/get_training_view/{training_type}}', response_model=schemas.Trainings)
async def get_one_training_view(id, db: Session = Depends(get_db)):
    """_summary_
       Get a json with one training 
    """
    training = db.query(models.Trainings).options(joinedload(
        models.Trainings.birds)).filter(models.Trainings.id == id).first()
    if not training:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail='training not found')
    return training


@router.put('/{training_type}')
def update_training(training_type, request: schemas.Trainings, db: Session = Depends(get_db)):
    """_summary_
       Update a json with one training 
    """
    training = db.query(models.Trainings).filter(
        models.Trainings.training_type == training_type)
    if not training.first():
        pass
    if not training:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail='training not found')
    training.update(request.dict())
    db.commit()
    return {'Training updated'}


@router.post('/', response_model=schemas.DisplayTrainings, status_code=status.HTTP_201_CREATED)
def add_training(request: schemas.Trainings, db: Session = Depends(get_db)):
    """_summary_
       Save a json with one training 
    """
    new_training = models.Trainings(
        id=request.id, training_type=request.training_type, reps=request.reps, day=request.day)
    db.add(new_training)
    db.commit()
    db.refresh(new_training)
    return new_training
