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
