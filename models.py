"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)



# need user model with id (pkey), first_name(not null), last_name(not null), image_url (have default img)]

class User(db.Model):
    """User Info (fill out later)"""

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
                            default = "https://merriam-webster.com/assets/mw/images/article/art-wap-article-main/egg-3442-e1f6463624338504cd021bf23aef8441@2x.jpg")