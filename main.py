from typing import List

import models

from database import engine, SessionLocal
from fastapi import FastAPI, Depends, status, Response, HTTPException

from hashing import Hash
from schemas import Blog, ShowBlog, User, ShowUser
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db

    finally:
        db.close()


@app.get('/')
def root():
    return "Server up"


@app.post('/blog', status_code=status.HTTP_201_CREATED, tags=['blog'])
def create(request: Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog


@app.get('/blog', response_model=List[ShowBlog], tags=['blog'])
def get_all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get('/blog/{_id}', status_code=200, response_model=ShowBlog, tags=['blog'])
def get_blog(_id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == _id).first()

    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Blog with the {_id} is not available')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail': f'Blog with the {_id} is not available'}

    return blog


@app.delete('/blog/{_id}', status_code=status.HTTP_204_NO_CONTENT, tags=['blog'])
def delete(_id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == _id)

    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Blog with id {_id} not found')

    blog.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/blog/{_id}', status_code=status.HTTP_202_ACCEPTED, tags=['blog'])
def update(_id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == _id)

    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Blog with id {_id} not found')

    blog.update({'title': 'updated title'})
    db.commit()

    return Response(status_code=status.HTTP_202_ACCEPTED)


@app.post('/user', response_model=ShowUser, tags=['user'])
def create_user(request: User, db: Session = Depends(get_db)):
    new_user = models.User(name=request.name, email=request.email,
                           password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.get('/user/{_id}', status_code=200, response_model=ShowUser, tags=['user'])
def get_user(_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == _id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with the {_id} is not available')

    return user
