from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import jsonify
from flask import url_for
from flask import flash
import requests
from flask_wtf import CSRFProtect
from flask_csp.csp import csp_header
import logging

import database_manager as dbHandler

# Code snippet for logging a message
# app.logger.critical("message")

app_log = logging.getLogger(__name__)
logging.basicConfig(
    filename="security_log.log",
    encoding="utf-8",
    level=logging.DEBUG,
    format="%(asctime)s %(message)s",
)

# Generate a unique basic 16 key: https://acte.ltd/utils/randomkeygen
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flashing messages and CSRF protection
csrf = CSRFProtect(app)


# Redirect index.html to domain root for consistent UX
@app.route("/index", methods=["GET"])
@app.route("/index.htm", methods=["GET"])
@app.route("/index.asp", methods=["GET"])
@app.route("/index.php", methods=["GET"])
@app.route("/index.html", methods=["GET"])
def root():
    return redirect("/", 302)


@app.route("/", methods=["POST", "GET"])
@csp_header(
    {
        "base-uri": "'self'",
        "default-src": "'self'",
        "style-src": "'self'",
        "script-src": "'self'",
        "img-src": "'self' data:",
        "media-src": "'self'",
        "font-src": "'self'",
        "object-src": "'self'",
        "child-src": "'self'",
        "connect-src": "'self'",
        "worker-src": "'self'",
        "report-uri": "/csp_report",
        "frame-ancestors": "'none'",
        "form-action": "'self'",
        "frame-src": "'none'",
    }
)
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = dbHandler.checkCredentials(email, password)
        if user:
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password')
    return render_template('login.html', current_route='login')


@app.route('/home')
def home():
    return render_template('index.html', current_route='home')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        first = request.form['firstName']
        last = request.form['lastName']
        password = request.form['password']
        developer_id = request.form['developerId']
        app.logger.debug(f"Received signup data: email={email}, firstName={first}, lastName={last}, password={password}, developerId={developer_id}")
        dbHandler.insertDetails(email, first, last, password, developer_id)
        return redirect(url_for('home'))
    return render_template('signup.html', current_route='signup')

@app.route("/privacy.html", methods=["GET"])
def privacy():
    return render_template("/privacy.html", current_route='privacy')


# example CSRF protected form
@app.route("/form.html", methods=["POST", "GET"])
def form():
    if request.method == "POST":
        email = request.form["email"]
        text = request.form["text"]
        return render_template("/form.html")
    else:
        return render_template("/form.html")


# Endpoint for logging CSP violations
@app.route("/csp_report", methods=["POST"])
@csrf.exempt
def csp_report():
    app.logger.critical(request.data.decode())
    return "done"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)