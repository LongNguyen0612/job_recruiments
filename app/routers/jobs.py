from flask import Blueprint, session, render_template, redirect, url_for, request, abort, json
from app.models.job import Jobs
from app.models.recruiter import Recruiter
from app.routers.auth import register
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
    job = Jobs.objects(id=job_id).first()
    recruiter = Recruiter.objects().first()
    return render_template("job_details.html", job=job, recruiter=recruiter)

@bp.route("/user-admin", methods=["GET"])
def query_records():
    if "username" not in session:
        return redirect(url_for("home.home"))
    elif session["user_type"] == "employee":
        return redirect(url_for("home.home"))
    else:
        jobs = Jobs.objects()
        return render_template("useradmin.html",jobs=jobs)


@bp.route("/add", methods=["GET", "POST"])
def create_record():
    if session["user_type"] == "recruiter":
        txtimage = request.form['txtimage']
        txttitle = request.form['txttitle']
        txtcompany = request.form['txtcompany']
        txtaddress = request.form['txtaddress']
        txtdescription = request.form['txtdescription']
        txtexperience = request.form['txtexperience']
        txttag_list = request.form['txttag_list'].split(",")
        txtsalary = request.form['txtsalary']
        jobs_save = Jobs(
            image=txtimage,
            title=txttitle,
            company=txtcompany,
            address=txtaddress,
            description=txtdescription,
            experience=txtexperience,
            salary=txtsalary,
            tag_list=txttag_list
            )
        jobs_save.save()
        return redirect("/user-admin")


@bp.route("/updatejobs", methods=["POST"])
def updatejobss():
    if session["user_type"] == "recruiter":
        pk = request.form['pk']
        namepost = request.form['name']
        value = request.form['value']
        jobs_rs = Jobs.objects(id=pk)
        if not jobs_rs:
            return json.dumps({'error':'data not found'})
        else:
            if namepost == 'image':
                jobs_rs.update(image=value)
            elif namepost == 'title':
                jobs_rs.update(title=value)
            elif namepost == 'company':
                jobs_rs.update(company=value)
            elif namepost == 'address':
                jobs_rs.update(address=value)
            elif namepost == 'description':
                jobs_rs.update(description=value)
            elif namepost == 'experience':
                jobs_rs.update(experience=value)
            elif namepost == 'tag_list':
                jobs_rs.update(tag_list=value)
            elif namepost == 'salary':
                jobs_rs.update(salary=value)
        return json.dumps({'status':'OK'})


@bp.route('/delete/<string:getid>', methods = ['POST','GET'])
def delete_job(getid):
    if session["user_type"] == "recruiter":
        job = Jobs.objects(id=getid).first()
        if not job:
            return jsonify({'error': 'data not found'})
        else:
            job.delete()	
        return redirect('/user-admin')

