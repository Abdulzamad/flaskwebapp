from crypt import methods
from flask import render_template, flash, redirect, url_for, request , session
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.forms import LoginForm, RegistrationForm , UserUpdateForm
from app.models import User, Recipe
from werkzeug.urls import url_parse
import random

@app.route('/mysite-admin' , methods=['GET' , 'POST'])
def adminLogin():
    if request.method == "POST":
        if current_user.is_authenticated:
            if current_user.role == "admin":
                session.cook_admin = "yes"
                redirect("/admin")

        else:
            redirect("/")
            
    return "<form method='post'> <input type='submit' value='go admin'></form>"



@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            if user.role == "admin":
                session["cook_admin"]="yes"
            flash('Invalid username or password')

            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = "/my-recipes"
        return redirect(next_page)
    return render_template('login.html', form=form , user=current_user)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@login_required
@app.route('/profile' , methods=['GET', 'POST'])
def profile():
    if not current_user.is_authenticated:
        return redirect("/login")
    form = UserUpdateForm()
    if form.validate_on_submit():
        current_user.email=form.email.data
        current_user.first_name=form.first_name.data
        current_user.last_name=form.last_name.data
        db.session.commit()
        db.session.flush()
    return render_template("profile.html" , user=current_user , form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():

    if current_user.is_authenticated:
        return redirect("/my-recipes")
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, first_name=form.first_name.data, last_name=form.last_name.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering! Please login below.')
        return redirect(url_for('login'))
    return render_template('register.html', form=form , user=current_user)