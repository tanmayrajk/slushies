from flask import Blueprint, request, jsonify, render_template
from flask_bcrypt import Bcrypt
from flask import session
import csv

auth_bp = Blueprint('auth', __name__)
bcrypt = Bcrypt()

@auth_bp.route('/signup', methods=['GET','POST'])
def signup():
    users = auth_bp.users
    if request.method == 'GET':
        return render_template('signup.html')
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    existing_user = users.find_one({"username": username})
    if existing_user:
        return jsonify({
            "error": "unoriginal ass mf 🫩",
            "file": "https://raw.githubusercontent.com/tanmayrajk/slushies/refs/heads/main/memes/buzz-lightyear-factory.gif"
        }), 400
    
    users.insert_one({
        "username": username,
        "password": hashed_password
    })
    return jsonify({
        "message": "you a yn now",
        "file": "https://raw.githubusercontent.com/tanmayrajk/slushies/refs/heads/main/memes/bro-is-new.jpg"
    }), 201

@auth_bp.route('/signin', methods=['GET','POST'])
def signin():
    if request.method == 'GET':
        return render_template('signin.html')
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = auth_bp.users.find_one({"username": username})
    if user and bcrypt.check_password_hash(user['password'], password):
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

@auth_bp.route('/signout', methods=['POST'])
def signout():
    session.pop("user", None)
    return jsonify({
        "message": "it-it's not like im gonna miss you or anything... b-baka! >.<",
        "file": "illaddthislater"
    })