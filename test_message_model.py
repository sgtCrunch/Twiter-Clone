import os
from unittest import TestCase

from models import db, User, Message, Follows

import datetime

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

with app.app_context():
    db.create_all()


    class MessagesModelTestCase(TestCase):
        """Test views for messages."""

        def setUp(self):
            """Create test client, add sample data."""

            User.query.delete()
            Message.query.delete()
            Follows.query.delete()

            self.client = app.test_client()

        def test_messages_model(self):
            """Does basic model work?"""

            u = User(
                email="test@test.com",
                username="testuser",
                password="HASHED_PASSWORD"
            )

            m = Message(
                text = "test",
                user_id = 1
            )

            db.session.add(u)
            db.session.add(m)
            db.session.commit()

            # User should have one message
            self.assertEqual(len(u.messages), 1)
            # Messages should have datetime obj by default
            self.assertTrue(type(m.timestamp) is datetime.date)

            