from flask import  Blueprint, render_template

main_blueprint = Blueprint('main', __name__)


@main_blueprint.route('/')
def hello_flask():
    return render_template('hello.html')
