import os

os.environ["DATABASE_URL"] = "postgresql:///blogly_test"
#createdb blogly_test and run from there

from unittest import TestCase

from app import app, db
from models import User, Post


# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.drop_all()
db.create_all()


class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the
        # User model below.
        User.query.delete()

        self.client = app.test_client()

        test_user = User(
            first_name="test1_first",
            last_name="test1_last",
            image_url=None,
        )

        test_post = Post(
            title='test1_post',
            content='test1_content',
        )

        db.session.add(test_user)
        db.session.add(test_post)
        db.session.commit()

        # We can hold onto our test_user's id by attaching it to self (which is
        # accessible throughout this test class). This way, we'll be able to
        # rely on this user in our tests without needing to know the numeric
        # value of their id, since it will change each time our tests are run.
        self.user_id = test_user.id
        self.post_id = test_post.post_id

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_list_users(self):
        """Tests that user list HTML appears on screen and status code is 200"""
        with self.client as c:
            resp = c.get("/users")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("test1_first", html)
            self.assertIn("test1_last", html)


    def test_new_users_form(self):
        """Tests that new user form HTML appears on screen and status code is 200"""
        with self.client as c:
            resp = c.get('/users/new')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('First Name', html)


    def test_process_new_user(self):
        """Tests redirect after new user form submit"""
        with self.client as c:
            resp = c.post('/users/new', data= {"firstname":"test1_first",
                                                "lastname":"test1_last",
                                                "imageurl": ''})
            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, '/users')

# make test making same post request and follow redirect, make sure new user appears in userlist

    def test_user_profile_page(self):
        """Tests that correct user profile is displayed on page"""
        with self.client as c:
            resp = c.get(f'/users/{self.user_id}')
            html = resp.get_data(as_text=True)
            self.assertIn("test1_first", html)
            self.assertEqual(resp.status_code, 200)


    def test_user_edit_page(self):
        """Tests that user edit page is displayed on page"""
        with self.client as c:
            resp = c.get(f'/users/{self.user_id}/edit')
            html = resp.get_data(as_text=True)
            self.assertIn("test1_last", html)
            self.assertEqual(resp.status_code, 200)

#add a test for the out of bounds bug once we fix it to prove that it's fixed

    def test_user_profile_page(self):
        """Tests that we are returned a 404 response, when user id doesn't exist"""
        with self.client as c:
            resp = c.get('/users/100')
            self.assertEqual(resp.status_code, 404)

    def test_show_add_new_post_form(self):
        """Tests that correct post is being displayed on page"""
        with self.client as c:
            resp = c.get(f'/users/{self.user_id}/posts/new')
            html = resp.get_data(as_text=True)
            self.assertIn("test1_newpost", html)
            self.assertEqual(resp.status_code, 200)


    def test_process_post_edits(self):

        with self.client as c:
            resp = c.get(f'/posts/{self.post_id}/edit')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
