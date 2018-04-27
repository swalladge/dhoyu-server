import os

import click
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# create and configure the app
app = Flask(__name__, instance_relative_config=True)

app.config.from_mapping(
    SECRET_KEY='dev',
    SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(app.instance_path, 'db.sqlite3'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

app.config.from_pyfile('config.py', silent=True)

# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass



# a simple page that says hello
@app.route('/hello')
def hello():
    return 'Hello, World!'


# register the db instance
db = SQLAlchemy(app)
from . import models

from . import api
app.register_blueprint(api.bp)

@click.command('init-db')
def init_db_command():
    db.create_all()
    click.echo('Database inited.')


app.cli.add_command(init_db_command)
