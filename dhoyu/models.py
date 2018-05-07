import datetime

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

    # scores updated by the server on game completion, game like, upload, etc.
    # future work probably should have extra tables for recording all actions
    # and calculate scores based on that
    learner_score = db.Column(db.Integer, default=0, nullable=False)
    creator_score = db.Column(db.Integer, default=0, nullable=False)
    games_played = db.Column(db.Integer, default=0, nullable=False)
    # games_uploaded can be calculated by count(games where game.author = user)

    saved_games = db.relationship('Game', secondary=game_user_links, lazy='subquery',
            backref=db.backref('players', lazy=True))

    saved_categories = db.relationship('Category', secondary=category_user_links, lazy='subquery',
            backref=db.backref('players', lazy=True))

    created_games = db.relationship('Game', backref='author', lazy='dynamic')
    created_categories = db.relationship('Category', backref='author', lazy='dynamic')

    cards = db.relationship('Card', backref='user', lazy=True)

    def __init__(self, username: str, password: str, admin: bool = False) -> None:
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

    def get_info_dict(self):
        print(type(self.created_games))
        print(self.created_games)
        return {
            'username': self.username,
            'is_admin': self.is_admin,
            'games_played': self.games_played,
            'games_created': self.created_games.count(),
            'learner_score': self.learner_score,
            'creator_score': self.creator_score,
        }


class Language(db.Model):
    __tablename__ = 'languages'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)

    # TODO: language id

    games = db.relationship('Game', backref='language', lazy='dynamic')
    categories = db.relationship('Category', backref='language', lazy='dynamic')

    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        return 'Language({!r})'.format(self.name)


# NOTE: image and audio are 'owned' by the author of the game to which they are
# attached
class Image(db.Model):
    __tablename__ = 'game_images'

    id = db.Column(db.Integer, primary_key=True)

    # can generate url from path
    # XXX: needs to be different schema if hosting images on remote server
    path = db.Column(db.String(512), nullable=False)

    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)

    def __init__(self, path: str):
        self.path = path

    def __repr__(self):
        return 'Image(name={!r})'.format(self.url)


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

    public = db.Column(db.Boolean, default=False, nullable=False)

    # whether the game has been finished editing by the user and ready to be
    # played (if creating a game is a multistep process)
    # ready = db.Column(db.Boolean, default=False, nullable=False)

    images = db.relationship('Image', order_by=Image.id, backref='game', lazy=True)
    audios = db.relationship('Audio', order_by=Audio.id, backref='game', lazy=True)
    flags = db.relationship('Flag', backref='game', lazy=True)

    language_id = db.Column(db.Integer, db.ForeignKey('languages.id'), nullable=False)

    def __init__(self, word: str, author: User, language: Language, public: bool = False):
        self.word = word
        self.author = author
        self.language = language
        self.public = public

    def __repr__(self):
        return 'Game(word={!r})'.format(self.word)


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)

    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    games = db.relationship('Game', secondary=category_game_links, lazy='subquery',
            backref=db.backref('categories', lazy=True))

    language_id = db.Column(db.Integer, db.ForeignKey('languages.id'), nullable=False)

    def __init__(self, name, author, language):
        self.name = name
        self.author = author
        self.language = language

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
    game = db.relationship('Game', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # TODO: include metadata about reviews for SRS purposes

    def __init__(self, user: User, game: Game):
        self.game = game
        self.user = user



class Flag(db.Model):
    '''
    user report on a game
    '''
    __tablename__ = 'flags'

    id = db.Column(db.Integer, primary_key=True)

    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # allows a user to write info on why flagged if necessary
    text = db.Column(db.String(512), default='', nullable=False)

    # date of report
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)

    def __init__(self, user: User, game: Game) -> None:
        self.game = game
        self.user = user


class Like(db.Model):
    '''
    user likes/thumbsup/upvotes for games
    '''
    __tablename__ = 'likes'

    id = db.Column(db.Integer, primary_key=True)

    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # date of like
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)

    def __init__(self, user: User, game: Game) -> None:
        self.game = game
        self.user = user
