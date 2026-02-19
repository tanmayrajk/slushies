from flask import Blueprint, request, jsonify
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
                return jsonify({
                    "error": "unoriginal ass mf 🫩",
                    "file": "https://raw.githubusercontent.com/tanmayrajk/slushies/refs/heads/main/memes/buzz-lightyear-factory.gif"
                }), 400
    with open('users.csv', 'a', newline='') as userfile:
        writer = csv.writer(userfile)
        writer.writerow([username, hashed_password])
    with open(f'marks_db/{username}.csv', 'w', newline='') as markfile:
        writer = csv.writer(markfile)
        writer.writerow(['id', 'timestamp', 'body'])
    return jsonify({
        "message": "you a yn now",
        "file": "https://raw.githubusercontent.com/tanmayrajk/slushies/refs/heads/main/memes/bro-is-new.jpg"
    }), 201

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
                    return jsonify({
                        "message": "welcome cuh",
                        "file": "https://raw.githubusercontent.com/tanmayrajk/slushies/refs/heads/main/memes/yn.jpg"
                    }), 200
                else:
                    return jsonify({
                        "error": "try that one more time and you getting slimed 😒😒",
                        "file": "https://raw.githubusercontent.com/tanmayrajk/slushies/refs/heads/main/memes/kevinhart.gif"
                    }), 401
