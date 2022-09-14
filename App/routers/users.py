from fastapi import APIRouter, status, HTTPException
from sqlalchemy.orm import Session
from fastapi.params import Depends
from fastapi_jwt_auth import AuthJWT
from App.database import get_db
from .. import schemas, models


router = APIRouter(tags=['Users'], prefix="/users")


@router.delete('/{id}')
def user_delete_id(id, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")

    current_user = Authorize.get_jwt_subject()
    db.query(models.Users).filter(models.Users.id ==
                                  id).delete(synchronize_session=False)
    db.commit()
    return {'Users deleted': id}


@router.get('/')
async def get_all_users(db: Session = Depends(get_db)):
    """_summary_
       Get a json with all bird 
    """
    users = db.query(models.Users).all()
    return users


@router.get('/{id}')
async def get_one_user(id, db: Session = Depends(get_db)):
    """_summary_
       Get a json with one user 
    """
    user = db.query(models.Users).filter(models.Users.id == id).first()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail='user not found')
    return user


@router.put('/{id}')
def update_user(id, request: schemas.Users, db: Session = Depends(get_db)):
    """_summary_
       Update a json with one user 
    """
    users = db.query(models.Users).filter(models.Users.id == id)
    if not users.first():
        pass
    users.update(request.dict())
    db.commit()
    return {'User updated'}


@router.post('/', status_code=status.HTTP_201_CREATED)
def add_user(request: schemas.Users, db: Session = Depends(get_db)):
    """_summary_
       Save a json with one user 
    """
    new_user = models.Users(name=request.name, first_name=request.first_name,
                            email=request.email, hashed_password=request.hashed_password, admin=False)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return request
