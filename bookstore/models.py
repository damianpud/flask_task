from datetime import datetime

from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    books = relationship('Book', back_populates='category')


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(length=128), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    author = relationship('Author', back_populates='author_books')
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = relationship('Category', back_populates='books')
    rating = db.Column(db.Integer, nullable=False)
    publish_date = db.Column(db.Date, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(length=64), nullable=False)
    description = db.Column(db.String)
    created = db.Column(db.DateTime, default=datetime.utcnow)


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=128), nullable=False)
    surname = db.Column(db.String(length=128), nullable=False)
    author_books = relationship('Book', back_populates='author')


engine = create_engine('sqlite:///db.sqlite3')
Session = sessionmaker(autoflush=False, bind=engine)
