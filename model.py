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
    weather_summary_id = db.Column(db.String(20), db.ForeignKey('weather_summaries.weather_summary_id'))
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

        return "<Location Visit Item location_visit_item_id=%s location_visit_id=%s item_id=%s>" % (self.location_visit_item_id, 
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


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///packing'
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





