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
    return redirect("/users")

@app.get("/users")
def show_users():
    # get users from db
    users = User.query.all()
    # loop through and display each as link

    # add link to add-user form
    return render_template('user_listing.html', users = users)

# @app.get("/users/new")
# @app.post("/users/new")
# @app.get("/users/<int:user_id>")
# @app.get("/users/<int:user_id>/edit")
# @app.post("/users/<int:user_id>/edit")
# @app.post("/users/<int:user_id>/delete")
