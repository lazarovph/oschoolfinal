from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from models.models import Task, Solution
from datetime import datetime

task_bp = Blueprint('task', __name__)

@task_bp.route('/tasks', methods=['GET', 'POST'])
@login_required
def tasks():
    if current_user.role == 'teacher':
        if request.method == 'POST':
            title = request.form['title']
            description = request.form['description']
            due_date = request.form['due_date']
            task = Task(title=title, description=description, due_date=datetime.strptime(due_date, '%Y-%m-%d'), created_by=current_user.id)
            db.session.add(task)
            db.session.commit()
            flash('Задачата е създадена успешно.')
        tasks = Task.query.all()
        return render_template('tasks.html', tasks=tasks)
    else:
        return redirect(url_for('main.dashboard'))

@task_bp.route('/task/<int:task_id>', methods=['GET', 'POST'])
@login_required
def task_detail(task_id):
    task = Task.query.get_or_404(task_id)
    if request.method == 'POST':
        content = request.form['content']
        solution = Solution(content=content, user_id=current_user.id, task_id=task.id)
        db.session.add(solution)
        db.session.commit()
        flash('Решението е качено успешно.')
        return redirect(url_for('task.tasks'))
    return render_template('task_detail.html', task=task)
