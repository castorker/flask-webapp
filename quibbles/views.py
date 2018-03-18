from flask import render_template, flash, redirect, url_for, request, abort
from flask_login import login_required, login_user, logout_user, current_user

from quibbles import app, db, login_manager
from .forms import QuibbleForm, LoginForm, SignupForm
from .models import User, Quibble, Tag


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', new_quibbles=Quibble.newest(7))


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = QuibbleForm()
    if form.validate_on_submit():
        text = form.text.data
        category = form.category.data
        tags = form.tags.data
        quibble = Quibble(user=current_user, text=text, category=category, tags=tags)
        db.session.add(quibble)
        db.session.commit()
        flash("Stored quibble: '{} {}'".format(text, category))
        return redirect(url_for('index'))
    return render_template('add.html', form=form)


@app.route('/edit/<int:quibble_id>', methods=['GET', 'POST'])
@login_required
def edit_quibble(quibble_id):
    quibble = Quibble.query.get_or_404(quibble_id)
    if current_user != quibble.user:
        abort(403)
    form = QuibbleForm(obj=quibble)
    if form.validate_on_submit():
        form.populate_obj(quibble)
        db.session.commit()
        flash("Stored quibble: '{} {}'".format(quibble.text, quibble.category))
        return redirect(url_for('user', username=current_user.username))
    return render_template('quibble_form.html', form=form, title="Edit quibble")


@app.route('/delete/<int:quibble_id>', methods=['GET', 'POST'])
@login_required
def delete_quibble(quibble_id):
    quibble = Quibble.query.get_or_404(quibble_id)
    if current_user != quibble.user:
        abort(403)
    if request.method == "POST":
        db.session.delete(quibble)
        db.session.commit()
        flash("Deleted quibble: '{} {}'".format(quibble.text, quibble.category))
        return redirect(url_for('user', username=current_user.username))
    else:
        flash("Please confirm deleting the quibble.")
    return render_template('confirm_delete.html', quibble=quibble, nolinks=True)


@app.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_username(form.username.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash("Logged in successfully as {}.".format(user.username))
            return redirect(request.args.get('next') or url_for('user', username=user.username))
        flash('Incorrect username or password.')
    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    flash("User has logged out.")
    logout_user()
    return redirect(url_for('index'))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data, password = form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Welcome, {}! Please login.'.format(user.username))
        return redirect(url_for('login'))
    return render_template("signup.html", form=form)


@app.route('/tag/<name>')
def tag(name):
    tag = Tag.query.filter_by(name=name).first_or_404()
    return render_template('tag.html', tag=tag)


@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.context_processor
def inject_tags():
    return dict(all_tags=Tag.all)
