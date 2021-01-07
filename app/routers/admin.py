from flask import Blueprint, session, render_template, redirect, url_for, request, abort, json
from app.models.job import Jobs
from app.models.recruiter import Recruiter
from app.routers.auth import register
from app.models.apply import Apply
from slugify import slugify
import json


bp = Blueprint('admin', __name__)


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

@bp.route('/apply', methods=['POST','GET'])
def apply():
    if session["user_type"] == "employee":
        if request.method == "GET":
            aply = Apply.objects()
            return render_template("apply.html",apply=aply)
        if request.method == "POST":
            data = request.form
            query = Apply.objects(username=data["username"]).first()
            apply = Apply(
                username=data["username"],
                email= data["email"],
                CV= data["CV"],
                title=data["title"]
            )
            apply.save()
            return redirect(url_for("jobs.all_job"))


@bp.route('/user-admin/apply', methods=["GET","POST"])
def usrapply():
    if session["user_type"] == "recruiter":
        if request.method == "GET":
            query = Apply.objects()
            job = Jobs.objects()
            return render_template("mng_apply.html",apply=query)

@bp.route('/deleteapply/<string:getid>', methods = ['POST','GET'])
def delete(getid):
    if session["user_type"] == "recruiter":
        apply = Apply.objects(id=getid).first()
        if not apply:
            return jsonify({'error': 'data not found'})
        else:
            apply.delete()	
        return render_template("mng_apply.html")