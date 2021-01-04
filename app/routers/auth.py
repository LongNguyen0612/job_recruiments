from typing import no_type_check_decorator
from flask import Blueprint, session, render_template, redirect, url_for, request, flash
from app.models.user import User
from app.models.recruiter import Recruiter

import bcrypt

bp = Blueprint('auth', __name__)

@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("signup.html")
    if request.method == "POST":
        user_info = request.form
        existing_user = User.objects(email=user_info["email"]).first()
        if existing_user is None:
            hashpass = bcrypt.hashpw(
                user_info["password"].encode("utf-8"), bcrypt.gensalt()
            )
            user = User(
                username=user_info["username"],
                password=hashpass,
                email=user_info["email"],
                user_type=user_info['user_type']
            )
            user.save()
            if user_info['user_type'] == 'recruiter':
                return redirect(url_for("auth.recruiter"))
            return redirect(url_for("auth.login"))

        flash("user is already exists", "error")

@bp.route("/recruiter", methods=["GET", "POST"])
def recruiter():
    if request.method == "GET":
        return render_template('recruiter.html')
    elif request.method == "POST":
        data = request.form
        user = User.objects(email=data["email"]).first()
        if user and user.user_type == "recruiter":
            recruiter = Recruiter(
                email = data['email'],
                name = data['name'],
                company = data['company'],
                address = data['address'],
                phone_number = data['phone_number'],
                description = data['description']
            )
            recruiter.save()
            return redirect(url_for("auth.login"))
        return render_template('recruiter.html')

@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        user_in = request.form
        login_user = User.objects(username=user_in["username"]).first()
        session["user_type"] = login_user["user_type"]

        if login_user :
            if session["user_type"] == "recruiter":
                session["username"] = user_in["username"]
                return redirect(url_for("jobs.query_records"))

        password = user_in["password"].encode("utf-8")
        password_in_db = login_user["password"].encode("utf-8")

        if login_user :
            if bcrypt.checkpw(password, password_in_db):
                session["username"] = user_in["username"]
            flash("Incorrect username or password")
            return redirect(url_for("home.home"))


@bp.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("home.home"))