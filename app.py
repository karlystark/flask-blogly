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
def display_user_list_page():
    """Renders user list page"""
    users = User.query.all()

# CHANGE HTML PAGES TO INCLUDE UNDERSCORES
    return render_template('user_list.html', users=users)


@app.get('/users/new')
def new_users_form():
    """Renders new user form"""
    return render_template('new_users_form.html')


@app.post('/users/new')
def process_new_user():
    """Collects new user form data and creates a new User instance, updating
    the database. Redirects to users list page."""
    first_name = request.form['firstname']
    last_name = request.form['lastname']
    image_url = request.form['imageurl']

    if image_url == '':
        image_url = None

    new_user = User(
        first_name=first_name,
        last_name=last_name,
        image_url=image_url
    )

    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')


@app.get('/users/<int:user_id>')
def show_user_profile(user_id):
    """Collects user data and renders user profile page."""
    user = User.query.get_or_404(user_id)

    return render_template('user_profile.html',
                           user=user,
                           user_id=user_id)


@app.get('/users/<int:user_id>/edit')
def show_user_edit_page(user_id):
    """Collects user data and renders user profile edit page."""
    user = User.query.get_or_404(user_id)


    return render_template('user_edit_page.html',
                           user=user,
                           user_id=user_id)


@app.post('/users/<int:user_id>/edit')
def process_user_edits(user_id):
    """Collect user edit form data and edit user instance in database,
    redirect to user list page."""
    user = User.query.get_or_404(user_id)

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