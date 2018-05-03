
import functools
import json
from datetime import datetime, timedelta

from flask import (abort, g, url_for, request, redirect, Blueprint, jsonify)
import jwt

from .models import User
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
