from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from models.user import User
from models.task import Task
from models.report import Report
from app import db

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        return redirect(url_for('main.dashboard'))
    users = User.query.all()
    tasks = Task.query.all()
    return render_template('admin/admin_dashboard.html', users=users, tasks=tasks)

@admin_bp.route('/admin/users')
@login_required
def manage_users():
    users = User.query.all()
    return render_template('admin/manage_users.html', users=users)

@admin_bp.route('/admin/users/delete/<int:user_id>')
@login_required
def delete_user(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('admin.manage_users'))

@admin_bp.route('/admin/reports')
@login_required
def view_reports():
    reports = Report.query.all()
    return render_template('admin/reports.html', reports=reports)

