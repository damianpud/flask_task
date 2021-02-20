from fastapi import APIRouter, Depends, status,  HTTPException
from sqlalchemy.orm import Session
from typing import List

from bookstore import models
from bookstore.models import SessionLocal
from . import schemas

routeapi = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@routeapi.get('/bookstore', tags=['Bookstore'])
def index():
    return {'name': 'Bookstore'}


@routeapi.get('/author/all', response_model=List[schemas.Author], tags=['Author'])
def show_all_authors(db: Session = Depends(get_db)):
    author = db.query(models.Author).all()
    return author


@routeapi.get('/author/{author_id}', status_code=200, response_model=schemas.Author, tags=['Author'])
def show_author(author_id, db: Session = Depends(get_db)):
    author = db.query(models.Author).filter(models.Author.id == author_id).first()
    if not author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Author with the id {author_id} in not available')
    return author


@routeapi.get('/category/all', response_model=List[schemas.Category], tags=['Category'])
def show_all_categories(db: Session = Depends(get_db)):
    categories = db.query(models.Category).all()
    return categories


@routeapi.get('/category/{category_id}', status_code=200, response_model=schemas.Category, tags=['Category'])
def show_category(category_id, db: Session = Depends(get_db)):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Author with the id {category_id} in not available')
    return category


@routeapi.get('/book/all', response_model=List[schemas.Book], tags=['Book'])
def show_all_books(db: Session = Depends(get_db)):
    books = db.query(models.Book).all()
    return books


@routeapi.get('/book/{book_id}', status_code=200, response_model=schemas.Book, tags=['Book'])
def show_book(book_id, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Author with the id {book_id} in not available')
    return book





