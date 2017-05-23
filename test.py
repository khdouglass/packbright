from unittest import TestCase
from model import connect_to_db, db, example_data
from server import app
from flask import session


class BasicFlaskTests(TestCase):
    """Flask tests."""

    def setUp(self):
        """Do before each test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        result = self.client.get('/')
        self.assertIn('<h4>Start packing for your next trip!</h4>', result.data)

    def test_register_page(self):
        result = self.client.get('/register')
        self.assertIn("<form action='/register' method='POST'>", result.data)

    
class DatabaseFlaskTests(TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Do before each test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_login(self):
        """Test login process."""

        result = self.client.post("/login", data={'user_id': 'khdouglass', 'password': '1234'},
                                  follow_redirects=True)

        self.assertIn("<h1>Create new trip</h1>", result.data)


if __name__ == '__main__':
    import unittest

    unittest.main()