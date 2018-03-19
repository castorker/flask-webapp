from flask import render_template, flash, redirect, url_for, request, abort
from flask_login import login_required, current_user

from . import quibbles
from . forms import QuibbleForm
from .. import db
from .. models import User, Quibble, Tag


@quibbles.route('/add', methods=['GET', 'POST'])
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
        return redirect(url_for('main.index'))
    return render_template('quibble_form.html', form=form, title="Add quibble")


@quibbles.route('/edit/<int:quibble_id>', methods=['GET', 'POST'])
@login_required
def edit(quibble_id):
    quibble = Quibble.query.get_or_404(quibble_id)
    if current_user != quibble.user:
        abort(403)
    form = QuibbleForm(obj=quibble)
    if form.validate_on_submit():
        form.populate_obj(quibble)
        db.session.commit()
        flash("Stored quibble: '{} {}'".format(quibble.text, quibble.category))
        return redirect(url_for('.user', username=current_user.username))
    return render_template('quibble_form.html', form=form, title="Edit quibble")


@quibbles.route('/delete/<int:quibble_id>', methods=['GET', 'POST'])
@login_required
def delete(quibble_id):
    quibble = Quibble.query.get_or_404(quibble_id)
    if current_user != quibble.user:
        abort(403)
    if request.method == "POST":
        db.session.delete(quibble)
        db.session.commit()
        flash("Deleted quibble: '{} {}'".format(quibble.text, quibble.category))
        return redirect(url_for('.user', username=current_user.username))
    else:
        flash("Please confirm deleting the quibble.")
    return render_template('confirm_delete.html', quibble=quibble, nolinks=True)


@quibbles.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


@quibbles.route('/tag/<name>')
def tag(name):
    tag = Tag.query.filter_by(name=name).first_or_404()
    return render_template('tag.html', tag=tag)
