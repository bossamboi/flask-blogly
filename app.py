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

# Commit--otherwise, this never gets saved!
    db.session.commit()

    return redirect("/users")


# @app.get("/users/<int:user_id>")
# @app.get("/users/<int:user_id>/edit")
# @app.post("/users/<int:user_id>/edit")
# @app.post("/users/<int:user_id>/delete")
