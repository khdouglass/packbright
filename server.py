"""Packing Lists."""

from jinja2 import StrictUndefined
import urllib2
import json

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import (connect_to_db, db, User, Trip, Location, Image, LocationVisit, 
                   Weather, WeatherSummary, LocationVisitItem, CoreList, CoreListItem,
                   Item)


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


@app.route('/new_trip')
def new_trip():
    """Create new trip."""

    session['user_id'] = 'khdouglass'

    # get location and trip name from user entry
    location = request.args.get('location')
    trip_name = request.args.get('trip_name').title()
   
    # add location to database if not already in db
    db_location = db.session.query(Location).filter_by(location_name=location).first()
    if db_location == None:
        new_location = Location(location_name=location)
        db.session.add(new_location)

    # add trip to db
    new_trip = Trip(user_id='khdouglass', trip_name=trip_name)
    db.session.add(new_trip)
    
    db.session.commit()

    # session["location"] = location

    # format location to get weather information from wunderground api
    location = location.split(',')
    location_city = location[0].replace(" ", "_")

    if "United States" in location:
        location_state = location[1][1:]
        url = 'http://api.wunderground.com/api/3e18519d13a0ee9d/forecast/q/{}/{}.json'.format(location_state, location_city)
    else:
        location_country = location[1][1:].replace(" ", "_")
        url = 'http://api.wunderground.com/api/3e18519d13a0ee9d/forecast/q/{}/{}.json'.format(location_country, location_city)

    f = urllib2.urlopen(url)
    json_string = f.read()
    parsed_json = json.loads(json_string)

    weather = []

    for i in range(3):
        forecast_info = parsed_json['forecast']['simpleforecast']['forecastday'][i]
        day = forecast_info['date']['weekday']         
        summary = forecast_info['conditions'] 
        temp_high = forecast_info['high']['fahrenheit']
        temp_low = forecast_info['low']['fahrenheit']
        weather_icon = db.session.query(WeatherSummary.icon_url).filter_by(weather_summary_id=summary).one()
        weather.append((day, summary, temp_high, temp_low, weather_icon[0]))

    f.close()

    occassions = ['Business', 'Party', 'Relaxing', 'Tourism', 'Camping']

    return render_template('new_trip.html', location=location, trip_name=trip_name, 
                                            weather=weather, occassions=occassions)


@app.route('/create_list')
def create_list():
    """Create packing list for specified location."""

    # add items to packing list.
    # suggested items displayed separately or in line with the option to "add".

    # option to add another location to your trip or see complete list.

    return render_template('create_list.html')


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













