from flask import Flask, render_template, session
from flask_bcrypt import Bcrypt
from auth import auth_bp
from marks import marks_bp
import os, csv
from werkzeug.middleware.proxy_fix import ProxyFix
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.environ.get("MONGO_URI"))
db = client['slushify']

users_collection = db['users']
marks_collection = db['marks']

marks_collection.create_index([("body", "text")])

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "supersecretkey")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_SAMESITE="None"
)
app.config['SESSION_COOKIE_DOMAIN'] = None

bcrypt = Bcrypt(app)

if not os.path.exists("users.csv"):
    with open("users.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["username", "password"])

@app.route('/')
def home():
    return render_template('index.html', user=session.get("user"))

auth_bp.users = users_collection
marks_bp.marks = marks_collection

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(marks_bp, url_prefix='/marks')

if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get("PORT", 5000)), host="0.0.0.0")