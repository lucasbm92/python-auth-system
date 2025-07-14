from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import get_user_by_username, create_user

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if get_user_by_username(username):
            flash('Username already exists')
            return redirect(url_for('auth.register'))
        create_user(username, password)
        flash('Registration successful! Please log in.')
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user_by_username(username)
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash('Logged in successfully!')
            return redirect(url_for('auth.dashboard'))
        flash('Invalid credentials')
        return redirect(url_for('auth.login'))
    return render_template('login.html')

@auth_blueprint.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    return 'Welcome to your dashboard!'

@auth_blueprint.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully!')
    return redirect(url_for('auth.login'))
