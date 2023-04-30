"""User View tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_user_views.py


import os
from unittest import TestCase

from models import db, connect_db, Message, User

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

from app import app, CURR_USER_KEY

with app.app_context():
    db.create_all()

    app.config['WTF_CSRF_ENABLED'] = False


    class UserViewTestCase(TestCase):
        """Test views for Users."""

        def setUp(self):
            """Create test client, add sample data."""

            User.query.delete()
            Message.query.delete()

            self.client = app.test_client()

            self.testuser = User.signup(username="testuser",
                                        email="test@test.com",
                                        password="testuser",
                                        image_url=None)
            self.testuser3 = User.signup(username="testuser3",
                                        email="test3@test.com",
                                        password="testuser3",
                                        image_url=None)
            db.session.commit()

        def test_signup(self):
            """Check signup page and signup function"""

            with self.client as c:

                resp = c.get("/signup")
                self.assertEquals(resp.status_code, 200)
                d = {"username":"testuser2",
                    "email":"test2@test.com",
                    "password":"testuser2",
                    "image_url":None}
                resp = c.post('/signup', data=d, follow_redirects=True)
                html = resp.get_data(as_text=True)
                
                self.assertEqual(resp.status_code, 200)
                self.assertIn(html, "@testuser2")


        def test_login_logout(self):
            """Check login/logout page and function"""

            with self.client as c:

                resp = c.get("/login")
                self.assertEquals(resp.status_code, 200)

                d = {"username":"testuser","password":"testuser"}
                resp = c.post('/login', data=d, follow_redirects=True)
                html = resp.get_data(as_text=True)
                
                self.assertEqual(resp.status_code, 200)
                self.assertIn(html, "Hello, testuser!")

                resp = c.get('/logout')
                html = resp.get_data(as_text=True)

                self.assertEqual(resp.status_code, 200)
                self.assertIn(html, "Goodbye, testuser!")


        def test_show_users(self):
            """Check show users route"""

            with self.client as c:

                resp = c.get('/users')
                self.assertEqual(resp.status_code, 200)
                html = resp.get_data(as_text=True)

                self.assertIn('@testuser', html)


        def test_show_user(self):
            """Check user profile route"""

            with self.client as c:

                resp = c.get(f'/users/{self.testuser.id}')
                self.assertEqual(resp.status_code, 200)
                html = resp.get_data(as_text=True)

                self.assertIn('@testuser', html)

        def test_show_user_likes(self):
            """Check user likes page"""

            with self.client as c:

                resp = c.get(f'/users/{self.testuser.id}/likes')
                self.assertEqual(resp.status_code, 200)
                html = resp.get_data(as_text=True)

                self.assertIn('@testuser', html)

        def test_show_user_following(self):
            """Check user following page and not logged-in message"""

            with self.client as c:

                resp = c.get(f'/users/{self.testuser.id}/following')
                self.assertEqual(resp.status_code, 200)
                html = resp.get_data(as_text=True)
                self.assertIn('Access unauthorized.', html)

                with c.session_transaction() as sess:
                    sess[CURR_USER_KEY] = self.testuser.id
                
                resp = c.get(f'/users/{self.testuser.id}/following')
                self.assertEqual(resp.status_code, 200)
                html = resp.get_data(as_text=True)
                self.assertIn('@testuser', html)
        
        def test_show_user_followers(self):
            """Check user followers page and not logged-in message"""

            with self.client as c:

                resp = c.get(f'/users/{self.testuser.id}/followers')
                self.assertEqual(resp.status_code, 200)
                html = resp.get_data(as_text=True)
                self.assertIn('Access unauthorized.', html)

                with c.session_transaction() as sess:
                    sess[CURR_USER_KEY] = self.testuser.id
                
                resp = c.get(f'/users/{self.testuser.id}/following')
                self.assertEqual(resp.status_code, 200)
                html = resp.get_data(as_text=True)
                self.assertIn('@testuser', html)

        def test_add_follow(self):
            """Check add follow to user and not logged-in message"""

            with self.client as c:

                resp = c.post(f'/users/follow/{self.testuser3.id}', follow_redirects=True)
                self.assertEqual(resp.status_code, 200)
                html = resp.get_data(as_text=True)
                self.assertIn('Access unauthorized.', html)

                with c.session_transaction() as sess:
                    sess[CURR_USER_KEY] = self.testuser.id
                
                resp = c.get(f'/users/follow/{self.testuser3.id}', follow_redirects=True)
                self.assertEqual(resp.status_code, 200)
                html = resp.get_data(as_text=True)
                self.assertNotIn('Access unauthorized.', html)

                resp = c.get(f'/users/stop-following/{self.testuser3.id}', follow_redirects=True)
                self.assertEqual(resp.status_code, 200)
                html = resp.get_data(as_text=True)
                self.assertNotIn('@testuser3', html)
