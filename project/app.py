from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt



db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:12345@localhost/flask'
    app.config['SECRET_KEY'] = 'SOME KEY'


    db.init_app(app)
    bcrypt.init_app(app)
    
    # Import Blueprints here
    from project.blueprints.profiles.routes import profile
    app.register_blueprint(profile, url_prefix='/profile')


    return app
