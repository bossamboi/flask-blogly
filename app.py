"""Blogly application."""

from tabnanny import process_tokens
from flask import Flask, request, redirect, render_template, flash
from models import db, connect_db, User, Post, DEFAULT_IMAGE_URL
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secret-key'

debug = DebugToolbarExtension(app)



connect_db(app)
db.create_all()


@app.get("/")
def redirect_to_users():
    """ Redirect to display users """
    return redirect("/users")


@app.get("/users")
def show_users():
    """ Show all current users """

    users = User.query.all()

    return render_template("user_listing.html", users=users)


@app.get("/users/new")
def show_new_user_form():
    """ Display new user form """

    return render_template("new_user_form.html")


@app.post("/users/new")
def process_and_add_new_user():
    """ Process form and add new user to database. Redirect to users list """

    first_name = request.form.get("first-name")
    last_name = request.form.get("last-name")
    image_url = request.form.get("image-url")

    new_user = User(first_name = first_name, last_name = last_name, image_url = image_url)

    # Add new object to session, so they'll persist
    db.session.add(new_user)

    db.session.commit()

    return redirect("/users")


@app.get("/users/<int:user_id>")
def show_user_details(user_id):
    """ Show profile page for user """

    # grab user id object
    user = User.query.get_or_404(user_id)
    posts = user.posts

    return render_template("user_detail_page.html", user = user, posts=posts)


@app.get("/users/<int:user_id>/edit")
def show_user_edit_page(user_id):
    """ Show edit page for user """

    user = User.query.get_or_404(user_id)

    return render_template("user_edit_page.html", user = user)


@app.post("/users/<int:user_id>/edit")
def process_user_edit(user_id):
    """ Update database with user edits and return user to user's profile """

    first_name = request.form.get("first-name-edit")
    last_name = request.form.get("last-name-edit")
    image_url = request.form.get("image-url-edit")

    user = User.query.get_or_404(user_id)

    user.first_name = first_name
    user.last_name = last_name

    if image_url == "":
        image_url = DEFAULT_IMAGE_URL

    user.image_url = image_url

    # user.edit_user(first_name, last_name, image_url)

    db.session.add(user)
    db.session.commit()

    # could add flash message for success edit
    flash("Profile successfully updated")

    return redirect(f"/users/{user_id}")


@app.post("/users/<int:user_id>/delete")
def delete_user(user_id):
    """ Delete user and redirect to users list """

    user = User.query.get_or_404(user_id)

    # user.query.delete()

    db.session.delete(user)

    db.session.commit()

    # could add flash message for successful delete

    return redirect("/users")



# BLOG POST ROUTES

@app.get("/users/<int:user_id>/posts/new")
def show_new_post_form(user_id):
    """ Show new post form for user"""

    user = User.query.get_or_404(user_id)

    return render_template("new_post_form.html", user = user)


@app.post("/users/<int:user_id>/posts/new")
def process_and_add_new_post(user_id):
    """ Process new post form, add post to database, redirect to user detail page """

    title = request.form.get("title")
    content = request.form.get("content")

    new_post = Post(title = title, content = content, user_id = user_id)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/users/{user_id}")

@app.get("/posts/<int:post_id>")
def show_post_detail(post_id):
    """ Show post detail """

    post = Post.query.get_or_404(post_id)

    return render_template("post_detail_page.html", post=post)


@app.get("/posts/<int:post_id>/edit")
def show_edit_post_form(post_id):
    """ Show form to edit post """

    post = Post.query.get_or_404(post_id)

    return render_template("post_edit_page.html", post = post)


@app.post("/posts/<int:post_id>/edit")
def process_post_edit(post_id):
    """ Process change data in post, update data base, redirect to post view"""

    new_title = request.form.get("title-edit")
    new_content = request.form.get("content-edit")

    post = Post.query.get_or_404(post_id)

    post.title = new_title
    post.content = new_content

    db.session.add(post)
    db.session.commit()

    flash("Post changes saved")

    return redirect(f"/posts/{post_id}")

@app.post("/posts/<int:post_id>/delete")
def delete_post(post_id):
    """ Delete post from database """

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)

    db.session.commit()

    flash("Post removed")

    return redirect(f"/users/{post.user_id}")