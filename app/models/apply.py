from app.db.database import db


class Apply(db.Document):
    username = db.StringField(required=True, max_length=15)
    email = db.EmailField(required=True)
    CV = db.StringField(required=True)
    title = db.StringField(required=True)