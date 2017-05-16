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

    return render_template('user_landing.html')

@app.route('/core_list')
def core_list():
    """Create user core packling list."""

    pass


@app.route('/new_trip')
def new_trip():
    """Create new trip."""

    # get location and trip name from user entry
    location = request.args.get('location')
    trip_name = request.args.get('trip_name')
   
    # add location to database if not already in db
    db_location = db.session.query(Location).filter_by(location_name=location).first()
    if db_location is None:
        new_location = Location(location_name=location)
        db.session.add(new_location)
    else:
        new_location = db_location

    # add trip to db
    new_trip = Trip(user_id='khdouglass', trip_name=trip_name)
    db.session.add(new_trip)

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

    # add information to session
    session['user_id'] = 'khdouglass'
    session['location'] = location
    session['weather_list'] = weather_list

    # add weather details to DB
    new_weather = Weather(weather_summary_id=weather_list[2][1], temperature_high=(weather_high_avg / 3), 
                              temperature_low=(weather_low_avg / 3))
    db.session.add(new_weather)
    db.session.commit()

    # add location visit to DB
    new_visit = LocationVisit(trip_id=new_trip.trip_id, weather_id=new_weather.weather_id, location_id=new_location.location_id, private=True)
    db.session.add(new_visit)

    db.session.commit()

    # occassions for html
    occassions = ['Business', 'Party', 'Relaxing', 'Tourism', 'Camping']

    return render_template('new_trip.html', location=location, trip_name=trip_name, 
                                            weather_list=weather_list, occassions=occassions)


@app.route('/create_list', methods=['GET'])
def create_list():
    """Create packing list for specified location."""

    # add items to packing list.
    # suggested items displayed separately or in line with the option to "add".
    # option to add another location to your trip or see complete list.

    # get info from html
    num_outfits = request.args.get('num_outfits')
    purpose = request.args.get('purpose')
    formal = request.args.get('formal') 

    # get info from session
    weather_list = session['weather_list']
    location = session['location']

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
                                               categories=categories)


@app.route('/create_list', methods=['POST'])
def add_item():
    """Add item to list for location visit to database."""

    item_category = request.form.get('category')
    item_description = request.form.get('description')

    print item_category
    print item_description

    # new_item = db.session.query(Item).filter_by(category_id=item_category, description=item_description).first()
    # if new_item is None:
    new_item = Item(category_id=item_category, description=item_description)
    db.session.add(new_item)
    # else:
    #     new_item = new_item

    db.session.commit()

    print new_item
    return "Item added"


@app.route('/complete_list')
def complete_list():
    """Display complete packing list for trip."""

    # include core items.
    # option of viewing items by location or by category.

    pass


@app.route('/past_trips')
def past_trips():
    """Display user's past trips."""

    # list of past trips information.

    pass



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")













