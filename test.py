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

    
class LogInLogOutFlaskTests(TestCase):
    """Test login and logout."""

    def setUp(self):
        """Do before each test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, 'postgresql:///testdb')

        # Create tables and add sample data
        db.create_all()
        example_data()


    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()


    def test_login_success(self):
        """Test login process."""

        with self.client as c:
            result = c.post('/login', data={'username': 'khdouglass', 'password': '1234'},
                                                follow_redirects=True)
            self.assertEqual(session['user_id'], 'khdouglass')
            self.assertIn('California vacation', result.data)


    def test_login_fail(self):
        """Test login process failure with unknown username."""

        result = self.client.post('/login', data={'username': 'hacker', 'password': '1234'}, 
                                            follow_redirects=True)

        self.assertIn('User does not exist!', result.data)


    def test_login_password_fail(self):
        """Test login process failure with incorrect password."""

        result = self.client.post('/login', data={'username': 'khdouglass', 'password': '5678'}, 
                                            follow_redirects=True)

        self.assertIn('Password is incorrect!', result.data)


    def test_logout(self):
        """Test logout process."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 'khdouglass'

            result = self.client.get('/logout', follow_redirects=True)

            self.assertNotIn('user_id', session)
            self.assertIn('<label>Not a member? Sign up!', result.data)


    def test_registeration(self):
        """Test registration process."""

        with self.client as c:
            result = self.client.post('/register', data={'username': 'new_user', 'first_name': 'New',
                                                     'last_name': 'User', 'email': 'new@user.com',
                                                     'password': '1234'}, follow_redirects=True)
            
            self.assertEqual(session['user_id'], 'new_user')
            self.assertIn('<h1>Create new trip</h1>', result.data)


class CoreListFlaskTests(TestCase):
    """Test core list."""

    def setUp(self):
        """Do before each test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, 'postgresql:///testdb')

        # Create tables and add sample data
        db.create_all()
        example_data()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 'khdouglass'               


    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()


    def test_core_list(self):
        """Test core list display."""

        result = self.client.get('/core_list')
        self.assertIn('Toothpaste', result.data)


    def test_add_core_item(self):
        """Test core item addition, returns json."""

        result = self.client.post('/create_core_list', data={'category': 'Hair Products / Tools', 
                                                             'description': 'Hair brush'})
        self.assertIn('Hair Products', result.data)

    # def test_core_item_removal(self):
    #     """Test core item removal."""

    #     result = self.client.post('/remove_core_item', data={'item_id': '3'})
    #     self.assertIn('Red lipstick', result.data)


class NewTripFlaskTests(TestCase):
    """Test new trip."""

    def setUp(self):
        """Do before each test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, 'postgresql:///testdb')

        # Create tables and add sample data
        db.create_all()
        example_data()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 'khdouglass'               


    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()


    def test_new_trip(self):
        """Test new trip set up."""

        result = self.client.post('/new_trip', data={'location': 'Los Angeles, CA, United States', 
                                                    'trip_name': 'Southern California Trip'})
        self.assertIn('Answer a few questions about your trip to Los Angeles', result.data)


    def test_trip_in_progress(self):
        """Test new_trip route with trip in progress."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess['trip_name'] = 'California vacation'    

            result = self.client.post('/new_trip', data={'location': 'San Diego, CA, United States'})
            self.assertIn('Answer a few questions about your trip to San Diego', result.data)           


    def test_survey(self):
        """Test suvey and suggested list."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess['weather_list'] = [('Tuesday', 'Clear', '79', '58', '/static/img/clear.png'), 
                                        ('Wednesday', 'Partly Cloudy', '74', '59', '/static/img/partlycloudy.png'), 
                                        ('Thursday', 'Partly Cloudy', '68', '58', '/static/img/partlycloudy.png')]    
                sess['location'] = 'Los Angeles, CA, United States'       
                sess['trip_name'] = 'Southern California Trip'    
                sess['trip_id'] = 1

            result = self.client.get('/create_list?num_outfits=2&purpose=Party&formal=yes')
            self.assertIn("You'll need 2 outfits", result.data)


    def test_add_item(self):
        """Test adding items to location visit, returns json."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess['location_id'] = 2
                sess['trip_id'] = 1

            result = self.client.post('/create_list', data={'category': 'Shirt', 
                                                        'description': 'Grey t-shirt', 
                                                        'location': 'Los Angeles, CA, United States'})

            self.assertIn('Grey t-shirt', result.data)

    # def test_item_removal(self):
    #     """Test item removal."""

    #     result = self.client.post('/remove_item', data={'item_id': '1'})
    #     self.assertIn('Black sweater from J.Crew', result.data)

    def test_packing_list(self):
        """Test packing list display."""

        result = self.client.get('/packing_list/California%20vacation', query_string='California vacation')
        self.assertIn('Black sweater from J.Crew', result.data)


    def test_trip_reset(self):
        """Test trip reset."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess['trip_name'] = 'California vacation'

            result = self.client.get('/reset_trip', follow_redirects=True)

            self.assertNotIn('trip_name', session)
            self.assertIn('Create new trip', result.data)


    def test_user_landing_reset(self):
        """Test trip reset on user_landing."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess['trip_name'] = 'California vacation'

            result = self.client.get('/user_landing/khdouglass', query_string='khdouglass')

            self.assertNotIn('trip_name', session)
            self.assertIn('<h1>Create new trip</h1>', result.data)








if __name__ == '__main__':
    import unittest

    unittest.main()