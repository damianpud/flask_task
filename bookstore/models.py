from datetime import datetime

from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.sql.functions import concat

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=128), nullable=False)
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
    description = db.Column(db.String(length=5000))
    created = db.Column(db.DateTime, default=datetime.utcnow)
    order = relationship('Order', back_populates='book')


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=128), nullable=False)
    surname = db.Column(db.String(length=128), nullable=False)
    author_books = relationship('Book', back_populates='author')


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(length=128), nullable=False)
    email = db.Column(db.String(length=128), nullable=False, unique=True)
    password = db.Column(db.String(length=256), unique=True)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    order = relationship('Order', back_populates='user')


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(length=12), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = relationship('User', back_populates='order')
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    book = relationship('Book', back_populates='order')
    created = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(length=128), nullable=False)


engine = create_engine('sqlite:///db.sqlite3')
Session = sessionmaker(autoflush=False, bind=engine)
