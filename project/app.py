from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os


load_dotenv("project/config.env")
db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI")
    app.config['UPLOAD_FOLDER'] = os.getenv("UPLOAD_FOLDER")
    app.config['UPLOAD_IMAGE_FOLDER'] = os.getenv("UPLOAD_IMAGE_FOLDER")
    
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    db.init_app(app)
    bcrypt.init_app(app)
    
    # Import Blueprints here
    from project.blueprints.profiles.routes import profile
    from project.blueprints.blogs.routes import blogs
    app.register_blueprint(blogs)
    app.register_blueprint(profile)


    return app
