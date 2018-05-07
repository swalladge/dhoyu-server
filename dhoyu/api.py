import os
import functools
import json
from datetime import datetime, timedelta
import uuid

from flask import (abort, g, url_for, request, redirect, Blueprint, jsonify,
        send_from_directory)
import jwt
from werkzeug.utils import secure_filename

from .models import User, Game, Image, Language
from . import db, app
from .decorators import token_required

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/token', methods=('POST',))
def get_token():
    data = request.json

    if data is None:
        abort(400)


    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if not username or not password:
        abort(401)

    user = User.query.filter_by(username=username).first()

    # user doesn't exist
    if not user:
        abort(401)

    # check password
    if not user.check_password(password):
        # oops, was invalid :P
        abort(401)

    expires = datetime.utcnow() + timedelta(weeks=1)

    token = jwt.encode({
        'sub': username,
        'exp': expires,
        },
        app.config['SECRET_KEY'],
        algorithm='HS256',
    )

    return jsonify({
        'token': token.decode('utf-8'),
        'expires': int(expires.timestamp()),
    })



@bp.route('/register', methods=('POST',))
def register():

    data = request.json

    if data is None:
        abort(400)


    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if not username or not password:
        abort(400)

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



@bp.route('/user', methods=('GET',))
@token_required
def user_info():
    return jsonify(g.user.get_info_dict())


@bp.route('/user/<username>', methods=('GET',))
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


@bp.route('/games', methods=('POST',))
@token_required
def create_game():

    images = request.files.getlist('images[]') # list of 0 or more FileStorage objects


    if len(images) > 4:
        abort(400, 'too many images (max 4)')

    data = request.form.get('data')
    try:
        data = json.loads(data)
    except Exception as e:
        print(e)
        abort(400, 'invalid json data in "data" attribute of formdata')

    # ok let's do this

    word = data.get('word')
    if not word:
        abort(400, '"word" empty or missing')

    public = bool(data.get('public', False))


    kriol = Language.query.filter_by(name='Kriol').first()

    game = Game(word, g.user, kriol, public)

    # TODO: images

    # validate stage
    for f in images:
        if not allowed_image_file(f):
            abort(400, 'invalid or rejected image')

    # save stage
    for f in images:

        # secure and generate random filename
        filename = secure_filename(f.filename)
        extension = filename.rsplit('.', 1)[1].lower()
        filename = '{}.{}'.format(str(uuid.uuid4()), extension)

        path = os.path.join(app.config['UPLOAD_IMAGES_FOLDER'], filename)
        f.save(path)

        image = Image(filename)
        game.images.append(image)


    db.session.add(game)
    db.session.commit()

    return jsonify({
        'msg': 'success'
        })


@bp.route('/images/<name>', methods=('GET',))
def get_image(name: str):
    return send_from_directory(app.config['UPLOAD_IMAGES_FOLDER'], name)
