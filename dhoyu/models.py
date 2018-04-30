
from passlib.hash import pbkdf2_sha256

from . import db

# links between categories and games on that category
category_game_links = db.Table('category_game_links',
    db.Column('game_id', db.Integer, db.ForeignKey('games.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('categories.id'), primary_key=True)
)

# links between categories and users that have saved that category
category_user_links = db.Table('category_user_links',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('categories.id'), primary_key=True)
)

# links between individual games and users that have saved those games
game_user_links = db.Table('game_user_links',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('game_id', db.Integer, db.ForeignKey('games.id'), primary_key=True)
)



class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    saved_games = db.relationship('Game', secondary=game_user_links, lazy='subquery',
            backref=db.backref('players', lazy=True))

    saved_categories = db.relationship('Category', secondary=category_user_links, lazy='subquery',
            backref=db.backref('players', lazy=True))

    created_games = db.relationship('Game', backref='author', lazy=True)
    created_categories = db.relationship('Category', backref='author', lazy=True)

    cards = db.relationship('Card', backref='user', lazy=True)

    def __init__(self, username: str, password: str, admin: bool = False):
        self.username = username
        self.password = User.hash_password(password)
        self.is_admin = admin

    @staticmethod
    def hash_password(password: str) -> str:
        return pbkdf2_sha256.hash(password)

    def set_password(self, password: str) -> None:
        self.password = User.hash_password(password)

    def check_password(self, password: str) -> bool:
        '''
        checks password against own password hash
        returns True if password correct, otherwise False
        '''
        return pbkdf2_sha256.verify(password, self.password)

    def __repr__(self):
        return 'User({!r})'.format(self.username)


class Image(db.Model):
    __tablename__ = 'game_images'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(512), nullable=False)

    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)

    def __init__(self, url: str):
        self.url = url

    def __repr__(self):
        return 'Image(url={!r})'.format(self.url)


class Audio(db.Model):
    __tablename__ = 'game_audios'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(512), nullable=False)

    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)

    def __init__(self, url: str):
        self.url = url

    def __repr__(self):
        return 'Image(url={!r})'.format(self.url)


class Game(db.Model):
    __tablename__ = 'games'

    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(128), nullable=False)

    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    images = db.relationship('Image', order_by=Image.id, backref='game', lazy=True)
    audios = db.relationship('Audio', order_by=Audio.id, backref='game', lazy=True)

    def __init__(self, word: str, author: User):
        self.word = word
        self.author = author

    def __repr__(self):
        return 'Game(word={!r})'.format(self.word)


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)

    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    games = db.relationship('Game', secondary=category_game_links, lazy='subquery',
            backref=db.backref('categories', lazy=True))

    def __init__(self, name, author):
        self.name = name
        self.author = author

    def __repr__(self):
        return 'Course(name={!r})'.format(self.name)

    def add_game(self, game):
        game.course = self


class Card(db.Model):
    '''
    Go-between to hold information about a game that a user is learning.
    Holds information about the number of reviews, when due next, game/word
    learnt status, etc.
    '''
    __tablename__ = 'cards'

    id = db.Column(db.Integer, primary_key=True)

    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)
    game = db.relationship('Game')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # TODO: include metadata about reviews for SRS purposes

    def __init__(self, user: User, game: Game):
        self.game = game
        self.user = user

