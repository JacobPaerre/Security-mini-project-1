import sqlite3, functools, os,time, sys, secrets
from flask import Flask, current_app, g, jsonify, session, redirect, render_template, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash




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
    

    db.execute("INSERT INTO users (username, password) VALUES (?, ?);", ("admin", generate_password_hash("st0rTRexRawr!")))
    db.execute("INSERT INTO users (username, password) VALUES (?, ?);", ("bernardo", generate_password_hash("NatalieElskerKage")))
    db.execute("INSERT INTO notes (assocUser, dateWritten, note, publicID) VALUES (?, ?, ?, ?);", (2, "1993-09-23 10:10:10", "hello my friend", 1234567890))
    db.execute("INSERT INTO notes (assocUser, dateWritten, note, publicID) VALUES (?, ?, ?, ?);", (2, "1993-09-23 12:10:10", "i want lunch pls", 1234567891))
    db.execute("INSERT INTO notes (assocUser, dateWritten, note, publicID) VALUES (?, ?, ?, ?);", (2, "1993-09-23 10:20:15", "This is a confidential note with the password hidden securely", 1234567892))
    db.execute("INSERT INTO notes (assocUser, dateWritten, note, publicID) VALUES (?, ?, ?, ?);", (2, "1993-09-23 11:30:45", "My secret notes include sensitive credentials", 1234567893))
    db.execute("INSERT INTO notes (assocUser, dateWritten, note, publicID) VALUES (?, ?, ?, ?);", (2, "1993-09-23 12:00:00", "Storing password securely within hidden files", 1234567894))
    db.execute("INSERT INTO notes (assocUser, dateWritten, note, publicID) VALUES (?, ?, ?, ?);", (2, "1993-09-23 12:30:30", "These credentials should remain confidential", 1234567895))
    db.execute("INSERT INTO notes (assocUser, dateWritten, note, publicID) VALUES (?, ?, ?, ?);", (2, "1993-09-23 13:10:15", "Please check the secret notes for password details", 1234567896))
    db.execute("INSERT INTO notes (assocUser, dateWritten, note, publicID) VALUES (?, ?, ?, ?);", (1, "1993-09-23 14:00:00", "Do not share these credentials with MRDATA", 9356))
    db.execute("INSERT INTO notes (assocUser, dateWritten, note, publicID) VALUES (?, ?, ?, ?);", (2, "1993-09-23 14:45:10", "Ensure all sensitive passwords are encrypted", 1234567898))
    db.execute("INSERT INTO notes (assocUser, dateWritten, note, publicID) VALUES (?, ?, ?, ?);", (2, "1993-09-23 15:15:20", "Just uncover locked entries marked as not disclosed.", 1234567899))
    db.execute("INSERT INTO notes (assocUser, dateWritten, note, publicID) VALUES (?, ?, ?, ?);", (2, "1993-09-23 16:25:30", "My private notes include the main password", 1234567900))
    db.execute("INSERT INTO notes (assocUser, dateWritten, note, publicID) VALUES (?, ?, ?, ?);", (2, "1993-09-23 17:40:50", "These are secret credentials for internal use", 1234567901))
    db.execute("INSERT INTO notes (assocUser, dateWritten, note, publicID) VALUES (?, ?, ?, ?);", (2, "1993-09-23 18:00:10", "Secure all notes containing sensitive information", 1234567902))
    db.execute("INSERT INTO notes (assocUser, dateWritten, note, publicID) VALUES (?, ?, ?, ?);", (2, "1993-09-23 18:30:30", "Password and credentials must be kept secure", 1234567903))
    db.execute("INSERT INTO notes (assocUser, dateWritten, note, publicID) VALUES (?, ?, ?, ?);", (2, "1993-09-23 19:20:15", "This document contains secret notes and login credentials", 1234567904))
    db.execute("INSERT INTO notes (assocUser, dateWritten, note, publicID) VALUES (?, ?, ?, ?);", (2, "1993-09-23 20:15:50", "Handle the password data with extreme caution", 1234567905))
    db.execute("INSERT INTO notes (assocUser, dateWritten, note, publicID) VALUES (?, ?, ?, ?);", (2, "1993-09-23 21:00:00", "The username is the last letter of the words in one note that is not like the others", 1234567906))
    db.execute("INSERT INTO notes (assocUser, dateWritten, note, publicID) VALUES (?, ?, ?, ?);", (2, "1993-09-23 21:30:30", "All credentials are saved in the secure notes", 1234567907))
    db.execute("INSERT INTO notes (assocUser, dateWritten, note, publicID) VALUES (?, ?, ?, ?);", (2, "1993-09-23 22:10:00", "Password is stored in confidential notes section", 1234567908))
    db.execute("INSERT INTO notes (assocUser, dateWritten, note, publicID) VALUES (?, ?, ?, ?);", (2, "1993-09-23 23:00:00", "Secret credentials are stored securely", 1234567909))
    db.execute("INSERT INTO notes (assocUser, dateWritten, note, publicID) VALUES (?, ?, ?, ?);", (2, "1993-09-24 00:00:00", "Please keep the password confidential", 1234567910))
    db.execute("INSERT INTO notes (assocUser, dateWritten, note, publicID) VALUES (?, ?, ?, ?);", (2, "1993-09-24 01:15:10", "Credentials are in the hidden notes section", 1234567911))
    db.execute("INSERT INTO notes (assocUser, dateWritten, note, publicID) VALUES (?, ?, ?, ?);", (2, "1993-09-24 02:00:00", "All passwords should be kept in secret notes", 1234567912))
    db.execute("INSERT INTO notes (assocUser, dateWritten, note, publicID) VALUES (?, ?, ?, ?);", (2, "1993-09-24 03:30:00", "Sensitive information including credentials is saved here", 1234567913))
    db.execute("INSERT INTO notes (assocUser, dateWritten, note, publicID) VALUES (?, ?, ?, ?);", (2, "1993-09-24 04:20:15", "Hej Frederik, du er på rette spor", 1234567914))
    db.execute("INSERT INTO notes (assocUser, dateWritten, note, publicID) VALUES (?, ?, ?, ?);", (2, "1993-09-24 05:10:10", "Refer to secret notes for password info", 1234567915))
    db.execute("INSERT INTO notes (assocUser, dateWritten, note, publicID) VALUES (?, ?, ?, ?);", (2, "1993-09-24 06:15:10", "The password is the first letter of the words in notes 1234567919 and 1234567899", 1234567916))
    db.execute("INSERT INTO notes (assocUser, dateWritten, note, publicID) VALUES (?, ?, ?, ?);", (2, "1993-09-24 06:15:10", "Sensitive credentials should remain in secure files", 1234567916))
    db.execute("INSERT INTO notes (assocUser, dateWritten, note, publicID) VALUES (?, ?, ?, ?);", (2, "1993-09-24 07:25:00", "The password is located in hidden notes", 1234567917))
    db.execute("INSERT INTO notes (assocUser, dateWritten, note, publicID) VALUES (?, ?, ?, ?);", (2, "1993-09-24 08:35:00", "Only authorized personnel should access these credentials", 1234567918))
    db.execute("INSERT INTO notes (assocUser, dateWritten, note, publicID) VALUES (?, ?, ?, ?);", (2, "1993-09-24 09:10:00", "Secure vaults often encrypt many messages, ensuring no data escapes.", 1234567919))
    db.execute("INSERT INTO notes (assocUser, dateWritten, note, publicID) VALUES (?, ?, ?, ?);", (2, "1993-09-24 10:45:10", "Credentials and password information are restricted", 1234567920))
    db.execute("INSERT INTO notes (assocUser, dateWritten, note, publicID) VALUES (?, ?, ?, ?);", (2, "1993-09-24 11:10:15", "Use secret notes for sensitive password storage", 1234567921))
    db.execute("INSERT INTO notes (assocUser, dateWritten, note, publicID) VALUES (?, ?, ?, ?);", (2, "1993-09-24 12:20:15", "All credentials are stored under secret notes", 1234567922))
    db.execute("INSERT INTO notes (assocUser, dateWritten, note, publicID) VALUES (?, ?, ?, ?);", (2, "1993-09-24 13:30:30", "The password is saved in the confidential notes section", 1234567923))
    db.execute("INSERT INTO notes (assocUser, dateWritten, note, publicID) VALUES (?, ?, ?, ?);", (2, "1993-09-24 14:40:45", "Der er vigtig info i brugeren bernardo's password", 1234567924))
    db.execute("INSERT INTO notes (assocUser, dateWritten, note, publicID) VALUES (?, ?, ?, ?);", (2, "1993-09-24 15:50:00", "Password data must be handled with extreme caution", 1234567925))
    db.execute("INSERT INTO notes (assocUser, dateWritten, note, publicID) VALUES (?, ?, ?, ?);", (2, "1993-09-24 16:00:00", "Check secret notes for additional password details", 1234567926))
    db.execute("INSERT INTO notes (assocUser, dateWritten, note, publicID) VALUES (?, ?, ?, ?);", (2, "1993-09-24 17:10:15", "All credentials are saved in the secure notes section", 1234567927))
    db.execute("INSERT INTO notes (assocUser, dateWritten, note, publicID) VALUES (?, ?, ?, ?);", (2, "1993-09-24 18:20:30", "Password is stored in the confidential notes section", 1234567928))
    

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
            note = request.form['noteinput']
            db = connect_db()
            c = db.cursor()
            statement = """INSERT INTO notes(id,assocUser,dateWritten,note,publicID) VALUES(null,?,?,?,?);"""
            c.execute(statement, (session['userid'], time.strftime('%Y-%m-%d %H:%M:%S'), note, secrets.randbelow(9999999999)))
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

@app.route("/note")
def view_note():
    noteid = request.args.get('noteid')
    if not noteid:
        return "Note ID is required", 400

    db = connect_db()
    c = db.cursor()
    # SQL Injection vulnerability
    statement = f"""SELECT * FROM notes WHERE publicID = '{noteid}'"""
    print(statement)
    c.execute(statement)
    note = c.fetchall()
    db.close()

    print(note)

    return jsonify(note)


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