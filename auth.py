from flask import Blueprint, request
from flask_bcrypt import Bcrypt
from flask import session
import csv

auth_bp = Blueprint('auth', __name__)
bcrypt = Bcrypt()

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    with open('users.csv', 'r') as userfile:
        reader = csv.DictReader(userfile)
        for row in reader:
            if row['username'] == username:
                return 'username already exists', 400
    with open('users.csv', 'a', newline='') as userfile:
        writer = csv.writer(userfile)
        writer.writerow([username, hashed_password])
    return 'user registered successfully', 201

@auth_bp.route('/signin', methods=['POST'])
def signin():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    with open('users.csv', 'r') as userfile:
        reader = csv.DictReader(userfile)
        for row in reader:
            if row['username'] == username:
                if bcrypt.check_password_hash(row['password'], password):
                    session["user"] = username
                    return 'logged in successfully', 200
                else:
                    return 'invalid credentials', 401
