from flask import Flask
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate

from bookstore.views import main_blueprint, login_manager
from bookstore.models import db

app = Flask(__name__)
app.register_blueprint(main_blueprint)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'Fnioz1Cnl2grWSA2MLEbCrBuJjJK0ELB'
db.init_app(app)
Migrate(app, db)
Bootstrap(app)
login_manager.init_app(app)


if __name__ == '__main__':
    app.run(debug=True)

