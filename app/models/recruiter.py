from flask.globals import request
from app.db.database import db


class Recruiter(db.Document):
    email = db.EmailField(required=True)
    name = db.StringField(required=True)
    company = db.StringField(required=True, max_length=15)
    address = db.StringField(required=True)
    phone_number = db.StringField()
    description = db.StringField(required=True)
