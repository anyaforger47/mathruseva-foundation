from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import mysql.connector
from flask_cors import CORS
from functools import wraps

app = Flask(__name__)
CORS(app)

# Secret key for session management
app.secret_key = 'mathruseva_foundation_2024_secure_key'

# MySQL Configuration
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'NehaJ@447747',  # Replace with your actual MySQL password
    'database': 'mathruseva_foundation'
}

def get_db_connection():
    return mysql.connector.connect(**MYSQL_CONFIG)

# Authentication decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Simple authentication (you can modify this to check against a database)
        if username == 'admin' and password == 'admin123':
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid username or password')
    
    return render_template('login.html')

# Logout route
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Dashboard (protected)
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('index.html')

# Serve login page as default
@app.route('/')
def index():
    if 'logged_in' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

# Keep all your existing API routes here...
# (Copy all your existing routes from app.py here)
