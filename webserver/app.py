from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import config

app = Flask(__name__)
db = mysql.connector.connect(
    host=config.db_host,
    user=config.db_user,
    password=config.db_password,
    database=config.db_name
)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return "Passwords do not match"

        cursor = db.cursor()
        query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        values = (username, password)
        cursor.execute(query, values)
        db.commit()
        cursor.close()

        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = db.cursor()
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        values = (username, password)
        cursor.execute(query, values)
        user = cursor.fetchone()
        cursor.close()

        if user:
            return "Welcome, " + user[1]
        else:
            return "Invalid username or password"

    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
