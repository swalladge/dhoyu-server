# XXX: security risk, only for demo purposes!!!

import sqlite3
import os
from flask import (Blueprint, abort, Response, jsonify)
from werkzeug.exceptions import HTTPException

from . import app

bp = Blueprint('demo', __name__, url_prefix='/demo')

@bp.app_errorhandler(HTTPException)
def error_handler(exception):
    return jsonify({
        'msg': exception.description,
    }), exception.code


# AKA login
@bp.route('/dump.sql', methods=('GET', ))
def get_db_dump():
    '''
    Returns a sql database dump.
    Only works if the default database is used
    '''

    db_path = os.path.join(app.instance_path, 'db.sqlite3')
    conn = sqlite3.connect(db_path)
    dump = '\n'.join(line for line in conn.iterdump())

    res = Response(response=dump, status=200, mimetype="text/plain")
    return res
