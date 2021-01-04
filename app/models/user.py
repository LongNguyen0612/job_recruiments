from app.db.database import db


class User(db.Document):
    username = db.StringField(required=True, max_length=15)
    password = db.StringField(required=True)
    email = db.EmailField(required=True)
    user_type = db.StringField()
