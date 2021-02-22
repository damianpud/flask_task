from os import environ as E

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_uploads import configure_uploads
import click
from click_params import EMAIL
from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
import uvicorn

from bookstore.views import main_blueprint, login_manager, admin, create_superuser, images
from bookstore.models import db
from fast_api.rest import routeapi

DB_CONFIG = {
    key: E[f'DB{key}'] for key in ['SCHEMA', 'USER', 'PASS', 'HOST', 'PORT']
}
DB_URI_TEMPLATE = '{SCHEMA}://{USER}:{PASS}@{HOST}:{PORT}'

app = Flask(__name__)
app.register_blueprint(main_blueprint)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI_TEMPLATE.format(**DB_CONFIG)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'Fnioz1Cnl2grWSA2MLEbCrBuJjJK0ELB'
app.config['UPLOADED_IMAGES_DEST'] = 'static/media'
admin.init_app(app)
db.init_app(app)
Migrate(app, db)
Bootstrap(app)
login_manager.init_app(app)
configure_uploads(app, images)

fast_app = FastAPI()
fast_app.include_router(routeapi)
fast_app.mount("/", WSGIMiddleware(app))

_CREATE_SUPERUSER_HELP = (
    'Create superuser account.'
)


@app.cli.command('createsuperuser', help=_CREATE_SUPERUSER_HELP)
@click.option('--username', prompt=True)
@click.option('--email', prompt=True, type=EMAIL)
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True)
def create_superuser_command(username, email, password):
    create_superuser(username, email, password)


@app.cli.command('autocreatesuperuser')
def create_superuser_command():
    create_superuser('admin', 'admin@admin.com', 'password')


if __name__ == '__main__':
    uvicorn.run("app:fast_app")

