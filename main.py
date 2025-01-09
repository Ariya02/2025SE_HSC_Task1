from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import flash
from flask_wtf import CSRFProtect
from flask_csp.csp import csp_header
import logging
import database_manager as dbHandler
from SVuser import validate_password, validate_email, sanitise_input  # Password and email validation function, input sanitization

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
        identifier = sanitise_input(request.form.get('identifier'))
        password = sanitise_input(request.form.get('password'))
        app.logger.debug(f"Login attempt with identifier: {identifier} and password: {password}")
        if not password:
            app.logger.debug("Password is missing")
        user = dbHandler.checkCredentials(identifier, password)
        if user:
            app.logger.debug(f"Login successful for user: {user}")
            return redirect(url_for('home'))
        else:
            app.logger.debug("Login failed: Invalid email/developer ID or password")
            flash('Invalid email/developer ID or password')
    app.logger.debug("Rendering login page")
    return render_template('login.html', current_route='login')


@app.route('/home')
def home():
    app.logger.debug("Rendering home page")
    return render_template('index.html', current_route='home')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = sanitise_input(request.form['email'])
        first = sanitise_input(request.form['firstName'])
        last = sanitise_input(request.form['lastName'])
        password = request.form['password']  # Password not sanitised
        developer_id = sanitise_input(request.form['developerId'])
        app.logger.debug(f"Received signup data: email={email}, firstName={first}, lastName={last}, password={password}, developerId={developer_id}")
        
        # Validate email
        email_error = validate_email(email)
        if email_error:
            flash(email_error)
            return render_template('signup.html', current_route='signup')

        # Validate password
        password_error = validate_password(password)
        if password_error:
            flash(password_error)
            return render_template('signup.html', current_route='signup')
        
        dbHandler.insertDetails(email, first, last, password, developer_id)
        return redirect(url_for('home'))
    return render_template('signup.html', current_route='signup')

@app.route('/submit_entry', methods=['POST'])
def submit_entry():
    if request.method == 'POST':
        project_name = request.form['project_name']
        summary = request.form['summary']
        programming_language = request.form['programming_language']
        time_started = request.form['time_started']
        time_finished = request.form['time_finished']
        description = request.form['description']

        dbHandler.insert_diary_entry(project_name, summary, programming_language, time_started, time_finished, description)

        flash('Entry submitted successfully!')
        return redirect(url_for('home'))

@app.route("/privacy.html", methods=["GET"])
def privacy():
    return render_template("/privacy.html", current_route='privacy')


# Endpoint for logging CSP violations
@app.route("/csp_report", methods=["POST"])
@csrf.exempt
def csp_report():
    app.logger.critical(request.data.decode())
    return "done"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)