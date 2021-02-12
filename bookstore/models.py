from datetime import datetime

from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

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
    order = relationship('Order', back_populates='book')


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
    order = relationship('Order', back_populates='user')
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))


class Role(RoleMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=80), unique=True)
    description = db.Column(db.String(length=255))

    def __str__(self):
        return self.name


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
