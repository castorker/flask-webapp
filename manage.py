from quibbles import app, db
from quibbles.models import User, Quibble, Tag
from flask_script  import Manager, prompt_bool
from flask_migrate import Migrate, MigrateCommand

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)


@manager.command
def insert_data():
    castorker = User(username="castorker", email="castorker@example.com", password="dev")
    db.session.add(castorker)

    def add_quibble(text, category, tags):
        db.session.add(Quibble(text=text, category=category, user=castorker, tags=tags))

    for name in ["c", "java", "internet", "programmer", "computer", "firewall", "bugs", "hacker", "memory"]:
        db.session.add(Tag(name=name))
    db.session.commit()

    add_quibble("Old programmers never die, they just can't C as well.", "Programmers", "c,programmer")
    add_quibble("Why don't programmers like nature? It has too many bugs.", "Programmers", "bugs,programmer")
    add_quibble("Why do Java Programmers wear glasses? Because they don't see sharp.", "Programmers", "java,programmer")
    add_quibble("Old programmers never die .. they just lose their memory.", "Programmers", "programmer,memory")
    add_quibble("A crazy programmer with a cold is a coughing hacker.", "Programmers", "programmer,hacker")
    add_quibble("Sign on the door of an internet hacker. 'Gone Phishing'.", "Technology", "internet,hacker")
    add_quibble("Did you hear about the computer technician who received third degree burns? He touched the firewall.", "Computer", "computer,firewall")

    craftsman = User(username="craftsman", email="craftsman@example.com", password="dev")
    db.session.add(craftsman)
    db.session.commit()
    print('Database initialized')


@manager.command
def drop_db():
    if prompt_bool("WARNING: Are you sure you want to lose all your data"):
        db.drop_all()
        print('Database dropped')


if __name__ == '__main__':
    manager.run()
