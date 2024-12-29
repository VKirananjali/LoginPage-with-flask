from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = "your_secret_key"

# MySQL Database Connection
def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Sql@2005",
        database="flask_login_system"
    )
    return conn

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', 
                       (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            flash('Login Successful', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid Credentials', 'error')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        user = cursor.fetchone()

        if user:
            flash('Username already exists', 'error')
            return redirect(url_for('signup'))
        else:
            cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', 
                           (username, password))
            conn.commit()
            conn.close()
            flash('Account created successfully', 'success')
            return redirect(url_for('login'))

    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)
