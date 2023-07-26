"""Blogly application."""

import os

from flask import Flask, redirect, render_template, request
from models import db, connect_db, User


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///blogly')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)


@app.get('/')
def home_page():

    return redirect('/users')


@app.get('/users')
def users():
    users = User.query.all()
    return render_template('userlist.html', users = users)

@app.get('/users/new')
def new_users_form():

    return render_template('newusersform.html')

@app.post('/users/new')
def process_new_user():
    first_name = request.form['firstname']
    last_name = request.form['lastname']
    image_url = request.form['imageurl']

    new_user = User(first_name=first_name,
                    last_name=last_name,
                    image_url=image_url)

    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

