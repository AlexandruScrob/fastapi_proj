import models

from sqlalchemy.orm import Session

from schemas import Blog
from fastapi import status, HTTPException, Response


def get_all(db: Session):
    return db.query(models.Blog).all()


def create(request: Blog, db: Session):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog


def delete(_id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == _id)

    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Blog with id {_id} not found')

    blog.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


def update(_id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == _id)

    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Blog with id {_id} not found')

    blog.update({'title': 'updated title'})
    db.commit()

    return Response(status_code=status.HTTP_202_ACCEPTED)


def show(_id: int, response: Response, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == _id).first()

    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Blog with the {_id} is not available')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail': f'Blog with the {_id} is not available'}

    return blog
