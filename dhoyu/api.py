import functools
import json
import os
import uuid
from datetime import datetime, timedelta
from pprint import pprint as pp

from flask import (Blueprint, abort, g, jsonify, redirect, request,
                   send_from_directory, url_for)
from werkzeug.utils import secure_filename

import jwt

from . import app, db
from .decorators import token_required
from .models import Game, Image, Language, User

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/token', methods=('POST', ))
def get_token():
    data = request.json

    if data is None:
        abort(400)

    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if not isinstance(username, str) or not username.strip() or not isinstance(password, str):
        abort(401, 'invalid credential data provided')

    # normalize
    username = username.lower().strip()

    user = User.query.filter_by(username=username).first()

    # user doesn't exist
    if not user:
        abort(401)

    # check password
    if not user.check_password(password):
        # oops, was invalid :P
        abort(401)

    expires = datetime.utcnow() + timedelta(weeks=1)

    token = jwt.encode(
        {
            'sub': username,
            'exp': expires,
        },
        app.config['SECRET_KEY'],
        algorithm='HS256', )

    return jsonify({
        'token': token.decode('utf-8'),
    })


@bp.route('/register', methods=('POST', ))
def register():

    data = request.json

    if data is None:
        abort(400)

    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if not isinstance(username, str) or not username.strip() or not isinstance(password, str):
        # TODO: template for sending abort message in json
        abort(401, 'invalid credential data provided')

    # normalize
    username = username.lower().strip()

    if len(username) > 30:
        # TODO: helpful message
        abort(400)

    # TODO: validate username only contains ascii alphanumeric plus `-`, `_`, etc.

    if User.query.filter_by(username=username).first():
        # username already exists
        abort(401)

    user = User(username, password)
    db.session.add(user)
    db.session.commit()

    return jsonify({'msg': 'success'})


@bp.route('/user', methods=('GET', ))
@token_required
def user_info():
    return jsonify(g.user.get_info_dict())


@bp.route('/user/<username>', methods=('GET', ))
@token_required
def other_user_info(username):

    user = User.query.filter_by(username=username).first_or_404()

    return jsonify(user.get_info_dict())


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


def allowed_image_file(f) -> bool:
    filename = f.filename
    ok = True
    if '.' in filename and \
      filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
        pass
    else:
        ok = False

    return ok


@bp.route('/games', methods=('POST', ))
@token_required
def create_game():

    data = request.json
    if data is None:
        abort(400, 'invalid json data')

    # json data shape example
    # {
    #   "images": [{
    #     "data": "base64 encoded blob"
    #   }],
    #   "audio": {
    #     "data": "base64 encoded blob"
    #   },
    #   "word": "epul",
    #   "public": true,
    #   "language": "rop", // language code

    # retrieve and validate data

    images = data.get('images', [])
    if not isinstance(images, list):
        abort(400, 'invalid images list')

    if len(images) > 4:
        abort(400, 'too many images (max 4)')

    word = data.get('word', None)
    if not isinstance(word, str) or not word:
        abort(400, '"word" empty or missing')

    public = bool(data.get('public', False))

    audio = data.get('audio', None)
    # TODO: validate and use audio

    language = data.get('language', None)
    if not isinstance(language, str) or not language:
        abort(400, 'invalid or missing language code')

    # TODO: support more language codes - this isn't part of mvp though
    SUPPORTED_LANGS = ['rop']
    if language not in SUPPORTED_LANGS:
        abort(400, 'unsupported language')

    language = Language.query.filter_by(code=language).first()
    game = Game(word, g.user, language, public)

    # validate stage
    for image in images:
        if not isinstance(image, dict):
            abort(400, 'invalid or rejected image')
        image_data = image.get('data', None)
        if not isinstance(image_data, str) or not image_data:
            abort(400, 'invalid or rejected image')
        # TODO: ensure valid base64 data, validate image, resize/compress (Pillow?)

        # save stage
    for image in images:
        game.images.append(Image(image['data']))

    game.language_id = language.id

    db.session.add(game)
    db.session.commit()

    return jsonify({'msg': 'success'})


# TODO: consider query param or /<language_code>/games style for language filtering support
@bp.route('/games', methods=('GET', ))
@token_required
def list_games():

    # union( public games, author's games)
    games = Game.query.filter(db.or_(Game.public == True, Game.author == g.user))

    return jsonify({
        'games': [
            {
                'id': game.id,
                'word': game.word,
                'public': game.public,
                'language': game.language.name,
                # thumbnail in future?
            }
            for game in games
        ],
    })


@bp.route('/games/<id>', methods=('GET', ))
@token_required
def get_game(id_):

    # TODO: get a game by name/id and return (with attached audio/images)

    return jsonify({'msg': 'success'})
