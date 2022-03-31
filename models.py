"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://merriam-webster.com/assets/mw/images/article/art-wap-article-main/egg-3442-e1f6463624338504cd021bf23aef8441@2x.jpg"

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)



class User(db.Model):
    """User information with instance method to edit info"""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                    primary_key = True,
                    autoincrement = True)
    first_name = db.Column(db.String(50),
                            nullable = False)
    last_name = db.Column(db.String(50),
                            nullable = False)
    image_url = db.Column(db.String,
                            nullable = False,
                            default = DEFAULT_IMAGE_URL)


    posts = db.relationship('Post',
                            backref='user')

    def __repr__(self):
        """Return repr with user data"""
        u = self

        return f"<User {u.id} {u.first_name} {u.last_name} {u.image_url}>"


    def edit_user(self, first_name, last_name, image_url):
        """ Update a user's information in the database """

        self.first_name = first_name
        self.last_name = last_name
        self.image_url = image_url


class Post(db.Model):
    """User information with instance method to edit info"""

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                    primary_key = True,
                    autoincrement = True)
    title = db.Column(db.String(50),
                            nullable = False)
    content = db.Column(db.String,
                            nullable = False)
    created_at = db.Column(db.DateTime, nullable = False,
        default = datetime.utcnow)
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.id"))


    def __repr__(self):
        """Return repr with user data"""
        p = self

        return f"<Post {p.id} Author {p.user_id} {p.title} {p.created_at}>"

