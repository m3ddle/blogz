from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
import os
import datetime

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://blogz:gitrdone@localhost:3307/blogz"
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
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __init__(self, title, body, date, owner_id):
        self.title = title
        self.body = body
        self.date = date
        self.owner = owner_id


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    posts = db.relationship("Post", backref="owner")

    def __init__(self, email, password):
        self.email = email
        self.password = password


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


@app.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        verify = request.form["verify"]

        # TODO: Validate user data

        existing_user = User.query.filter_by(email=email).first()

        if not existing_user:
            new_user = User(email, password)
            db.session.add(new_user)
            db.session.commit()
            session["email"] = email
            return redirect("/")
        else:
            # TODO: use a better message here
            return "<h1>Duplicate user</h1>"

    return render_template("register.html")


@app.route("/view-post", methods=["POST", "GET"])
def view_post():
    post_id = request.args.get("post")
    post = Post.query.get(int(post_id))
    post_title = post.title
    post_body = post.body

    return render_template("view-post.html", post_body=post_body, post_title=post_title)


@app.route("/add-post", methods=["POST", "GET"])
def add_post():
    post_title = ""
    post_body = ""
    title_error = ""
    body_error = ""
    posts = Post.query.all()
    if request.method == "POST":
        post_title = request.form["post-title"]
        post_body = request.form["new-post"]
        owner = User.query.filter_by(email=session["email"]).first()
        owner_id = owner.id

        if post_title == "" or post_body == "":
            if post_title == "":
                title_error = "Must have a title."

            if post_body == "":
                body_error = "Wheres the post!?"

            return render_template("add-post.html", title="Build a Blog",
                                   title_error=title_error, body_error=body_error, post_title=post_title, post_body=post_body)

        new_post = Post(post_title, post_body,
                        datetime.datetime.now(), 400)
        db.session.add(new_post)
        db.session.commit()
        new_post_id = new_post.id
        return redirect(f"/view-post?post={new_post_id}")
    return render_template("add-post.html", title="Build a Blog",
                           title_error=title_error, body_error=body_error)


if __name__ == "__main__":
    app.run()
