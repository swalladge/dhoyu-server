
from . import db

# links between categories and games on that category
category_game_links = db.Table('category_game_links',
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True)
)

# links between categories and users that have saved that category
category_user_links = db.Table('category_user_links',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True)
)

# links between individual games and users that have saved those games
game_user_links = db.Table('game_user_links',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True)
)

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    saved_games = db.relationship('Game', secondary=game_user_links, lazy='subquery',
            backref=db.backref('players', lazy=True))

    saved_categories = db.relationship('Category', secondary=category_user_links, lazy='subquery',
            backref=db.backref('players', lazy=True))

    def __repr__(self):
        return '<User %r>' % self.username



class Image(db.Model):
    __tablename__ = 'game_image'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(512))

    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    game = db.relationship('Game', back_populates='images')

    def __init__(self, url):
        self.url = url

    def __repr__(self):
        return 'Image(url={!r})'.format(self.url)


class Audio(db.Model):
    __tablename__ = 'game_audio'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(512))

    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    game = db.relationship('Game', back_populates='audios')

    def __init__(self, url):
        self.url = url

    def __repr__(self):
        return 'Image(url={!r})'.format(self.url)


class Game(db.Model):
    __tablename__ = 'game'

    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(128))

    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('User', back_populates='created_games')

    images = db.relationship('Image', order_by=Image.id, back_populates='game')
    audios = db.relationship('Audio', order_by=Audio.id, back_populates='game')

    def __init__(self, word):
        self.word = word

    def __repr__(self):
        return 'Game(word={!r})'.format(self.name, self.word)


class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))

    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('User', back_populates='created_categories')

    games = db.relationship('Game', secondary=category_game_links, lazy='subquery',
            backref=db.backref('categories', lazy=True))

    def __init__(self, name, author):
        self.name = name
        self.author = author

    def __repr__(self):
        return 'Course(name={!r})'.format(self.name)

    def add_game(self, game):
        game.course = self
