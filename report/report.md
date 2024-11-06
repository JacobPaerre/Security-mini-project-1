# Security: Pen-testing 1

Made by Alex, Carmen, Daniel, & Jacob

## Fixed vulnerabilities

### Using `secrets`-library instead of rand

We chose to repalce the rand-method with the `secrets`' modules method for getting a random number. This is because the rand method is actually predictable if the seed is known or guessed. `secrets` is also a module that is used to generate cryptographically strong random numbers suitable for managing data.

### Fixing SQL injection

Most of the SQL queries used in the application were prone to SQL injection, e.g:

```python
statement = "SELECT * FROM notes WHERE assocUser = %s;" %session['userid']
c.execute(statement)
```

We have fixed this vulnerability by sanitizing the input and making the queries parameterized:

```python
statement = "SELECT * FROM notes WHERE assocUser = ?;"
c.execute(statement, (session['userid'],))
```

To do this when initializing the database, we can not use executescript, as it does not support parameterized queries. Therefore, we use execute instead.

### Hash passwords

We have also fixed the vulnerability of storing passwords in plain text. We now hash the passwords before storing them in the database. We use werkzeug.security for this.

### Do not check if or inform about passwords already in use when registering

We have fixed the vulnerability of informing the user if a password is already in use when registering. This was a security risk, as it could be used to guess passwords.
Different users should be able to use the same password, so we have removed this check completely. The user will now be informed if the username is already in use, but not if the password is already in use, and the user will be able to register with the same password as another user.

### Cross-site scripting attacks (XSS)

We had a look at XSS to see if it was necessary for us to sanitize the user input. After doing some research, we figured that Flask uses Jinja2 as the template engine, and because of the way a node is displayed, it would not matter if a user had submitted html or JavaScript code. Jinja2 automatically escapes variables to prevent XSS attacks.

### Secure Session Cookies

We have set the session cookie to be secure, so it will only be sent over HTTPS. This is done by setting the `SESSION_COOKIE_SECURE` to `True` in the config.
We also set the `SESSION_COOKIE_HTTPONLY` to `True` to prevent the cookie from being accessed by JavaScript.
