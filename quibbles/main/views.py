from flask import render_template

from . import main
from .. import login_manager
from .. models import User, Quibble, Tag


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@main.route('/')
# @main.route('/index')
def index():
    return render_template('index.html', new_quibbles=Quibble.newest(7))


@main.app_errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403


@main.app_errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404


@main.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@main.app_context_processor
def inject_tags():
    return dict(all_tags=Tag.all)
