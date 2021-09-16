import models

from sqlalchemy.orm import Session
from fastapi import status, HTTPException

from hashing import Hash
from schemas import User


def create(request: User, db: Session):
    new_user = models.User(name=request.name, email=request.email,
                           password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def get(_id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == _id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with the {_id} is not available')

    return user
