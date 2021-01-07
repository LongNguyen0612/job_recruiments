from flask import Flask
from app.db.database import initialize_db
from app.routers import home, auth, jobs, contact,admin

def create_app():
    app = Flask(__name__)

    app.config.from_pyfile('settings.py')

    initialize_db(app)
    app.register_blueprint(home.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(jobs.bp)
    app.register_blueprint(contact.bp)
    app.register_blueprint(admin.bp)

    return app
