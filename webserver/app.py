from flask import *
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)
app.secret_key = 'mysecretkey'

mysql = MySQL(app)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'testuser'
app.config['MYSQL_PASSWORD'] = 'tspas'
app.config['MYSQL_DB'] = 'logindb'

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = %s AND password = %s', (email, password,))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['id'] = user['id']
            session['email'] = user['email']
            return redirect(url_for('dashboard'))
        else:
            message = 'Invalid email or password'
            return render_template('login.html', message=message)
            print("Invalid email or password")
    else:
        if 'loggedin' in session:
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        firstname = request.form['first-name']
        lastname = request.form['last-name']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        user = cursor.fetchone()
        if user:
            message = 'Email already exists'
            return render_template('register.html', message=message)
        else:
            cursor.execute('INSERT INTO users VALUES (NULL, %s, %s, %s,%s)', (firstname,lastname, email, password))
            mysql.connection.commit()
            message = 'You have successfully registered'
            return render_template('register.html', message=message)
    else:
        return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'loggedin' in session:
        return render_template('dash.html')
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

