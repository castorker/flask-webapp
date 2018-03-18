from quibbles import app, db
from quibbles.models import User
from flask_script  import Manager, prompt_bool

manager = Manager(app)


@manager.command
def init_db():
    db.create_all()
    db.session.add(User(username="castorker", email="castorker@example.com", password="dev"))
    db.session.add(User(username="craftsman", email="craftsman@example.com", password="dev"))
    db.session.commit()
    print('Database initialized')


@manager.command
def drop_db():
    if prompt_bool("WARNING: Are you sure you want to lose all your data"):
        db.drop_all()
        print('Database dropped')


if __name__ == '__main__':
    manager.run()
