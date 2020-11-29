from flask import render_template, url_for, flash, redirect, request
from app import app, bcrypt, db
from app.forms import RegistrationForm, LoginForm
from app.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from app.forms import RegistrationForm, LoginForm, UpdateAccountForm
import os
import secrets
from PIL import Image


@app.route('/')
def index():
    return render_template('index.html', name='IPZ', title='PNU')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=format(form.email.data)).first()
        if user == None:
            flash(f'There is no user with this email', category='errors')
        else:
            if user.email == format(form.email.data) and bcrypt.check_password_hash(user.password,
                                                                                    form.password.data) == True:
                login_user(user, remember=form.remember.data)
                flash(f'Welcome {user.username}', category='success')
                next_page = request.args.get('next')
                if next_page:
                    return redirect(next_page)
                else:
                    return redirect(url_for('index'))
            else:
                flash(f'Email or password wrong', category='errors')
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    register = RegistrationForm()
    if register.validate_on_submit():
        user = User()
        if User.query.filter_by(email=format(register.email.data)).first() == None:
            user.username = format(register.username.data)
            user.email = format(register.email.data)
            user.password = bcrypt.generate_password_hash(format(register.password.data))
            db.session.add(user)
            db.session.commit()
            flash(f'Account created for {register.username.data}!', category='success')
            return redirect(url_for('login'))
        else:
            flash(f'This user already exist', category='success')
    return render_template('register.html', register=register)


@app.route('/posts', methods=['GET', 'POST'])
def posts():
    user = {'nickname': 'Miguel'}
    posts = [
        {
            'author': {'nickname': 'Miguel'},
            'body': 'Beautiful day in Portland'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'The Avengers movie was so cool'
        }
    ]
    return render_template('posts.html', title='Home', user=user, posts=posts)


@app.route('/logout')
def logout():
    logout_user()
    flash("You have been logged out")
    return redirect(url_for('index'))


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        if bcrypt.check_password_hash(current_user.password, form.old_password.data):
            hashed_password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
            current_user.password = hashed_password
            flash('Password was changed!','success')
        else:
            flash('Your old password is not correct!','error')

        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about = form.about.data
        current_user.last_seen = form.last_seen.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about.data = current_user.about
        form.last_seen.data = current_user.last_seen
    image = url_for('static', filename='img/' + current_user.image_file)
    return render_template('account.html', title='Account', image=image, form=form)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/img', picture_fn)
    # form_picture.save(picture_path)
    # return picture_fn
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn
