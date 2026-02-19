from flask import Flask, render_template, session
from flask_bcrypt import Bcrypt
from auth import auth_bp
from marks import marks_bp
import os, csv
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.secret_key = 'crazy?iwascrazyonce.theylockedmeinaroom.arubberroom.arubberroomwithrats.andratsmakemecrazy.'
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

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(marks_bp, url_prefix='/marks')

if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get("PORT", 5000)), host="0.0.0.0")