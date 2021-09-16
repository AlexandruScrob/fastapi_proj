import models

from database import engine
from fastapi import FastAPI

from routers import user, blog, login

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(login.router,
                   tags=["Authentication"])

app.include_router(user.router,
                   prefix="/user",
                   tags=["User"])

app.include_router(blog.router,
                   prefix="/blog",
                   tags=["Blog"])


@app.get('/')
def root():
    return "Server up"
