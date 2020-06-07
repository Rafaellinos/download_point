# -*- config:utf-8 -*-

from flask import Flask, request, jsonify, send_file, make_response
import jwt
from datetime import datetime, timedelta

from os import listdir, stat
from os.path import isfile, join
from functools import wraps

from models.models import User
from models.db import db

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config.Dev')

PATH_DOCUMENTS = app.config['DOCUMENTS_FOLDER']  # TODO GIVE THE FULL PATH
DATE_PATTERN = app.config['DATE_PATTERN']

@app.before_first_request
def init_db():
    db.create_all()


def token_required(f):
    @wraps(f)
    def decorated(*args, **kw):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        else:
            return jsonify({'message': 'Token is missing'}), 403

        if not token:
            return jsonify({'message': 'Token is missing'}), 403

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.search(public_id=data['public_id'])
        except:
            return jsonify({'message': 'Token is invalid'}), 403

        return f(current_user, *args, **kw)

    return decorated


def bytes_to_human(num, suffix='B'):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def seconds_to_datetime(seconds):
    return datetime.fromtimestamp(seconds).strftime(DATE_PATTERN)


@app.route('/files', methods=['GET'])
@token_required
def main_page(current_user):
    app.logger.info("getting content in the folder")
    files = [f for f in listdir(PATH_DOCUMENTS) if isfile(join(PATH_DOCUMENTS, f))]
    formatted_files = []
    for file in files:
        desc = stat(PATH_DOCUMENTS + '/' + file)
        file_description = {
            'name': file,
            # 'create_date': desc.st_birthtime,
            'last_modification': seconds_to_datetime(desc.st_mtime),
            'type': file.split('.')[-1] if '.' in file else "",
            'size': bytes_to_human(desc.st_size)
        }
        formatted_files.append(file_description)

    return jsonify(formatted_files), 200


@app.route('/download/<filename>', methods=['GET'])
@token_required
def download(current_user, filename):
    app.logger.info("checking is file exists")
    file = PATH_DOCUMENTS + '/' + filename
    if isfile(file):
        return send_file(file, as_attachment=True)
    return jsonify({'message': 'File not found :('}), 404


@app.route('/user/<public_id>', methods=['GET'])
@token_required
def get_user(current_user, public_id=None):
    user = User.search(public_id=public_id)
    if not user:
        return {'message': "Not found :("}, 404
    return jsonify({'user': {
        'login': user.login,
        'public_id': user.public_id,
        'admin': user.admin
    }}), 200


@app.route('/user', methods=['GET'])
@token_required
def get_users(current_user):
    
    if not current_user.admin:
        return {'message': "You don't have permission!"}, 403
    users = User.search()
    if not users:
        return {'message': 'The are no users in the server :('}, 404
    data = list()
    for user in users:
        data.append({
            'login': user.login,
            'public_id': user.public_id,
            'admin': user.admin
        })
    return jsonify({'users': data}), 200


@app.route('/user', methods=['POST'])
def post_user():
    
    data = request.get_json()

    try:
        login = data.get('login')
        password = data.get('password')
    except AttributeError:
        return {'message': 'Content not found :('}, 500

    if not login and not password:
        return {'message': "Field login or passowrd is required!"}, 404
    
    exists = User.search(login=login)
    if exists:
        return {'message': "User already exists!"}, 404
    
    user_model = User(
        login=login,
        password=password)
    new_id = user_model.do_commit()

    return {'message': 'User created successfully!. Your id is: %s' % new_id}, 201


@app.route('/user/<public_id>', methods=['PUT'])
def put_user(public_id=None):
    user = User.search(public_id=public_id)

    if not user:
        return {'message': "Not found :("}, 404
    try:
        for k, v in request.form.items():
            setattr(user, k, v)
        user.do_commit()

    except Exception as err:
        app.logger.error(str(err))
        return {"message": "internal error"}, 500

    return {"message": "User updated!"}, 200


@app.route('/user/<public_id>', methods=['DELETE'])
@token_required
def delete_user(current_user, public_id=None):
    user = User.search(public_id=public_id)
    if not user:
        return {'message': 'user not found :('}, 404
    if not current_user.admin:
        return {'message': 'You do not have permission to do that :('}, 403
    try:
        user.unlink()
    except Exception as err:
        app.logger.error(str(err))
        return {"message": 'internal error'}, 500


@app.route('/login')
def login():
    auth = request.authorization

    if not auth or not all([auth.password, auth.username]):
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

    user = User.search(login=auth.username)
    if not user:
        return {"message": "User not fount!"}, 404

    check = User.check_password(user, auth.password)
    if not check:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

    token = jwt.encode({'public_id': user.public_id,
                        'exp': datetime.utcnow() + timedelta(minutes=30)},
                       app.config['SECRET_KEY'])

    return jsonify({'token': token.decode('UTF-8')}), 200


if __name__ == '__main__':
    db.init_app(app)
    app.run(host=app.config['HOST'])
