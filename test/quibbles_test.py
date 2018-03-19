from flask import url_for
from flask_testing import TestCase

import quibbles
from quibbles.models import User, Quibble

class QuibblesTestCase(TestCase):

    def create_app(self):
        return quibbles.create_app('test')

    def setUp(self):
        self.db = quibbles.db
        self.db.create_all()
        self.client = self.app.test_client()

        user = User(username='testuser', email='testuser@example.com', password='test')
        quibble = Quibble(user=user, text="Old programmers never die, they just can't C as well.",
                          category="Programmers", tags="c,programmer")

        self.db.session.add(user)
        self.db.session.add(quibble)
        self.db.session.commit()

        self.client.post(url_for('auth.login'),
            data = dict(username='testuser', password='test'))

    def tearDown(self):
        quibbles.db.session.remove()
        quibbles.db.drop_all()

    def test_delete_all_tags(self):
        response = self.client.post(
            url_for('quibbles.edit', quibble_id=1),
            data = dict(
                text = "Old programmers never die, they just can't C as well.",
                category = "Programmers",
                tags = ""
            ),
            follow_redirects = True
        )

        assert response.status_code == 200
        quibble = Quibble.query.first()
        assert not quibble._tags
