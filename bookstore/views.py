from flask import Blueprint, render_template

from bookstore import models

main_blueprint = Blueprint('main', __name__)


@main_blueprint.route('/')
def books():
    return render_template('books.html', books=models.Book.query)


@main_blueprint.route('/categories')
def categories():
    return render_template('categories.html', categories=models.Category.query)
