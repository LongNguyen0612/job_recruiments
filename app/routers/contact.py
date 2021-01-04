from flask import Blueprint, session, render_template

bp = Blueprint('contact', __name__)

@bp.route("/contact")
def contact():
    if 'username' in session:
        username = session['username']
        return render_template("contact.html", login=username)
    return render_template("contact.html")