from flask import render_template, url_for, flash, redirect, request
from app import app,bcrypt,db
from app.forms import RegistrationForm, LoginForm
from app.models import User, Post
from pprint import pprint

@app.route('/')
def index():
  return render_template('index.html', name='IPZ', title='PNU')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=format(form.email.data)).first()
        if user == None:
            flash(f'There is no user with this email', category='errors')
        else:
            if user.email == format(form.email.data) and bcrypt.check_password_hash(
                    bcrypt.generate_password_hash(format(form.password.data), 10), user.password) == True:
                flash(f'Welcome {user.username}', category='success')
            else:
                flash(f'Email or password wrong', category='errors')
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
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

@app.route('/posts', methods=['GET','POST'])
def posts():
    user = {'nickname' : 'Miguel'}
    posts = [
        {
            'author' : {'nickname' : 'Miguel'},
            'body' : 'Beautiful day in Portland'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'The Avengers movie was so cool'
        }
    ]
    return render_template('posts.html',title='Home',user=user,posts=posts)