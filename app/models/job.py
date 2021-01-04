from app.db.database import db


class Jobs(db.Document):
    image = db.StringField(required=False)
    title = db.StringField(required=True)
    company = db.StringField(required=True)
    address = db.StringField(required=True)
    description = db.StringField(required=True)
    experience = db.StringField()
    tag_list = db.ListField(db.StringField())
    salary = db.StringField(required=True)
