from flask import render_template, url_for, flash, redirect, request
from app import app, db
from app.forms import FriendForm
from app.models import Friend


@app.route('/')
def index():
    friends = Friend.query.all()
    q = request.args.get('q')
    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1

    if q:
        friends = Friend.query.filter(Friend.name.contains(q) | Friend.last_name.contains(q))
    else:
        friends = Friend.query.order_by(Friend.id.desc())

    pages = friends.paginate(page=page, per_page=5)
    return render_template('index.html', friends=friends, pages=pages, q=q)


@app.route('/create', methods=['GET', 'POST'])
def create():
    form = FriendForm()
    if form.validate_on_submit():
        friend = Friend(name=form.name.data,
                        last_name=form.last_name.data,
                        phone=form.phone.data,
                        sex=form.sex.data,
                        birth_day=form.birth_day.data,
                        friend_rank=form.friend_rank.data,
                        hobby=form.hobby.data)
        db.session.add(friend)
        db.session.commit()
        flash('Your friend has been created!', 'success')
        return redirect(url_for('index'))
    return render_template('create.html', form=form)


@app.route("/friend/<int:friend_id>")
def friend(friend_id):
    friend = Friend.query.get_or_404(friend_id)
    return render_template('friend.html', friend=friend)


@app.route("/friend/<int:friend_id>/update", methods=['GET', 'POST'])
def update_friend(friend_id):
    friend = Friend.query.get_or_404(friend_id)
    form = FriendForm()
    if form.validate_on_submit():
        friend.name = form.name.data
        friend.last_name = form.last_name.data
        friend.phone = form.phone.data
        friend.sex = form.sex.data
        friend.birth_day = form.birth_day.data
        friend.friend_rank = form.friend_rank.data
        friend.hobby = form.hobby.data
        db.session.commit()
        flash('Your friend hes been updated!', 'success')
        return redirect(url_for('friend', friend_id=friend.id))
    elif request.method == 'GET':
        form.name.data = friend.name
        form.last_name.data = friend.last_name
        form.phone.data = friend.phone
        form.sex.data = friend.sex
        form.birth_day.data = friend.birth_day
        form.friend_rank.data = friend.friend_rank
        form.hobby.data = friend.hobby

    return render_template('create.html', form=form)


@app.route("/friend/<int:friend_id>/delete", methods=['GET', 'POST'])
def delete_friend(friend_id):
    friend = Friend.query.get_or_404(friend_id)
    db.session.delete(friend)
    db.session.commit()
    flash('Your friend hes been deleted!', 'success')
    return redirect(url_for('index'))