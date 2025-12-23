from flask import Blueprint, render_template

main_bp = Blueprint("main_bp", __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/server_monitor')
def server_monitor():
    return render_template('server_monitor.html')