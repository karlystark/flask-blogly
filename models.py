"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""

    app.app_context().push()
    db.app = app
    db.init_app(app)

class User(db.Model):
    __tablename__ = "user"

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
        default='https://is3-ssl.mzstatic.com/image/thumb/Purple30/v4/89/a6/70/89a67093-f892-cdcd-00af-76d6a68c4ec0/source/256x256bb.jpg'
    )

