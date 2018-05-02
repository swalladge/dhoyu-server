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


# register the db instance
db = SQLAlchemy(app)

from .models import User, Game, Card, Audio, Image, Category, Language, Flag, Like

from . import api
app.register_blueprint(api.bp)

@click.command('db-up')
def init_db_command():
    db.create_all()
    click.echo('Database inited.')

@click.command('db-down')
def wipe_db_command():
    db.drop_all()
    click.echo('Database tabled dropped.')

def reset_db():
    db.drop_all()
    db.create_all()

@click.command('db-demo')
def demo_db_command():
    click.echo('wiping db and creating some demo data')

    reset_db()

    # some users, one being admin
    admin1 = User('username1', 'password', admin=True)
    user1 = User('username2', 'password')

    kriol = Language('Kriol')

    # categories
    cat1 = Category('Fruit', user1, kriol)
    cat2 = Category('Random', user1, kriol)


    # some games
    game1 = Game('epul', user1, kriol)
    game1.audios.append(Audio('https://upload.wikimedia.org/wikipedia/commons/9/9a/En-us-apple.ogg'))
    game1.images.append(Image('https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Apple_red_delicius_flower_end.jpg/330px-Apple_red_delicius_flower_end.jpg'))
    game1.images.append(Image('https://upload.wikimedia.org/wikipedia/commons/thumb/f/f4/Honeycrisp.jpg/330px-Honeycrisp.jpg'))
    game1.images.append(Image('https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Discovery_apples.jpg/180px-Discovery_apples.jpg'))

    game2 = Game('binana', admin1, kriol)
    game2.audios.append(Audio('https://upload.wikimedia.org/wikipedia/commons/6/61/En-us-banana.ogg'))
    game2.images.append(Image('https://upload.wikimedia.org/wikipedia/commons/thumb/d/de/Bananavarieties.jpg/330px-Bananavarieties.jpg'))
    game2.images.append(Image('https://upload.wikimedia.org/wikipedia/commons/thumb/9/94/Banana_farm_Chinawal.jpg/255px-Banana_farm_Chinawal.jpg'))
    game2.images.append(Image('https://upload.wikimedia.org/wikipedia/commons/thumb/9/92/Cavendish_DS.jpg/405px-Cavendish_DS.jpg'))


    # add the games to categories
    cat1.games.append(game1)
    cat1.games.append(game2)

    cat2.games.append(game2)

    # add and commit to session so they're all saved
    db.session.add(admin1)
    db.session.add(cat1)
    db.session.commit()



app.cli.add_command(init_db_command)
app.cli.add_command(wipe_db_command)
app.cli.add_command(demo_db_command)
