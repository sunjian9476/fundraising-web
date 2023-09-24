import datetime

from flask import Blueprint
from flask import session, request, jsonify, redirect, render_template

import data_layer
from models import User

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if data_layer.is_valid_credentials(username, password):
        user = data_layer.get_user(username)
        session['user_id'] = user.id
        return jsonify({'success': True})

    return jsonify({'error': 'invalid username or password'})


@auth.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('password-confirm')

    if password != confirm_password:
        return jsonify({'error': 'password should be the same!'})

    # Validate input

    if data_layer.get_user(username):
        return jsonify({'error': 'Username already exists'})

    # Create User object
    user = User(0, username, password, email, name, datetime.datetime.now())

    # Call data layer method
    if not data_layer.register_user(user):
        return jsonify({'error': 'Error registering user'})

    return jsonify({'success': True})
