import logging
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_wtf import CSRFProtect
from flask_csp.csp import csp_header
import bcrypt
import database_manager as dbHandler  # Database functions
from SVuser import validate_password, validate_email, sanitise_input, sanitise_email  # Password and email validation function, input sanitization
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flashing messages and CSRF protection
csrf = CSRFProtect(app)

# Set up logging
logging.basicConfig(
    filename="security_log.log",
    filemode='a',  # Append mode
    level=logging.DEBUG,
    format="%(asctime)s %(message)s",
)
app.logger = logging.getLogger(__name__)

# Remove default Flask logger handlers to prevent duplicate logs in the terminal
for handler in app.logger.handlers:
    app.logger.removeHandler(handler)

# Add file handler to Flask logger
file_handler = logging.FileHandler('security_log.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
app.logger.addHandler(file_handler)

@app.route("/index.html", methods=["GET"])
def root():
    return redirect("/", 302)

@app.route("/", methods=['POST', 'GET'], endpoint='login')
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
        try:
            email = request.form['email']
            password = request.form['password']
        except KeyError as e:
            app.logger.error(f"Missing form field: {e}")
            flash('Invalid form submission')
            return redirect(url_for('login'))

        user = dbHandler.checkCredentials(email)
        
        if user:
            app.logger.debug(f"User found: {user}")
            app.logger.debug(f"Entered password: {password}")
            app.logger.debug(f"Stored password: {user['developer_password']}")
            
            # Compare the entered password with the stored password
            if password == user['developer_password']:
                app.logger.debug("Password match")
                session['user_id'] = user['developer_email']
                session['developer_firstName'] = user['developer_firstName']
                session['developer_lastName'] = user['developer_lastName']
                app.logger.debug(f"Session developer_firstName set to: {session['developer_firstName']}")
                app.logger.debug(f"Session developer_lastName set to: {session['developer_lastName']}")
                return redirect(url_for('home'))
            else:
                app.logger.error("Invalid password")
                flash('Invalid credentials')
        else:
            app.logger.error("User not found")
            flash('Invalid credentials')
    
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = sanitise_email(request.form['email'])
        first = sanitise_input(request.form['firstName'])
        last = sanitise_input(request.form['lastName'])
        password = request.form['password']  # Password should not be sanitized
        app.logger.debug(f"Received signup data: email={email}, firstName={first}, lastName={last}, password={password}")
        
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
        
        # Store the plain text password
        dbHandler.insertDetails(email, first, last, password)
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/submit_entry', methods=['POST'])
def submit_entry():
    user_email = session['user_id']
    user_details = dbHandler.get_user_details(user_email)

    developer_firstName = user_details['developer_firstName']
    developer_lastName = user_details['developer_lastName']
    developer_name = f"{developer_firstName} {developer_lastName}"
    app.logger.debug(f"Retrieved developer_name from session: {developer_name}")
    
    project_name = request.form['project_name']
    summary = request.form['summary']
    programming_language = request.form['programming_language']
    time_started = request.form['time_started']
    time_finished = request.form['time_finished']
    description = request.form['description']
    date = datetime.now().strftime('%Y-%m-%d')
    entry_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    developer_email = session['user_id']

    dbHandler.insert_diary_entry(developer_name, project_name, summary, programming_language, time_started, time_finished, description, date, developer_email, entry_timestamp)
    return redirect(url_for('diary'))


@app.route("/privacy.html", methods=["GET"])
def privacy():
    return render_template("/privacy.html", current_route='privacy')

@app.route('/diary')
def diary():
    diary_entries = dbHandler.get_all_diary_entries()
    return render_template('diary.html', diary_entries=diary_entries)

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_email = session['user_id']
    user_details = dbHandler.get_user_details(user_email)
    diary_entries = dbHandler.get_diary_entries(user_email)
    
    return render_template('profile.html', 
                           first_name=user_details['developer_firstName'], 
                           last_name=user_details['developer_lastName'], 
                           email=user_details['developer_email'],
                           diary_entries=diary_entries)

@app.route('/api/diary_entries', methods=['GET'])
def get_diary_entries():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    diary_entries = dbHandler.get_all_diary_entries()
    return jsonify(diary_entries)

# Endpoint for logging CSP violations
@app.route("/csp_report", methods=["POST"])
@csrf.exempt
def csp_report():
    app.logger.critical(request.data.decode())
    return "done"

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)