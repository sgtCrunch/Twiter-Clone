"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows

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


    class UserModelTestCase(TestCase):
        """Test views for messages."""

        def setUp(self):
            """Create test client, add sample data."""

            User.query.delete()
            Message.query.delete()
            Follows.query.delete()

            self.client = app.test_client()

        def test_user_model(self):
            """Does basic model work?"""

            u = User(
                email="test@test.com",
                username="testuser",
                password="HASHED_PASSWORD"
            )

            db.session.add(u)
            db.session.commit()

            # User should have no messages & no followers
            self.assertEqual(len(u.messages), 0)
            self.assertEqual(len(u.followers), 0)

            #test repr
            self.assertEqual(repr(u), "<User #1: testuser, test@test.com>")

        def test_is_followed_by(self):
            """Does model function correctly dectect if user if being followed by another"""

            u = User(
                email="test1@test.com",
                username="testuser1",
                password="HASHED_PASSWORD"
            )

            u2 = User(
                email="test1@test.com",
                username="testuser2",
                password="HASHED_PASSWORD"
            )

            u3 = User(
                email="test3@test.com",
                username="testuser3",
                password="HASHED_PASSWORD"
            )

            following1 = Follows(1,2)

            db.session.add(u)
            db.session.add(u2)
            db.session.add(u3)
            db.session.add(following1)
            db.session.commit()

            self.assertTrue(u2.is_following(u))
            self.assertFalse(u.is_following(u3))

            self.assertTrue(u.is_followed_by(u2))
            self.assertFalse(u.is_followed_by(u3))

        def test_user_creation(self):
            """Test user creation and authentication"""

            u = User.signup(username="test", email="test@test.com", password="Test", image_url="test.png")
            db.session.commit()

            u2 = User.query.get(1)

            self.assertEqual(u.username, u2.username)

            with self.assertRaises(Exception):
                u3 = User.signup(username="test", email="test@test.com", password="Test", image_url="test.png")
                db.session.commit()

            with self.assertRaises(Exception):
                u4 = User.signup(username="test", password="Test", image_url="test.png")
                db.session.commit()

            u = User.authenticate("test", "Test")
            uFail = User.authenticate("fakeName", "Test")
            uFail2 = User.authenticate("test","fakepass")

            self.assertTrue(u)
            self.assertFalse(uFail)
            self.assertFalse(uFail2)


            


            
            

