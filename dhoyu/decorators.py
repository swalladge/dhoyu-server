
from functools import wraps
import re

from flask import g, request, abort
import jwt

from . import db, app
from .models import User

TOKEN_RE = re.compile(r'^Bearer ([^\s]+)$')

def token_required(f):
    '''
    wraps a route handler function

    if a valid jwt is in the request header, it sets g.user to the corresponding
    User object, otherwise None
    '''
    @wraps(f)
    def decorated(*args, **kwargs):
        authheader = request.headers.get('Authorization', None)
        token = None
        if authheader:
            m = TOKEN_RE.match(authheader)
            if m:
                token = m.group(1)

        if not token:
            # invalid or missing token header
            abort(401, 'JWT is required and was not found')

        try:
            decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms='HS256')
        except Exception as e:
            return abort(401, 'invalid JWT {}'.format(str(e)))

        # from here it's a valid JWT.
        # add these sanity checks in case it's an old jwt with a different
        # format or the user has been deleted
        username = decoded.get('sub', None)
        if not username:
            # no username
            abort(401, 'empty username')

        user = User.query.filter_by(username=username).first()

        if user:
            g.user = user
        else:
            # user not found
            abort(401, 'this username no longer exists')

        # if reached here, then g.user must be a valid User object
        return f(*args, **kwargs)
    return decorated
