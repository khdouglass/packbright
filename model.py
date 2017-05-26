"""Models and database functions for Packing List project."""
from flask_sqlalchemy import SQLAlchemy
# import correlation
# from collections import defaultdict

db = SQLAlchemy()

class User(db.Model):
    """User of application."""

    __tablename__ = "users"

    user_id = db.Column(db.String(20), primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)

    trips = db.relationship('Trip', backref='user')

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s email=%s>" % (self.user_id, self.email)


class Trip(db.Model):
    """Trips planned by a user."""

    __tablename__ = "trips"

    trip_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    trip_name = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.String(20),db.ForeignKey('users.user_id'))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Trip trip_id=%s user_id=%s>" % (self.trip_id, self.user_id)


class Location(db.Model):
    """Location visited by a user."""

    __tablename__ = "locations"

    location_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    location_name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Location location_id=%s location_name=%s>" % (self.location_id, self.city_name)


class Image(db.Model):
    """Image displayed for a location."""

    __tablename__ = "images"

    image_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.location_id'))
    month = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(400), nullable=False)
    month_check = db.CheckConstraint(month < 13)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Image image_id=%s location_id=%s>" % (self.image_id, self.location_id)


class LocationVisit(db.Model):
    """Locations visited on a user's trip."""

    __tablename__ = "location_visits"

    location_visit_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.trip_id'))
    weather_id = db.Column(db.Integer, db.ForeignKey('weather.weather_id'))
    location_id = db.Column(db.Integer, db.ForeignKey('locations.location_id'))
    private = db.Column(db.Boolean, default=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Location Visit location_visit_id=%s trip_id=%s>" % (self.location_visit_id, self.trip_id)


class Weather(db.Model):
    """Weather for a user's visit to a location."""

    __tablename__ = "weather"

    weather_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    weather_summary_id = db.Column(db.String(200), db.ForeignKey('weather_summaries.weather_summary_id'))
    temperature_high = db.Column(db.Integer, nullable=False)
    temperature_low = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Weather weather_id=%s>" % (self.weather_id)


class WeatherSummary(db.Model):
    """Weather summary for a user's visit to a location."""

    __tablename__ = "weather_summaries"

    weather_summary_id = db.Column(db.String(30), primary_key=True)
    icon_url = db.Column(db.String(150), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Weather Summary weather_summary_id=%s>" % (self.weather_summary_id)


class LocationVisitItem(db.Model):
    """Items packed for a location visit."""

    __tablename__ = "location_visit_items"

    location_visit_items_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    location_visit_id = db.Column(db.Integer, db.ForeignKey('location_visits.location_visit_id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.item_id'))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Location Visit Item location_visit_items_id=%s location_visit_id=%s item_id=%s>" % (self.location_visit_items_id, 
                                                                                         self.location_visit_id, 
                                                                                         self.item_id)


class CoreList(db.Model):
    """Core packing list for a user."""

    __tablename__ = "core_lists"

    core_list_id = db.Column(db.Integer, autoincrement= True, primary_key=True)
    user_id = db.Column(db.String(20), db.ForeignKey('users.user_id'))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Core List core_list_id=%s user_id=%s>" % (self.core_list_id, self.user_id)


class CoreListItem(db.Model):
    """Items in a user's core packing list."""

    __tablename__ = "core_list_items"

    core_list_item_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    core_list_id = db.Column(db.Integer, db.ForeignKey('core_lists.core_list_id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.item_id'))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Core List Item core_list_item_id=%s core_list_id=%s> item_id:%s" % (self.core_list_item_id, 
                                                                                     self.core_list_id,                                                                                     self.item_id)


class Category(db.Model):
    """Categories items belong to."""

    __tablename__ = "categories"

    category_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    category_name = db.Column(db.String(25), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Category category_id=%s category_name=%s>" % (self.category_id, self.category_name)


class Item(db.Model):
    """Items a user can add to their packling list."""

    __tablename__ = "items"

    item_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'))
    description = db.Column(db.String(100))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Items item_id=%s category_id=%s>" % (self.item_id, self.category_id)

def example_data():
    """Create sample data for testing."""

    Location.query.delete()
    CoreList.query.delete()
    Category.query.delete()
    Item.query.delete()
    CoreListItem.query.delete()
    Trip.query.delete()
    User.query.delete()
    WeatherSummary.query.delete()
    LocationVisit.query.delete()
    LocationVisitItem.query.delete()
    Weather.query.delete()

    user = User(user_id='khdouglass', first_name='Kathryn', last_name='Douglass', email='email@gmail.com', password='1234')
    db.session.add(user)
    db.session.commit()
    
    locations = ['Seattle, WA, United States', 'Los Angeles, CA, United States', 'New York, NY, United States']
    for location in locations:
        new_location = Location(location_name=location)
        db.session.add(new_location)    
    db.session.commit()    

    new_core_list = CoreList(user_id='khdouglass')
    db.session.add(new_core_list)
    db.session.commit()
    
    categories = ['Jeans', 'Pants', 'Shorts', 'Skirts', 'Dress', 'Tank Top', 'Shirt',
                  'Sweater', 'Turtleneck', 'Jacket', 'Shoes', 'Suit', 'Skin Care',
                  'Swimsuit','Socks', 'Undergarments', 'Jewelry', 'Belt', 'Scarf', 
                  'Hair Products / Tools', 'Make Up', 'Tolietries', 'Technology',
                  'Vitamins / Medications', 'Eye Care', 'Hat', 'Activewear',
                  'Outdoor Equipment', 'Misc Items', 'Sleepwear']

    for category in categories:
        new_category = Category(category_name=category)
        db.session.add(new_category)
    db.session.commit()

    items = [(8, 'Black sweater from J.Crew'), (1, 'Light denim flares'), 
             (9, 'Tan turtleneck'), (2, 'Cutoff Levis'), (1, 'Dark skinny jeans'),
             (2, 'Black leggings'), (3, 'Denim shorts'), (3, 'Running shorts'), 
             (4, 'Floral skirt'), (5, 'White ruffle dress'), (5, 'Yellow sundress'),
             (6, 'White ribbed tank'), (7, 'White collared shirt'), (7, 'Black silk blouse'), 
             (10, 'Leather jacket'), (10, 'Trench'), (11, 'Tennis shoes'), (11, 'Sandals'),
             (16, 'Gold bracelet'), (19, 'Headband'), (20, 'Blow dryer'), (21, 'Mascara'), 
             (21, 'Red lipstick'), (22, 'Tootbrush'), (22, 'Toothpaste'), (22, 'Deodorant')]
    for item in items:
        new_item = Item(category_id=item[0], description=item[1])
        db.session.add(new_item)
    db.session.commit()

    core_list_items = [(1, 21), (1, 22), (1, 23), (1, 24), (1, 25), (1, 26)]
    for item in core_list_items:
        new_core_item = CoreListItem(core_list_id=item[0], item_id=item[1])
        db.session.add(new_core_item)

    trips = [('khdouglass', 'California vacation'), ('khdouglass', 'Winter trip to NYC')]
    for trip in trips:
        new_trip = Trip(user_id=trip[0], trip_name=trip[1])
        db.session.add(new_trip)
        db.session.commit()

    images = [('Chance Flurries', '/static/img/chanceflurries.png'), ('Clear', '/static/img/clear.png'), 
              ('Rain', '/static/img/rain.png'), ('Chance of Rain', '/static/img/chancerain.png'), 
              ('Chance of Sleet', '/static/img/chancesleet.png'), ('Chance of Snow', '/static/img/chancesnow.png'),
              ('Chance of a Thunderstorm', '/static/img/chancetstorms.png'), ('Cloudy', '/static/img/cloudy.png'),
              ('Flurries', '/static/img/flurries.png'), ('Fog', '/static/img/fog.png'), ('Hazy', '/static/img/hazy.png'),
              ('Mostly Cloudy', '/static/img/mostlycloudy.png'), ('Mostly Sunny', '/static/img/mostlysunny.png'),
              ('Partly Cloudy', '/static/img/partlycloudy.png'), ('Partly Sunny', '/static/img/partlysunny.png'),
              ('Sleet', '/static/img/sleet.png'), ('Snow', '/static/img/snow.png'), ('Sunny', '/static/img/sunny.png'),
              ('Thunderstorm', '/static/img/tstorms.png'), ('Unknown', '/static/img/unknown.png'), ('Overcast', '/static/img/cloudy.png')]

    for image in images:
        new_image = WeatherSummary(weather_summary_id=image[0], icon_url=image[1])
        db.session.add(new_image)
        db.session.commit()

    new_weather = Weather(weather_summary_id='Clear', temperature_high=72, temperature_low=60)
    db.session.add(new_weather)
    db.session.commit()

    new_visit = LocationVisit(trip_id=1, weather_id=1, location_id=2, private=False)
    db.session.add(new_visit)
    db.session.commit()

    items = [(1, 1), (1, 2), (1, 3), (1, 6), (1, 16), (1, 17), (1, 20)]
    for item in items:
        new_item = LocationVisitItem(location_visit_id=item[0], item_id=item[1])
        db.session.add(new_item)

    db.session.commit()



def connect_to_db(app, db_uri='postgresql:///packing'):
    """Connect the database to our Flask app."""

    # Configure to use PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app

    connect_to_db(app)
    print "Connected to DB."





