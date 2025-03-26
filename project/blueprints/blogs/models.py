from project.app import db

class Blogs(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    date = db.Column(db.String(100),nullable=False)
    path = db.Column(db.String(300),nullable=False)
    user_id = db.Column(db.Integer,nullable=False)
    title = db.Column(db.String(100),nullable=False)