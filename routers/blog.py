import oauth2

from typing import List

from fastapi import APIRouter
from fastapi import Depends, status, Response

from sqlalchemy.orm import Session

from database import get_db
from repository import blog_r
from schemas import Blog, ShowBlog, User


router = APIRouter()


@router.post('/', status_code=status.HTTP_201_CREATED)
def create(request: Blog, db: Session = Depends(get_db)):
    return blog_r.create(request, db)


@router.get('/', response_model=List[ShowBlog])
def get_all(db: Session = Depends(get_db),
            get_current_user: User = Depends(oauth2.get_current_user)):
    return blog_r.get_all(db)


@router.get('/{_id}', status_code=200, response_model=ShowBlog)
def get_blog(_id: int, response: Response, db: Session = Depends(get_db)):
    return blog_r.show(_id, response, db)


@router.delete('/{_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete(_id: int, db: Session = Depends(get_db)):
    return blog_r.delete(_id, db)


@router.put('/{_id}', status_code=status.HTTP_202_ACCEPTED)
def update(_id: int, db: Session = Depends(get_db)):
    return blog_r.update(_id, db)
