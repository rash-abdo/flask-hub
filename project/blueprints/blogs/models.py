from project.app import db
from project.blueprints.profiles.models import Users

class Blogs(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    date = db.Column(db.String(100),nullable=False)
    path = db.Column(db.String(300),nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"))
    title = db.Column(db.String(100),nullable=False)
    like = db.Column(db.Integer)
    dislike = db.Column(db.Integer)