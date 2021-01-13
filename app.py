from flask import Flask
from flask_bootstrap import Bootstrap

from first_app.views import main_blueprint

app = Flask(__name__)
app.register_blueprint(main_blueprint)
Bootstrap(app)


if __name__ == '__main__':
    app.run()

