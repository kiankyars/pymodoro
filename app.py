from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required, passwordChecker, formatTime, logout_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///pomodoro.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Renders home page"""
    settings = db.execute('SELECT * FROM settings WHERE id = ?', session['user_id'])[0]
    print(settings)
    return render_template("index.html", settings=settings)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Initialize parameters
        username = request.form.get("username")
        password = request.form.get("password")
        # Ensure username was submitted
        if not username:
            flash('must provide username', 'error')
            return redirect(url_for('login'))
        # Ensure password was submitted
        elif not password:
            flash('must provide password', 'error')
            return redirect(url_for('login'))
        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            flash('invalid username and/or password', 'error')
            return redirect(url_for('login'))
        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        # Sets username
        session['username'] = username
        # Add log entry
        db.execute('INSERT INTO logTable (id, type, time) VALUES(?, ?, ?)', session["user_id"], 'login', formatTime())
        # Welcome user back
        flash(f'Welcome back, {username}', 'info')
        # Redirect user to home page
        return redirect("/")
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        if 'user_id' in session:
            flash('Already logged in!', 'info')
            return redirect(url_for('index'))
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""
    # Add log entry
    db.execute('INSERT INTO logTable (id, type, time) VALUES(?, ?, ?)', session["user_id"], 'logout', formatTime())
    # Forget any user_id
    session.clear()
    # Flashes logout confirmation
    flash(f'You have been successfully logged out', 'info')
    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
@logout_required
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        confirmation = request.form.get('confirmation')
        if not all([username, password, confirmation]):
            flash('All fields must be filled', 'error')
            return redirect(url_for('register'))
        elif password != confirmation:
            flash('Passwords do not match', 'error')
            return redirect(url_for('register'))
        elif not passwordChecker(password, username):
            flash('Password not strong enough, check requirements', 'error')
            return redirect(url_for('register'))
        elif username in [keyValue['username'] for keyValue in db.execute('SELECT username FROM users')]:
            flash('Username already taken', 'error')
            return redirect(url_for('register'))
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, generate_password_hash(password))
        # Query database for username
        id = db.execute("SELECT id FROM users WHERE username = ?", username)
        session["user_id"] = id[0]["id"]
        # Add log entry
        db.execute('INSERT INTO logTable (id, type, time) VALUES(?, ?, ?)', session["user_id"], 'register', formatTime())
        # Add settings
        db.execute('INSERT INTO settings (id) VALUES (?)', session["user_id"])
        # Welcome message
        flash(f'Welcome, {username}', 'info')
        # Redirect user to home page
        return redirect("/")
    elif request.method == "GET":
        return render_template("register.html")


@app.route("/history")
@login_required
def history():
    """Shows the user their log history"""
    logHistory = db.execute('SELECT * FROM logTable WHERE id = ?', session['user_id'])
    return render_template("history.html", history=logHistory)


@app.route("/analysis", methods=["GET"])
@login_required
def analysis():
    """Shows the user their past pymodoro sessions"""
    # analysis = db.execute('SELECT * FROM analysis WHERE id = ?', session['user_id'])
    # return render_template("analysis.html", data=analysis)
    return redirect(url_for('index'))


@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    """Redirects the user to the settings  menu"""
    if request.method == "POST":
        global sound, volume
        colour = request.form.get('colour')
        session["colour"] = colour
        pomodoroLength = request.form.get('pomodoroLength')
        breakLength = request.form.get('breakLength')
        togglePomodoro = request.form.get('pomodoro')
        if togglePomodoro == 'on':
            togglePomodoro = True
        else:
            togglePomodoro = False
        # Changed variable name here since break is a key word
        toggleBreak = request.form.get('break')
        if toggleBreak == 'on':
            toggleBreak = True
        else:
            toggleBreak = False
        darkMode = request.form.get('darkMode')
        if darkMode == 'on':
            darkMode = True
        else:
            darkMode = False
        sound = request.form['alarm']
        volume = request.form.get('volume')
        db.execute('UPDATE settings SET togglePomodoro = ?, darkMode = ?, volume = ?, pomodoroLength = ?, breakLength = ?, colour = ?, alarm = ?, toggleBreak = ? WHERE id = ?', togglePomodoro,darkMode, volume, pomodoroLength, breakLength, colour, sound, toggleBreak, session['user_id'])
        flash('Settings saved!', 'info')
        # Redirect user to settings
        return redirect("/settings")

    elif request.method == "GET":
        settings = db.execute('SELECT * FROM settings WHERE id = ?', session['user_id'])
        alarms = ['casino', 'clock', 'rooster']
        return render_template("settings.html", settings=settings[0], alarms=alarms)