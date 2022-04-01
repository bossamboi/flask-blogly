"""Models for Blogly."""

from enum import unique
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://merriam-webster.com/assets/mw/images/article/art-wap-article-main/egg-3442-e1f6463624338504cd021bf23aef8441@2x.jpg"


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """User information"""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    first_name = db.Column(db.String(50),
                            nullable=False)
    last_name = db.Column(db.String(50),
                            nullable=False)
    image_url = db.Column(db.String,
                            default=DEFAULT_IMAGE_URL)

    posts = db.relationship('Post',
                            backref='user')

    def __repr__(self):
        """Return repr with user data"""
        u = self

        return f"<User {u.id} {u.first_name} {u.last_name} {u.image_url}>"


class Post(db.Model):
    """Post information"""

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    title = db.Column(db.String(50),
                            nullable=False)
    content = db.Column(db.String,
                            nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.id"),
                        nullable=False)



    tags = db.relationship('Tag',
                            secondary="posttags",
                            backref="posts")


    def __repr__(self):
        """Return repr with post data"""
        p = self

        return f"<Post {p.id} Author {p.user_id} {p.title} {p.created_at}>"


class Tag(db.Model):
    """Tag information"""

    __tablename__ = "tags"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    name = db.Column(db.String(50),
                    nullable=False,
                    unique=True)


    def __repr__(self):
        """Return repr with tag data"""
        t = self

        return f"<Tag {t.id} {t.name}>"
        

class PostTag(db.Model):
    """PostTag information """

    __tablename__ = "posttags"

    post_id = db.Column(db.Integer,
                        db.ForeignKey("posts.id"),
                        primary_key=True)
    tag_id = db.Column(db.Integer,
                        db.ForeignKey("tags.id"),
                        primary_key=True)