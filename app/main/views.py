from . import main
from flask import render_template
from flask_login import login_required, current_user
from ..decorators import professor_required

@main.route('/')
def index():
    return render_template('main/index.html', title="Welcome")

@main.route('/professor/dashboard')
@login_required
@professor_required
def professor_dashboard():
    return render_template('main/professor_dashboard.html', title="Dashboard")

@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('main/dashboard.html', title="Dashboard")
