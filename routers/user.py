from database import get_db
from fastapi import Depends, APIRouter

from repository import user_r
from schemas import User, ShowUser
from sqlalchemy.orm import Session


router = APIRouter()


@router.post('/', response_model=ShowUser)
def create_user(request: User, db: Session = Depends(get_db)):
    return user_r.create(request, db)


@router.get('/{_id}', status_code=200, response_model=ShowUser)
def get_user(_id: int, db: Session = Depends(get_db)):
    return user_r.get(_id, db)
