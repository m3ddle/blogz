from app import db
from hashutils import make_pw_hash


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text)
    date = db.Column(db.DateTime)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __init__(self, title, body, date, owner):
        self.title = title
        self.body = body
        self.date = date
        self.owner = owner


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    pw_hash = db.Column(db.String(120))
    posts = db.relationship("Post", backref="owner")

    def __init__(self, email, pw_hash):
        self.email = email
        self.pw_hash = pw_hash
