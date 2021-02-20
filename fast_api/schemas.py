from pydantic import BaseModel
from datetime import date


class Author(BaseModel):
    name: str
    surname: str

    class Config:
        orm_mode = True


class Category(BaseModel):
    name: str

    class Config:
        orm_mode = True


class Book(BaseModel):
    title: str
    author: Author
    category: Category
    publish_date: date
    rating: int
    type: str
    price: int
    description: str = None

    class Config:
        orm_mode = True
