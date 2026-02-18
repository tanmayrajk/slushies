from flask import Flask
from flask_bcrypt import Bcrypt
from auth import auth_bp
import os, csv

app = Flask(__name__)
app.secret_key = 'crazy?iwascrazyonce.theylockedmeinaroom.arubberroom.arubberroomwithrats.andratsmakemecrazy.'

bcrypt = Bcrypt(app)

if not os.path.exists("users.csv"):
    with open("users.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["username", "password"])

@app.route('/')
def home():
    return 'hello world'

app.register_blueprint(auth_bp, url_prefix='/auth')

if __name__ == '__main__':
    app.run(debug=True)