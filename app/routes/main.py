from flask import Blueprint, render_template

bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    return render_template('index.html')

@bp.route('/about')
def about():
    return render_template('about.html')

@bp.route('/features')
def features():
    return render_template('features.html')

@bp.route('/how-to-use')
def how_to_use():
    return render_template('how_to_use.html')
