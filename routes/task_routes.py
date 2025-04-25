from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app import db
from models.task import Task
from models.submission import Submission

task_bp = Blueprint('tasks', __name__)

@task_bp.route('/tasks/create', methods=['GET', 'POST'])
@login_required
def create_task():
    if request.method == 'POST':
        task = Task(
            title=request.form['title'],
            description=request.form['description'],
            created_by=current_user.id
        )
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('tasks.list_tasks'))
    return render_template('task_create.html')

@task_bp.route('/tasks')
@login_required
def list_tasks():
    tasks = Task.query.all()
    return render_template('task_list.html', tasks=tasks)

@task_bp.route('/tasks/<int:task_id>/submit', methods=['GET', 'POST'])
@login_required
def submit_task(task_id):
    if request.method == 'POST':
        submission = Submission(
            content=request.form['content'],
            student_id=current_user.id,
            task_id=task_id
        )
        db.session.add(submission)
        db.session.commit()
        return redirect(url_for('main.dashboard'))
    return render_template('task_submit.html', task_id=task_id)

@task_bp.route('/tasks/<int:task_id>/review', methods=['GET', 'POST'])
@login_required
def review_task(task_id):
    submissions = Submission.query.filter_by(task_id=task_id).all()
    return render_template('task_review.html', submissions=submissions, task_id=task_id)

@task_bp.route('/submission/<int:submission_id>/grade', methods=['POST'])
@login_required
def grade_submission(submission_id):
    submission = Submission.query.get(submission_id)
    submission.grade = request.form['grade']
    submission.feedback = request.form['feedback']
    db.session.commit()
    return redirect(url_for('tasks.review_task', task_id=submission.task_id))
