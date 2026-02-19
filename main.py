from flask import Flask, render_template, session
from flask_bcrypt import Bcrypt
from auth import auth_bp
from marks import marks_bp
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
    return render_template('index.html', user=session.get("user"))

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(marks_bp, url_prefix='/marks')

if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get("PORT", 5000)))