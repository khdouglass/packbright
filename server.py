"""Packing Lists."""

from jinja2 import StrictUndefined

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

    # create new trip -- enter trip name and (first) location.
    # user google map api for location search.
    # key = AIzaSyAzyl6IGlGGmnVCqHiAluta6VfjuGf6Fec
    # see/edit core list.
    # link to view past trips.

    return render_template('user_landing.html')


@app.route('/new_trip')
def new_trip():
    """Create new trip."""

    location = request.args.get('location')
   
    new_location = Location(location_name=location)
    db.session.add(new_location)
    db.session.commit()

    # session["location"] = location

    return render_template('new_trip.html', location=location)


@app.route('/create_list')
def create_list():
    """Create packing list for specified location."""

    # add items to packing list.
    # suggested items displayed separately or in line with the option to "add".

    # option to add another location to your trip or see complete list.

    pass


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













