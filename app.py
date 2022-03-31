"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User
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
    """ Process form and add new user to database """

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
    user = User.query.get(user_id)

    return render_template("user_detail_page.html", user = user)


@app.get("/users/<int:user_id>/edit")
def show_user_edit_page(user_id):
    """ Show edit page for user """

    user = User.query.get(user_id)

    return render_template("user_edit_page.html", user = user)


@app.post("/users/<int:user_id>/edit")
def process_user_edit(user_id):
    """ Update database with user edits and return user to user's profile """

    first_name = request.form.get("first-name-edit")
    last_name = request.form.get("last-name-edit")
    image_url = request.form.get("image-url-edit")

    user = User.query.get(user_id)

    user.edit_user(first_name, last_name, image_url)

    db.session.commit()

    return redirect(f"/users/{user_id}")


@app.post("/users/<int:user_id>/delete")
def delete_user(user_id):
    """ Delete user """

    user = User.query.get(user_id)

    db.session.delete(user)

    db.session.commit()

    return redirect("/users")





