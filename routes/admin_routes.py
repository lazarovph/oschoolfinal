from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required
from app import db
from models.models import User, Task, Solution

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
@login_required
def admin_panel():
    if current_user.role != 'admin':
        return redirect(url_for('main.dashboard'))

    users = User.query.all()
    tasks = Task.query.all()
    return render_template('admin/admin_panel.html', users=users, tasks=tasks)

@admin_bp.route('/admin/user/<int:user_id>/delete')
@login_required
def delete_user(user_id):
    if current_user.role != 'admin':
        return redirect(url_for('main.dashboard'))
    
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('Потребителят е изтрит успешно.')
    return redirect(url_for('admin.admin_panel'))

@admin_bp.route('/admin/task/<int:task_id>/delete')
@login_required
def delete_task(task_id):
    if current_user.role != 'admin':
        return redirect(url_for('main.dashboard'))
    
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash('Задачата е изтрита успешно.')
    return redirect(url_for('admin.admin_panel'))
