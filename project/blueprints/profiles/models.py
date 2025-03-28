from project.app import db

class Users(db.Model):  
    id = db.Column(db.Integer, primary_key = True)
    infos = db.relationship('Info', backref='user',
                 cascade="all, delete", passive_deletes=True)
    name = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(50),nullable=False,unique=True)
    password = db.Column(db.String(60),nullable=False,unique=True)

class Info(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"))
    color = db.Column(db.String(20))
    music = db.Column(db.String(30))