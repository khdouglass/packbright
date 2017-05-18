"""Packing Lists."""

from jinja2 import StrictUndefined
import urllib2
import json
from random import choice

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import (connect_to_db, db, User, Trip, Location, Image, LocationVisit, 
                   Weather, WeatherSummary, LocationVisitItem, CoreList, CoreListItem,
                   Item, Category)
from support_classes import SuggestedList


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    #sign in option
    #register option

    pass

@app.route('/register', methods=['GET'])
def register_form():
    """Show form for user signup."""

    # show form to register new user.

    pass


@app.route('/register', methods=['POST'])
def register_process():
    """Process registration."""

    # process new user registration.

    pass

@app.route('/login', methods=['POST'])
def login():
    """Process login."""

    # process user login.

    pass

@app.route('/logout')
def logout():
    """Process logout."""

    # process user logout.

    pass

@app.route('/user_landing', methods=['GET'])
def user_landing():
    """Display user landing page."""

    # see/edit core list.
    # link to view past trips.
    trips = db.session.query(Trip.trip_name).filter_by(user_id='khdouglass').all()

    return render_template('user_landing.html', trips=trips)

@app.route('/core_list')
def core_list():
    """Create user core packling list."""

    # query db for user's core list
    core_list_id = db.session.query(CoreList.core_list_id).filter_by(user_id='khdouglass').one()

    # create user's core list in db
    if core_list_id is not None:
        core_list = db.session.query(Item.description, Category.category_name).join(CoreListItem, CoreList, Category).filter(CoreList.user_id=='khdouglass').all()

        return render_template('core_list.html', core_list=core_list)
    else:
        trip_name = session['trip_name']

        # get categories from DB
        categories = db.session.query(Category.category_name).order_by(Category.category_name).all()

        return render_template('create_core_list.html', categories=categories, trip_name=trip_name)


@app.route('/create_core_list', methods=['POST'])
def process_core_list():
    """Add items to user's core packing list."""

        
    # else:
    #     core_list_id = CoreList(user_id='khdouglass')
    #     db.session.add(core_list_id)
    #     db.session.commit()


    # get user input from html
    item_category = request.form.get('category')
    item_description = request.form.get('description')

    # query db for id associated with item_category
    category_id = db.session.query(Category.category_id).filter_by(category_name=item_category).one()

    # query db for item matching category and description from user
    new_item = db.session.query(Item).filter_by(category_id=category_id, description=item_description).first()

    # create new item if not in db
    if new_item is None:
        new_item = Item(category_id=category_id, description=item_description)
        db.session.add(new_item)
        db.session.commit()

    #create new core_list_items instance
    core_list_item = CoreListItem(core_list_id=core_list_id, item_id=new_item.item_id)
    db.session.add(core_list_item)

    db.session.commit()

    return "Item added"


@app.route('/new_trip')
def new_trip():
    """Create new trip."""

    # get location and trip name from user entry
    location = request.args.get('location')
    
    # if trip name already in session, keep it
    if 'trip_name' in session:
        trip_name = session['trip_name']
        new_trip = db.session.query(Trip).filter_by(trip_name=trip_name, user_id='khdouglass').one()
    else:
        # if not, get name from html and add to db
        trip_name = request.args.get('trip_name')
        new_trip = Trip(user_id='khdouglass', trip_name=trip_name)
        db.session.add(new_trip)
   
    # add location to database if not already in db
    db_location = db.session.query(Location).filter_by(location_name=location).first()
    if db_location is None:
        new_location = Location(location_name=location)
        db.session.add(new_location)
    else:
        new_location = db_location

    # format location to get weather information from wunderground api
    location = location.split(',')
    location_city = location[0].replace(" ", "_")

    # format wunderground api url 
    if "United States" in location:
        location_state = location[1][1:]
        url = 'http://api.wunderground.com/api/3e18519d13a0ee9d/forecast/q/{}/{}.json'.format(location_state, location_city)
    else:
        location_country = location[1][1:].replace(" ", "_")
        url = 'http://api.wunderground.com/api/3e18519d13a0ee9d/forecast/q/{}/{}.json'.format(location_country, location_city)

    f = urllib2.urlopen(url)
    json_string = f.read()
    parsed_json = json.loads(json_string)

    weather_list = []
    weather_high_avg = 0
    weather_low_avg = 0

    # store weather information for location in weather_list
    for i in range(3):
        forecast_info = parsed_json['forecast']['simpleforecast']['forecastday'][i]
        day = forecast_info['date']['weekday']         
        summary = forecast_info['conditions'] 
        temp_high = forecast_info['high']['fahrenheit']
        temp_low = forecast_info['low']['fahrenheit']
        weather_icon = db.session.query(WeatherSummary.icon_url).filter_by(weather_summary_id=summary).one()
        weather_list.append((day, summary, temp_high, temp_low, weather_icon[0]))
        weather_high_avg += int(temp_high)
        weather_low_avg += int(temp_low)

    f.close()

    # add weather details to DB
    new_weather = Weather(weather_summary_id=weather_list[2][1], temperature_high=(weather_high_avg / 3), 
                              temperature_low=(weather_low_avg / 3))
    db.session.add(new_weather)
    db.session.commit()

    # add location visit to DB
    new_visit = LocationVisit(trip_id=new_trip.trip_id, weather_id=new_weather.weather_id, location_id=new_location.location_id, private=True)
    db.session.add(new_visit)

    db.session.commit()

    # add information to session
    session['user_id'] = 'khdouglass'
    session['location'] = location
    session['weather_list'] = weather_list
    session['trip_name'] = trip_name
    session['location_visit_id'] = new_visit.location_visit_id

    # occassions for html
    occassions = ['Business', 'Party', 'Relaxing', 'Tourism', 'Camping']

    return render_template('new_trip.html', location=location, trip_name=trip_name, 
                                            weather_list=weather_list, occassions=occassions)


@app.route('/create_list', methods=['GET'])
def create_list():
    """Create packing list for specified location."""

    # get info from html
    num_outfits = request.args.get('num_outfits')
    purpose = request.args.get('purpose')
    formal = request.args.get('formal') 

    # get info from session
    weather_list = session['weather_list']
    location = session['location']
    trip_name = session['trip_name']

    # create new suggeted list instance
    new_list = SuggestedList(num_outfits, location, weather_list)
    
    # call suggested list methods
    passport = new_list.need_passport()
    sunglasses = new_list.need_sunglasses()
    jacket = new_list.need_jacket()
    umbrella = new_list.need_umbrella()

    # get categories from DB
    categories = db.session.query(Category.category_name).order_by(Category.category_name).all()

    return render_template('create_list.html', num_outfits=num_outfits, 
                                               purpose=purpose, formal=formal,
                                               passport=passport, sunglasses=sunglasses,
                                               jacket=jacket, umbrella=umbrella,
                                               categories=categories, trip_name=trip_name)


@app.route('/create_list', methods=['POST'])
def add_item():
    """Add item to list for location visit to database."""

    # get user input from html
    item_category = request.form.get('category')
    item_description = request.form.get('description')

    # query db for id associated with item_category
    category_id = db.session.query(Category.category_id).filter_by(category_name=item_category).one()

    # query db for item matching category and description from user
    new_item = db.session.query(Item).filter_by(category_id=category_id, description=item_description).first()

    # create new item if not in db
    if new_item is None:
        new_item = Item(category_id=category_id, description=item_description)
        db.session.add(new_item)
        db.session.commit()

    # get location id from session
    location_visit_id = session['location_visit_id']

    #create new location_visit_items instance
    new_location_visit_item = LocationVisitItem(location_visit_id=location_visit_id, item_id=new_item.item_id)
    db.session.add(new_location_visit_item)

    db.session.commit()

    return "Item added"


@app.route('/packing_list/<trip_name>', methods=['GET'])
def complete_list(trip_name):
    """Display complete packing list for trip."""
    
    # retrieve trip from session
    if 'trip_name' in session:
        trip_name = session['trip_name']

    trip_id = db.session.query(Trip.trip_id).filter_by(trip_name=trip_name).one()

    # query db for location weather
    location_weather_list = db.session.query(Weather.temperature_high, Weather.temperature_low, WeatherSummary.icon_url, Location.location_name).join(WeatherSummary, LocationVisit, Location).filter(LocationVisit.trip_id==trip_id).all()

    # query db for trip items
    trip_locations = db.session.query(LocationVisit.location_visit_id).join(Trip).filter_by(trip_name=trip_name).all()
    items = db.session.query(Item.description, Location.location_name, Category.category_name).join(LocationVisitItem, LocationVisit, Category, Location).filter(LocationVisit.location_visit_id.in_(trip_locations)).all()
    core_list = db.session.query(Item.description, Category.category_name).join(CoreListItem, CoreList, Category).filter(CoreList.user_id=='khdouglass').all()

    return render_template('packing_list.html', items=items, trip_name=trip_name, core_list=core_list, location_weather_list=location_weather_list)


@app.route('/reset_trip')
def reset_trip():
    """Reset session to create new trip."""

    del session['trip_name']

    return redirect('/user_landing')


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")













