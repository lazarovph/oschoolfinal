from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from models.models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        level = request.form.get('level')
        group = request.form.get('group')

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Имейлът вече е регистриран.')
            return redirect(url_for('auth.register'))

        hashed_pw = generate_password_hash(password, method='sha256')
        new_user = User(username=username, email=email, password=hashed_pw, role=role, level=level, group=group)
        db.session.add(new_user)
        db.session.commit()
        flash('Регистрацията е успешна. Моля, влезте.')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        flash('Невалидни данни за вход.')

    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
