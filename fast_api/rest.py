from fastapi import APIRouter, Depends, status,  HTTPException
from sqlalchemy.orm import Session

from bookstore import models
from bookstore.models import SessionLocal

routeapi = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@routeapi.get('/bookstore')
def index():
    return {'name': 'Bookstore'}


@routeapi.get('/author/all')
def show_all(db: Session = Depends(get_db)):
    author = db.query(models.Author).all()
    return author


@routeapi.get('/author/{author_id}', status_code=200)
def show(author_id, db: Session = Depends(get_db)):
    author = db.query(models.Author).filter(models.Author.id == author_id).first()
    if not author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Author with the id {author_id} in not available')
    return author






