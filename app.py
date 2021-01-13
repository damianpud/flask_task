from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)


@app.route('/')
def hello_flask():
    return render_template(
        'hello.html'
    )


if __name__ == '__main__':
    app.run()

