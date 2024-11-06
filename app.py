import json, sqlite3, click, functools, os, hashlib,time, random, sys, secrets
from flask import Flask, current_app, g, session, redirect, render_template, url_for, request
from werkzeug.security import generate_password_hash, check_password_hash
import bleach




### DATABASE FUNCTIONS ###

def connect_db():
    return sqlite3.connect(app.database)

def init_db():
    """Initializes the database with our great SQL schema"""
    conn = connect_db()
    db = conn.cursor()
    db.executescript("""

    DROP TABLE IF EXISTS users;
    DROP TABLE IF EXISTS notes;

    CREATE TABLE notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        assocUser INTEGER NOT NULL,
        dateWritten DATETIME NOT NULL,
        note TEXT NOT NULL,
        publicID INTEGER NOT NULL
    );

    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    );
    """)
    

    db.execute("INSERT INTO users (username, password) VALUES (?, ?);", ("admin", generate_password_hash("password")))
    db.execute("INSERT INTO users (username, password) VALUES (?, ?);", ("bernardo", generate_password_hash("omgMPC")))
    db.execute("INSERT INTO notes (assocUser, dateWritten, note, publicID) VALUES (?, ?, ?, ?);", (2, "1993-09-23 10:10:10", "hello my friend", 1234567890))
    db.execute("INSERT INTO notes (assocUser, dateWritten, note, publicID) VALUES (?, ?, ?, ?);", (2, "1993-09-23 12:10:10", "i want lunch pls", 1234567891))

    conn.commit()
    conn.close()



### APPLICATION SETUP ###
app = Flask(__name__)
app.database = "db.sqlite3"
app.secret_key = os.urandom(32)

app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True
)

ALLOWED_TAGS = ['b', 'i', 'u', 'p', 'br']
ALLOWED_ATTRIBUTES = {}

# Sanitize input function using bleach
def sanitize_input(input_text):
    return bleach.clean(input_text, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES)

### ADMINISTRATOR'S PANEL ###
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return view(**kwargs)
    return wrapped_view

@app.route("/")
def index():
    if not session.get('logged_in'):
        return render_template('index.html')
    else:
        return redirect(url_for('notes'))


@app.route("/notes/", methods=('GET', 'POST'))
@login_required
def notes():
    importerror=""
    #Posting a new note:
    if request.method == 'POST':
        if request.form['submit_button'] == 'add note':
            note = sanitize_input(request.form['noteinput'])
            db = connect_db()
            c = db.cursor()
            statement = """INSERT INTO notes(id,assocUser,dateWritten,note,publicID) VALUES(null,?,?,?,?);"""
            c.execute(statement, (session['userid'], time.strftime('%Y-%m-%d %H:%M:%S'), note, secrets.below(9999999999)))
            db.commit()
            db.close()
        elif request.form['submit_button'] == 'import note':
            noteid = request.form['noteid']
            db = connect_db()
            c = db.cursor()
            statement = """SELECT * from NOTES where publicID = ?"""
            c.execute(statement, (noteid,))
            result = c.fetchall()
            if(len(result)>0):
                row = result[0]
                statement = """INSERT INTO notes(id,assocUser,dateWritten,note,publicID) VALUES(null,?,?,?,?);"""
                c.execute(statement, (session['userid'],row[2],row[3],row[4]))
            else:
                importerror="No such note with that ID!"
            db.commit()
            db.close()
    
    db = connect_db()
    c = db.cursor()
    statement = "SELECT * FROM notes WHERE assocUser = ?;"
    c.execute(statement, (session['userid'],))
    notes = c.fetchall()
    
    return render_template('notes.html',notes=notes,importerror=importerror)


@app.route("/login/", methods=('GET', 'POST'))
def login():
    error = ""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = connect_db()
        c = db.cursor()
        statement = "SELECT id, username, password FROM users WHERE username = ?;"
        c.execute(statement, (username,))
        result = c.fetchone()

        if result and check_password_hash(result[2], password):
            session.clear()
            session['logged_in'] = True
            session['userid'] = result[0]
            session['username']=result[1]
            return redirect(url_for('index'))        
        else:
            error = "Wrong username or password!"
        db.close()
    return render_template('login.html',error=error)


@app.route("/register/", methods=('GET', 'POST'))
def register():
    errored = False
    usererror = ""
    if request.method == 'POST':
        

        username = request.form['username']
        password = request.form['password']
        db = connect_db()
        c = db.cursor()
        statement = """SELECT * FROM users WHERE username = ?;"""

        c.execute(statement, (username,))
        if(len(c.fetchall())>0):
            errored = True
            usererror = "That username is already in use by someone else!"

        if(not errored):
            hashed_password = generate_password_hash(password)
            statement = """INSERT INTO users(id,username,password) VALUES(null,?,?);"""
            c.execute(statement, (username, hashed_password))
            db.commit()
            db.close()
            return redirect(url_for('index'))
        
        db.close()
    return render_template('register.html',usererror=usererror)


@app.route("/logout/")
@login_required
def logout():
    """Logout: clears the session"""
    session.clear()
    return redirect(url_for('index'))

if __name__ == "__main__":
    #create database if it doesn't exist yet
    if not os.path.exists(app.database):
        init_db()
    runport = 5000
    if(len(sys.argv)==2):
        runport = sys.argv[1]
    try:
        app.run(host='0.0.0.0', port=runport) # runs on machine ip address to make it visible on netowrk
    except:
        print("Something went wrong. the usage of the server is either")
        print("'python3 app.py' (to start on port 5000)")
        print("or")
        print("'sudo python3 app.py 80' (to run on any other port)")