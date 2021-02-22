from os import environ as E

from datetime import datetime

from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from flask_sqlalchemy import SQLAlchemy
from flask_security import RoleMixin, UserMixin

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
    cover = db.Column(db.String(length=256))
    created = db.Column(db.DateTime, default=datetime.utcnow)
    order_items = relationship('OrderItems', back_populates='book')


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=128), nullable=False)
    surname = db.Column(db.String(length=128), nullable=False)
    author_books = relationship('Book', back_populates='author')


roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(length=128), nullable=False)
    email = db.Column(db.String(length=128), nullable=False, unique=True)
    password = db.Column(db.String(length=256), unique=True)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    active = db.Column(db.Boolean, default=True)
    personal_data = relationship('PersonalData', back_populates='user')
    order = relationship('Order', back_populates='user')
    order_items = relationship('OrderItems', back_populates='user')
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))


class Role(RoleMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=80), unique=True)
    description = db.Column(db.String(length=255))

    def __str__(self):
        return self.name


class OrderItems(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = relationship('User', back_populates='order_items')
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    book = relationship('Book', back_populates='order_items')
    created = db.Column(db.DateTime, default=datetime.utcnow)
    cart = db.Column(db.Boolean, default=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    order = relationship('Order', back_populates='order_items')


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(length=12), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = relationship('User', back_populates='order')
    created = db.Column(db.DateTime, default=datetime.utcnow)
    paid = db.Column(db.Boolean, default=False)
    send = db.Column(db.Boolean, default=False)
    order_items = relationship('OrderItems', back_populates='order')


class PersonalData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(length=128), nullable=False)
    last_name = db.Column(db.String(length=128), nullable=False)
    address = db.Column(db.String(length=128), nullable=False)
    postal_code = db.Column(db.String(length=20), nullable=False)
    city = db.Column(db.String(length=128), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = relationship('User', back_populates='personal_data')


DB_CONFIG = {
    key: E[f'DB{key}'] for key in ['SCHEMA', 'USER', 'PASS', 'HOST', 'PORT']
}
DB_URI_TEMPLATE = '{SCHEMA}://{USER}:{PASS}@{HOST}:{PORT}'

engine = create_engine(DB_URI_TEMPLATE.format(**DB_CONFIG))
Session = sessionmaker(autoflush=False, bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

