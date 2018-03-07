from flask import flash, request, session, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from config import app_config

import jwt
import datetime
import uuid
from . import auth
from ..models import User
from app import create_app


# Set var to check user login status
global logged_in
logged_in = False

app = create_app(config_name='development')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    data = request.get_json()
    # Check if email already registred
    users_dict = User.users.items()
    existing_user = {k:v for k, v in users_dict if data['email'] in v['email']}
    if existing_user:
        return jsonify({'message':'This email is registered, login instead'}), 404


    # If email not registred, create user account
    new_user = User(email=data['email'], username=data['username'], password=data['password'])
    new_user.create_user()

    for key, value in users_dict:     # user gets id, eg 3
        if data['email'] in value['email']:
            session['user_id'] = key

    return jsonify({'message' : 'New user Succesfully created'}), 201


#user_id=str(uuid.uuid4()),

@auth.route('/login', methods=['GET', 'POST'])
def login():
    data = request.get_json()

    users_dict = User.users.items()
    existing_user = {ke:va for ke, va in users_dict if data['email'] in va['email']}
    if existing_user:
        valid_user = [va for va in existing_user.values() if check_password_hash(va
                        ['password'], data['password'])]
        if valid_user:
            global logged_in
            logged_in = True

            for key, value in users_dict:     # user gets id, eg 3
                if data['email'] in value['email']:
                    session['user_id'] = key
            token = jwt.encode({'email':data['email'], 'exp': datetime.datetime.utcnow()+
                                datetime.timedelta(minutes=15)}, app.config['SECRET_KEY'])
            return jsonify({'message' : 'User valid and succesfully logged in','token': token.decode('UTF-8')}), 200 #

        else:
            return jsonify({'message': 'Wrong password'}), 403

    else:
        return jsonify({'message': 'Not registered user'}), 400

@auth.route('/logout')
def logout():
    global logged_in
    logged_in = False

    session.pop('user_id', None)

    return jsonify({'message' : 'Succesfully logged out'}), 200