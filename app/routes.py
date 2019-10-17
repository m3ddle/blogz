from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from hashutils import check_pw_hash, make_pw_hash, make_salt
import os
import datetime
from app import app, db
from app.models import User, Post


@app.before_request
def require_login():
    allowed_routes = ["login", "register"]
    print(session)
    if request.endpoint not in allowed_routes and "email" not in session:
        return redirect("/login")


@app.route("/")
def index():
    user_list = User.query.all()

    return render_template("index.html", user_list=user_list)


@app.route("/posts", methods=["POST", "GET"])
def posts():
    title_error = ""
    body_error = ""
    posts = Post.query.all()
    if request.method == "POST":
        post_title = request.form["post-title"]
        post_body = request.form["new-post"]
        owner = User.query.filter_by(email=session["email"]).first()

        if post_title == "" or post_body == "":
            if post_title == "":
                title_error = "Must have a title."

            if post_body == "":
                body_error = "Wheres the post!?"

            return render_template("add-post.html", title="Build a Blog",
                                   title_error=title_error, body_error=body_error, post_title=post_title, post_body=post_body)

        new_post = Post(post_title, post_body,
                        datetime.datetime.now(), owner)
        db.session.add(new_post)
        db.session.commit()
        new_post_id = new_post.id

    posts = Post.query.all()

    return render_template("posts.html", title="Build a Blog", posts=posts,
                           title_error=title_error, body_error=body_error)


@app.route("/register", methods=['POST', 'GET'])
def register():
    email = ""
    email_error = ""
    password_error = ""
    verify_error = ""
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        verify = request.form["verify"]
        email_error = ""
        password_error = ""
        verify_error = ""

        if password == "":
            password_error = "Password cannot be blank. "

        elif len(password) < 3 or len(password) > 20:
            password = ""
            verify = ""
            password_error = password_error + \
                "Password must be between 3 and 20 characters in length. "

        if verify == "":
            verify_error = "Password cannot be blank. "

        if " " in email:
            email_error = email_error + "Username cannot contain spaces. "

        if " " in password:
            password = ""
            verify = ""
            password_error = password_error + "Password cannot contain spaces. "

        if password != verify:
            password = ""
            verify = ""
            verify_error = verify_error + "Does not match password. "
        # TODO: Validate user data
        if not email_error and not password_error and not verify_error:

            existing_user = User.query.filter_by(email=email).first()

            if not existing_user:
                new_user = User(email, make_pw_hash(password))
                db.session.add(new_user)
                db.session.commit()
                session["email"] = email
                return redirect("/add-post")
            else:
                # TODO: use a better message here
                return "<h1>Duplicate user</h1>"

    return render_template("register.html", email_error=email_error, password_error=password_error, verify_error=verify_error, email=email)


@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = User.query.filter_by(email=email).first()
        if user and check_pw_hash(password, user.pw_hash) == True:

            session["email"] = email
            flash("Logged in")
            print(session)
            return redirect("/add-post")
        else:
            flash("User password incorrect, or user does not exist", "error")
    return render_template("login.html")


@app.route("/logout")
def logout():
    del session["email"]
    return redirect('/')


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

        if post_title == "" or post_body == "":
            if post_title == "":
                title_error = "Must have a title."

            if post_body == "":
                body_error = "Wheres the post!?"

            return render_template("add-post.html", title="Build a Blog",
                                   title_error=title_error, body_error=body_error, post_title=post_title, post_body=post_body)

        new_post = Post(post_title, post_body,
                        datetime.datetime.now(), owner)
        db.session.add(new_post)
        db.session.commit()
        new_post_id = new_post.id
        return redirect(f"/view-post?post={new_post_id}")
    return render_template("add-post.html", title="Build a Blog",
                           title_error=title_error, body_error=body_error)


@app.route("/blog")
def blog():
    title_error = ""
    body_error = ""
    user_id = request.args.get("user")
    posts = Post.query.filter_by(owner_id=user_id).all()
    username = User.query.filter_by(id=user_id).first()

    return render_template("posts.html", title="Build a Blog", posts=posts,
                           title_error=title_error, body_error=body_error)
