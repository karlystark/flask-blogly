"""Blogly application."""

import os

from flask import Flask, redirect, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///blogly')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


connect_db(app)

app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)


@app.get('/')
def home_page():
    """Redirect to user list page"""
    return redirect('/users')


@app.get('/users')
def users():
    """Renders user list page"""
    users = User.query.all()

    return render_template('userlist.html', users = users)


@app.get('/users/new')
def new_users_form():
    """Renders new user form"""
    return render_template('newusersform.html')


@app.post('/users/new')
def process_new_user():
    """Collects new user form data and creates a new User instance, updating
    the database. Redirects to users list page."""
    first_name = request.form['firstname']
    last_name = request.form['lastname']
    image_url = request.form['imageurl']

    if image_url == '':
        image_url = None

    new_user = User(first_name=first_name,
                    last_name=last_name,
                    image_url=image_url)

    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')


@app.get('/users/<int:user_id>')
def show_user_profile(user_id):
    """Collects user data and renders user profile page."""
    user = User.query.get(user_id)

    first_name = user.first_name
    last_name = user.last_name
    image_url = user.image_url

    return render_template('userprofile.html',
                           first_name = first_name,
                           user_id = user_id,
                           last_name = last_name,
                           image_url = image_url)


@app.get('/users/<int:user_id>/edit')
def show_user_edit_page(user_id):
    """Collects user data and renders user profile edit page."""
    user = User.query.get(user_id)

    first_name = user.first_name
    last_name = user.last_name
    image_url = user.image_url

    return render_template('usereditpage.html',
                           user_id = user_id,
                           first_name = first_name,
                           last_name = last_name,
                           image_url = image_url)


@app.post('/users/<int:user_id>/edit')
def process_user_edits(user_id):
    """Collect user edit form data and edit user instance in database,
    redirect to user list page."""
    user = User.query.get(user_id)

    first_name = request.form['firstname']
    last_name = request.form['lastname']
    image_url = request.form['imageurl']

    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url

    db.session.commit()

    return redirect('/users')


@app.post('/users/<int:user_id>/delete')
def delete_user_profile(user_id):
    """Deletes user from database on delete button click, redirects to
    user list page."""

    user = User.query.get(user_id)

    db.session.delete(user)
    db.session.commit()

    return redirect('/users')