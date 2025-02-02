from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_wtf import CSRFProtect
from flask_csp.csp import csp_header
import logging
import database_manager as dbHandler  # Database functions
from SVuser import validate_password, validate_email, sanitise_input, sanitise_email  # Password and email validation function, input sanitization

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flashing messages and CSRF protection
csrf = CSRFProtect(app)

app_log = logging.getLogger(__name__)
logging.basicConfig(
    filename="security_log.log",
    encoding="utf-8",
    level=logging.DEBUG,
    format="%(asctime)s %(message)s",
)

@app.route("/index.html", methods=["GET"])
def root():
    return redirect("/", 302)

@app.route("/", methods=["POST", "GET"], endpoint='login')
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
        identifier = sanitise_email(request.form.get('identifier'))
        password = sanitise_input(request.form.get('password'))
        app.logger.debug(f"Login attempt with identifier: {identifier} and password: {password}")
        if not password:
            app.logger.debug("Password is missing")
        user = dbHandler.checkCredentials(identifier, password)
        if user:
            session['developer_id'] = user[0]  
            app.logger.debug(f"Login successful for user: {user}")
            return redirect(url_for('home'))
        else:
            app.logger.debug("Login failed: Invalid email/developer ID or password")
            flash('Invalid email/developer ID or password')
    app.logger.debug("Rendering login page")
    return render_template('login.html', current_route='login')

@app.route('/home')
def home():
    app.logger.debug("Fetching all diary entries")
    diary_entries = dbHandler.get_all_diary_entries()
    app.logger.debug(f"Diary entries fetched: {diary_entries}")
    return render_template('index.html', current_route='home', diary_entries=diary_entries)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = sanitise_email(request.form['email'])
        first = sanitise_input(request.form['firstName'])
        last = sanitise_input(request.form['lastName'])
        password = validate_password(request.form['password'] ) #Validates the password
        developer_id = request.form['developerId']
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
        developer_id = request.form['developer_id']  # Get developer ID from form
        project_name = sanitise_input(request.form['project_name'])
        summary = sanitise_input(request.form['summary'])
        programming_language = request.form['programming_language']
        time_started = request.form['time_started']
        time_finished = request.form['time_finished']
        description = sanitise_input(request.form['description'])
        date = request.form.get('date')  # Get date from form

        dbHandler.insert_diary_entry(developer_id, project_name, summary, programming_language, time_started, time_finished, description, date)

        flash('Entry submitted successfully!')
        return redirect(url_for('diary'))

@app.route("/privacy.html", methods=["GET"])
def privacy():
    return render_template("/privacy.html", current_route='privacy')

@app.route('/diary')
def diary():
    diary_entries = dbHandler.get_all_diary_entries()
    return render_template('diary.html', diary_entries=diary_entries)

# Endpoint for logging CSP violations
@app.route("/csp_report", methods=["POST"])
@csrf.exempt
def csp_report():
    app.logger.critical(request.data.decode())
    return "done"

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)