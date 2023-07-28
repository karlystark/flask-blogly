"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

#global variable to hold default image link

def connect_db(app):
    """Connect to database."""

    app.app_context().push()
    db.app = app
    db.init_app(app)


class User(db.Model):
    __tablename__ = "users"
    # make sure tablename is plural

    posts = db.relationship('Post', backref='user')

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)

    first_name = db.Column(
        db.String(30),
        nullable=False)

    last_name = db.Column(
        db.String(50),
        nullable=False)

    image_url = db.Column(
        db.String,
        nullable=False,
        default='https://www.welcomewildlife.com/wp-content/uploads/2015/01/Raccoon-face.jpg'

    )


class Post(db.Model):
    __tablename__ = "posts"

    post_id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    title = db.Column(
        db.String(50),
        nullable=False
    )

    content = db.Column(
        db.String,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=db.func.now()
     )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id')
        )


