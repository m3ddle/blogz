from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
import os
import datetime

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://build-a-blog:gitrdone@localhost:3307/build-a-blog"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.secret_key = "qwertyuiop"


# Note: To update the database with these model classes do the following:

# Open a python shell:
# $ python

# import this file and the appropriate classes:

# $ from main import db, Post, User etc.

# instruct mysql to create all tables:

# $ db.create_all()

# Good luck!


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text)
    date = db.Column(db.DateTime)
    # This will be used when I implement users
    #owner_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __init__(self, title, body, date):
        self.title = title
        self.body = body
        self.date = date
        #self.owner = owner_id

# Saving this class for when it is time to implement users

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(120), unique=True)
#     password = db.Column(db.String(120))
#     posts = db.relationship("Post", backref="owner")

#     def __init__(self, email, password):
#         self.email = email
#         self.password = password


@app.route("/", methods=["POST", "GET"])
def index():
    title_error = ""
    body_error = ""
    posts = Post.query.all()
    if request.method == "POST":
        post_title = request.form["post-title"]
        post_body = request.form["new-post"]

        if post_title == "" or post_body == "":
            if post_title == "":
                title_error = "Must have a title."

            if post_body == "":
                body_error = "Wheres the post!?"

            return render_template("posts.html", title="Build a Blog",
                                   posts=posts, title_error=title_error, body_error=body_error, post_title=post_title, post_body=post_body)

        new_post = Post(post_title, post_body, datetime.datetime.now())
        db.session.add(new_post)
        db.session.commit()
    posts = Post.query.all()

    return render_template("posts.html", title="Build a Blog", posts=posts,
                           title_error=title_error, body_error=body_error)


@app.route("/add", methods=["POST", "GET"])
def add_post():

    return render_template("add.html")


if __name__ == "__main__":
    app.run()
