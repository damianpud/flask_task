from datetime import date

from flask_wtf import FlaskForm
from flask_wtf.form import _Auto
from wtforms import (
    DateField, IntegerField, SelectField, StringField, ValidationError, SubmitField
)
from wtforms.validators import DataRequired, Length, NumberRange

from bookstore.models import Author, Category, Book


class AuthorForm(FlaskForm):

    name = StringField()
    surname = StringField()

