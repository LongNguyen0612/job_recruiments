from flask import Blueprint, session, render_template, redirect, url_for, request, abort, json
from app.models.job import Jobs
from app.models.recruiter import Recruiter
from app.routers.auth import register
from app.models.apply import Apply
from slugify import slugify
import json

bp = Blueprint('jobs', __name__)
"""
@bp.route("/create-job", methods=["GET", "POST"])
def create_job():
    if "username" in session:
        if request.method == "GET":
            return render_template("create_job.html")
        if request.method == "POST":
            job_info = request.form
            tags = job_info["tag_list"].split(",")
            job = Jobs(
                image=job_info['image'],
                title=job_info["title"],
                company=job_info["company"],
                address=job_info["address"],
                description=job_info["description"],
                experience=job_info["experience"],
                tag_list=tags,
                salary=job_info["salary"]
            )
            job.save()
            return redirect(url_for("jobs.all_job"))

        return redirect(url_for("auth.login"))
    return redirect(url_for("auth.login"))
    """


@bp.route("/all-job", methods=["GET","POST"])
def all_job():
    if "username" not in session:
        return redirect(url_for("auth.login"))
    elif "username" in session and session["user_type"] == "employee":
        username = session['username']
        jobs = Jobs.objects()
        pages = len(jobs) // 10 + len(jobs) % 10
        page_param = request.args.get('page')
        if page_param:
            jobs = jobs.skip(10*(int(page_param)-1)).limit(10)
        return render_template("jobs.html", jobs=jobs, count=len(jobs), username=username, pages=pages)
    elif session["user_type"] == "recruiter":
        jobss = Jobs.objects()
        pagess = len(jobss) // 10 + len(jobss) % 10
        page_params = request.args.get('page')
        if page_params:
            jobss = jobss.skip(10*(int(page_params)-1)).limit(10)
        return render_template("jobs_admin.html", jobs=jobss, count=len(jobss), pages=pagess)


@bp.route("/all-job/search", methods=["GET"])
def search_with_tag():
    if 'username' in session:
        if request.method == "GET":
            username = session['username']
            tag_name = request.args.get("q")
            query = Jobs.objects(tag_list=tag_name)
            return render_template("job_search.html", jobs=query, count=len(query))
        return render_template("jobs.html")


@bp.route("/job-details/<job_id>", methods=["GET", "POST"])
def job_detail(job_id=None):
    if session["user_type"] == "recruiter":
        job = Jobs.objects(id=job_id).first()
        recruiter = Recruiter.objects().first()
        return render_template("jobs_detail_admin.html", job=job, recruiter=recruiter)
    else:
        job = Jobs.objects(id=job_id).first()
        recruiter = Recruiter.objects().first()
        return render_template("job_details.html", job=job, recruiter=recruiter)

