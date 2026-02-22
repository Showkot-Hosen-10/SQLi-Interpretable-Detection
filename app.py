from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import sqlite3
import joblib
import shap
import numpy as np
import pandas as pd
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'showkot-hosen-sqli-detector-2025'

# Load ML Models
print("🔄 Loading ML Models...")
dt_model = joblib.load('sqli_detector_model.joblib')
# Load ML Models
print("🔄 Loading ML Models...")
dt_model = joblib.load('sqli_detector_model.joblib')
import zipfile
with zipfile.ZipFile('sqli_vectorizer.zip', 'r') as z:
    vectorizer = joblib.load(z.open('sqli_vectorizer.joblib'))  # FIXED!
explainer = shap.TreeExplainer(dt_model)
feature_names = vectorizer.get_feature_names_out()
print("✅ Models loaded!")

explainer = shap.TreeExplainer(dt_model)
feature_names = vectorizer.get_feature_names_out()
print("✅ Models loaded!")

def init_db():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    
    # DROP & RECREATE ALL TABLES
    c.execute('DROP TABLE IF EXISTS students')
    c.execute('DROP TABLE IF EXISTS soc_alerts')
    c.execute('DROP TABLE IF EXISTS users')
    
    # ✅ USERS TABLE (LOGIN CREDENTIALS)
    c.execute('''CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        student_id TEXT UNIQUE,
        role TEXT DEFAULT 'student',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # ✅ STUDENTS TABLE (PROFILES)
    c.execute('''CREATE TABLE students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        student_id TEXT UNIQUE NOT NULL,
        email TEXT,
        address TEXT,
        admission_fee REAL,
        result TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # ✅ SOC ALERTS
    c.execute('''CREATE TABLE soc_alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        query TEXT,
        prediction TEXT,
        confidence REAL,
        top_feature TEXT,
        shap_value REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # ✅ SAMPLE USERS
    c.executemany("INSERT INTO users (username, password, student_id, role) VALUES (?, ?, ?, ?)", [
        ('student', 'student123', 'STU001', 'student'),
        ('admin', 'admin123', None, 'admin')
    ])
    
    # ✅ SAMPLE STUDENTS
    c.executemany("INSERT INTO students (name, student_id, email, address, admission_fee, result) VALUES (?, ?, ?, ?, ?, ?)", [
        ('Alice Johnson', 'STU001', 'alice@email.com', 'Dhaka, Bangladesh', 50000.0, 'A+'),
        ('Bob Wilson', 'STU002', 'bob@email.com', 'Chittagong, Bangladesh', 45000.0, 'A'),
        ('Carol Lee', 'STU003', 'carol@email.com', 'Rajshahi, Bangladesh', 48000.0, 'A-'),
        ('David Kim', 'STU004', 'david@email.com', 'Sylhet, Bangladesh', 52000.0, 'A')
    ])
    
    conn.commit()
    print("✅ Database initialized: Users + Students + Sample Data!")
    conn.close()

def detect_sqli(query, username="anonymous"):
    """ML-Powered SQLi Detection + XAI"""
    X_query = vectorizer.transform([query]).toarray()
    pred = dt_model.predict(X_query)[0]
    prob = dt_model.predict_proba(X_query)[0,1]
    
    shap_vals = explainer.shap_values(X_query)
    shap_class1 = shap_vals[1] if isinstance(shap_vals, list) else shap_vals
    top_idx = np.argmax(np.abs(shap_class1[0]))
    top_feature = feature_names[top_idx]
    shap_val = shap_class1[0, top_idx]
    
    return {
        'is_sqli': bool(pred),
        'confidence': float(prob),
        'top_feature': top_feature,
        'shap_value': float(shap_val)
    }

# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('students.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        conn.close()
        
        if user:
            session['role'] = user[4]  # role column
            session['username'] = username
            session['user_id'] = user[0]
            if user[3]:  # student_id
                session['student_id'] = user[3]
            flash(f'✅ Welcome back, {username}!')
            if user[4] == 'admin':
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('dashboard'))
        else:
            flash('❌ Invalid credentials!')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        student_id = request.form['student_id']
        email = request.form['email']
        address = request.form['address']
        admission_fee = float(request.form['admission_fee'])
        result = request.form['result']
        
        conn = sqlite3.connect('students.db')
        c = conn.cursor()
        try:
            # ✅ CREATE LOGIN USER
            c.execute("INSERT INTO users (username, password, student_id) VALUES (?, ?, ?)",
                     (username, password, student_id))
            
            # ✅ CREATE STUDENT PROFILE
            c.execute("INSERT INTO students (name, student_id, email, address, admission_fee, result) VALUES (?, ?, ?, ?, ?, ?)",
                     (name, student_id, email, address, admission_fee, result))
            conn.commit()
            flash(f'✅ Account created! Login: {username}/{password}')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError as e:
            flash('❌ Username or Student ID already exists!')
        finally:
            conn.close()
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'role' not in session:
        return redirect(url_for('login'))
    
    if session['role'] == 'student':
        conn = sqlite3.connect('students.db')
        c = conn.cursor()
        c.execute("SELECT * FROM students WHERE student_id=?", (session['student_id'],))
        profile = c.fetchone()
        conn.close()
        return render_template('dashboard.html', profile=profile, role='student')
    else:
        return redirect(url_for('admin'))

@app.route('/search', methods=['POST'])
def search():
    if 'role' not in session:
        return redirect(url_for('login'))
    
    query = request.form['query']
    result = detect_sqli(query, session.get('username', ''))
    
    if result['is_sqli']:
        conn = sqlite3.connect('students.db')
        c = conn.cursor()
        c.execute("INSERT INTO soc_alerts (username, query, prediction, confidence, top_feature, shap_value) VALUES (?, ?, ?, ?, ?, ?)",
                 (session.get('username', 'anonymous'), query, 'SQLi DETECTED', result['confidence'], result['top_feature'], result['shap_value']))
        conn.commit()
        conn.close()
        
        flash(f'🚨 SQLi BLOCKED! {result["confidence"]:.1%} | {result["top_feature"]} | SHAP: {result["shap_value"]:+.3f}')
        return redirect(url_for('dashboard'))
    
    # Safe search
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute("SELECT * FROM students WHERE student_id=? OR name LIKE ? OR email LIKE ?", 
             (query, f"%{query}%", f"%{query}%"))
    students = c.fetchall()
    conn.close()
    
    return render_template('dashboard.html', students=students, search_query=query, role='student')

@app.route('/admin')
def admin():
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute("SELECT * FROM students ORDER BY id DESC LIMIT 20")
    students = c.fetchall()
    c.execute("SELECT * FROM soc_alerts ORDER BY timestamp DESC LIMIT 20")
    alerts = c.fetchall()
    conn.close()
    
    return render_template('admin.html', students=students, alerts=alerts)

@app.route('/logout')
def logout():
    session.clear()
    flash('👋 Logged out successfully!')
    return redirect(url_for('home'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
