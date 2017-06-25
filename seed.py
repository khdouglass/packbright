"""Utility file to seed packing database"""

import datetime
from sqlalchemy import func

from model import User, Trip, Location, LocationVisit, Weather, WeatherSummary, LocationVisitItem, CoreList, CoreListItem, Category, Item, connect_to_db, db
from server import app


def load_users():
    """Load users from into database."""

    print "Users"

    user = User(user_id='khdouglass', first_name='Kathryn', last_name='Douglass', email='email@gmail.com', password='1234')

    db.session.add(user)
    db.session.commit()


def load_trips():
    """Load trips into database"""

    print "Trips"

    trips = [('khdouglass', 'California vacation'), ('khdouglass', 'Winter trip to NYC')]

    for trip in trips:
        new_trip = Trip(user_id=trip[0], trip_name=trip[1])
        db.session.add(new_trip)

    db.session.commit()


def load_locations():
    """Load locations into database."""

    locations = ['Palm Springs, CA, United States', 'New York, NY, United States']

    for location in locations:
        new_location = Location(location_name=location)
        db.session.add(new_location)    

    db.session.commit()

def load_location_visits():
    """Load location visits into database."""

    # add location visits with reference to the trip id, weather id, location id, and privacy setting
    visits = [(1, 1, 1, False), (2, 2, 2, True)]

    for visit in visits:
        new_visit = LocationVisit(trip_id=visit[0], weather_id=visit[1], location_id=visit[2], private=visit[3])
        db.session.add(new_visit)

    db.session.commit()


def load_weather():
    """Load weather data into database."""

    weather = [('Clear', 72, 58), ('Chance Flurries', 40, 32), ('Rain', 55, 43)]

    for item in weather:
        new_weather = Weather(weather_summary_id=item[0], temperature_high=item[1], 
                              temperature_low=item[2])
        db.session.add(new_weather)

    db.session.commit()


def load_weather_summary():
    """Load weather summary icons into database."""

    # need to select icon color and size, save in img file.
    # https://github.com/manifestinteractive/weather-underground-icons/tree/master/dist/icons
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

def load_location_visit_items():
    """Load location visit items into database."""

    # add sample location items referencing the location visit id and item id
    items = [(1, 1), (1, 2), (1, 3), (1, 6), (1, 16), (1, 17), (1, 20),
             (2, 7), (2, 12), (2, 18), (2, 19), (2, 4), (2, 14), (2, 15)]

    for item in items:
        new_item = LocationVisitItem(location_visit_id=item[0], item_id=item[1])
        db.session.add(new_item)

    db.session.commit()    


def load_core_list():
    """Load core list into database."""

    new_core_list = CoreList(user_id='khdouglass')
    db.session.add(new_core_list)
    db.session.commit()


def load_core_list_items():
    """Load core list items into database."""

    # add core packing items with reference to the core list id and item id
    items = [(1, 21), (1, 22), (1, 23), (1, 24), (1, 25), (1, 26)]

    for item in items:
        new_item = CoreListItem(core_list_id=item[0], item_id=item[1])
        db.session.add(new_item)

    db.session.commit()


def load_categories():
    """Load categories into database."""

    categories = ['Jeans', 'Pants', 'Shorts', 'Skirts', 'Dress', 'Tank Top', 'Shirt',
                  'Sweater', 'Jacket', 'Shoes', 'Suit', 'Travel Supplies', 'Accessories',
                  'Swimsuit','Socks', 'Undergarments', 'Jewelry', 'Belt', 'Scarf', 
                  'Hair Products / Tools', 'Make Up', 'Tolietries', 'Technology',
                  'Sleepwear', 'Outdoor Equipment', 'Vitamins / Medications', 'Skin Care',
                  'Hat']

    for category in categories:
        new_category = Category(category_name=category)
        db.session.add(new_category)

    db.session.commit()


def load_items():
    """Load items into database."""

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




if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    load_users()
    load_trips()
    load_locations()
    load_weather_summary()
    load_weather()
    load_categories()
    load_items()
    load_location_visits()
    load_location_visit_items()
    load_core_list()
    load_core_list_items()
    load_images()

    


