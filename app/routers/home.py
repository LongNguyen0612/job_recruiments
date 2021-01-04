from flask import Blueprint, session, render_template
from app.models.job import Jobs

bp = Blueprint('home', __name__, url_prefix='/')

@bp.route("/")
def home():
    if 'username' in session:
        username = session['username']
        return render_template("index.html", login=username)
    return render_template("index.html")