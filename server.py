"""Packing Lists."""

from jinja2 import StrictUndefined
import urllib2
import json
import helper_functions
from random import choice

from flask import Flask, render_template, request, flash, redirect, session, jsonify
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


    return render_template('homepage.html')


@app.route('/register')
def register_form():
    """Show form for user signup."""


    return render_template('register.html')


@app.route('/register', methods=['POST'])
def register_process():
    """Process registration."""

    # get user information from registration form
    user_id = request.form.get('username')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    password = request.form.get('password')

    # create new user, add to db
    new_user = User(user_id=user_id, first_name=first_name, last_name=last_name, 
                    email=email, password=password)
    
    db.session.add(new_user)
    db.session.commit()

    # set user_id in session
    session['user_id'] = user_id

    return redirect('/user_landing/' + user_id)    
    

@app.route('/login', methods=['POST'])
def login():
    """Process login."""

    # get user input
    user_id = request.form.get('username')
    password = request.form.get('password')

    # query db for user_id
    user = db.session.query(User).filter_by(user_id=user_id).first()

    # flash message and redirect if username or password is incorrect
    if user is None:
        flash('User does not exist!')
        return redirect('/')

    if user.password != password:
        flash('Password is incorrect!')
        return redirect('/')

    # set session to user_id
    session['user_id'] = user_id

    return redirect('user_landing/' + user_id)


@app.route('/logout')
def logout():
    """Process logout."""

    del session['user_id']

    return redirect('/')


@app.route('/user_landing/<user_id>')
def user_landing(user_id):
    """Display user landing page."""

    # gtet user's trips to from db to display
    trips = db.session.query(Trip.trip_name).filter_by(user_id=user_id).all()

    # clear session for new trip
    if 'trip_name' in session:
        del session['trip_name']

    return render_template('user_landing.html', trips=trips)


@app.route('/core_list')
def core_list():
    """Create user core packling list."""

    # get user_id from session
    user_id = session['user_id'] 

    # get core list items and categories from db 
    core_list = db.session.query(Item.description, Category.category_name, CoreListItem.core_list_item_id).join(CoreListItem, CoreList, Category).filter(CoreList.user_id==user_id).all()
    categories = db.session.query(Category.category_name).order_by(Category.category_name).all()


    return render_template('create_core_list.html', core_list=core_list, categories=categories)
   

@app.route('/create_core_list', methods=['POST'])
def process_core_list():
    """Add items to user's core packing list."""

    # get user_id from session
    user_id = session['user_id']

    # get core_list_id from db
    core_list_id = db.session.query(CoreList.core_list_id).filter_by(user_id=user_id).first()
    core_list_id = core_list_id[0]

    if core_list_id is None:
        user_core_list = CoreList(user_id=user_id)
        db.session.add(user_core_list)
        db.session.commit()
        core_list_id = user_core_list.core_list_id

    # get user input from form
    item_category = request.form.get('category')
    item_description = request.form.get('description')

    # create new item in db
    new_item = helper_functions.get_new_item(item_category, item_description)

    # create new core item in db
    new_core_item = helper_functions.get_core_item(core_list_id, new_item.item_id)

    # get core list id for core list item
    core_item_id = new_core_item.core_list_item_id
    
    # get item description and category from db
    core_item_details = db.session.query(Item.description, Category.category_name).join(Category, CoreListItem).filter_by(core_list_item_id=core_item_id).one()
    core_item_dict = {}

    # add item info to dictionary
    core_item_dict['core_item_id'] = core_item_id
    core_item_dict['category'] = core_item_details[1]
    core_item_dict['description'] = core_item_details[0]

    # return dictionary in json
    return jsonify(core_item_dict)


@app.route('/remove_core_item')
def remove_core_item():
    """Remove item from location visit list."""

    item_id = request.args.get('item_id')
    
    # get item from db
    item = db.session.query(CoreListItem).filter_by(core_list_item_id=item_id).first()

    # delete item from location_visit_items table
    db.session.delete(item)
    db.session.commit()

    return "Item deleted"


@app.route('/new_trip', methods=['POST'])
def new_trip():
    """Create new trip."""

    # get location and trip name from user entry
    location = request.form.get('location')
    
    # add trip to database if not already in db, return object
    new_trip = helper_functions.get_trip_name()
   
    # add location to database if not already in db, return object
    new_location = helper_functions.get_location(location)

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
    new_weather = helper_functions.get_weather(weather_list, weather_high_avg, weather_low_avg)

    # add location visit to DB
    new_visit = LocationVisit(trip_id=new_trip.trip_id, weather_id=new_weather.weather_id, location_id=new_location.location_id, private=True)
    db.session.add(new_visit)
    db.session.commit()

    # add information to session
    session['location'] = location
    session['weather_list'] = weather_list
    session['location_visit_id'] = new_visit.location_visit_id

    num_location = db.session.query(LocationVisit).filter_by(trip_id = new_trip.trip_id).all()

    # activities for html
    activities = ['Business / Work', 'Party', 'Relaxing', 'Tourism', 'Hiking', 'Skiing',
                  'Working Out', 'Camping', 'Swimming', 'Wedding / Special Event']

    outfits = ['Formal', 'Casual', 'Active', 'Going Out']

    return render_template('new_trip.html', location=location, trip_name=new_trip.trip_name, 
                                            weather_list=weather_list, activities=activities,
                                            outfits=outfits, num_location=num_location)


@app.route('/create_list', methods=['GET'])
def create_list():
    """Create packing list for specified location."""

    # get info from html
    num_formal = request.args.get('Formal')
    num_casual = request.args.get('Casual')
    num_active = request.args.get('Active')
    num_going_out = request.args.get('Going Out')
    num_nights = int(request.args.get('num_nights'))
    flying = request.args.get('flying')
    activities_list = request.args.getlist('purpose')

    outfit_sum = (int(num_formal) + int(num_casual) + int(num_active) + int(num_going_out))

    # get info from session
    weather_list = session['weather_list']
    location = session['location']
    trip_name = session['trip_name']
    trip_id = session['trip_id']
    location = session['location']

    # create new suggeted list instance
    new_list = SuggestedList(location, weather_list, activities_list, num_nights, outfit_sum)
    
    # call suggested list methods
    passport = new_list.need_passport()
    sunglasses = new_list.need_sunglasses()
    jacket = new_list.need_jacket()
    umbrella = new_list.need_umbrella()
    activities_items_list = new_list.activities()
    misc_items = new_list.misc_items()

    # get categories from DB
    categories = db.session.query(Category.category_name).order_by(Category.category_name).all()

    # get current list of trip items
    trip_locations = db.session.query(LocationVisit.location_visit_id).join(Trip).filter_by(trip_name=trip_name).all()
    items = db.session.query(Item.description, LocationVisitItem.location_visit_items_id, Location.location_name, Category.category_name).join(LocationVisitItem, LocationVisit, Category, Location).filter(LocationVisit.location_visit_id.in_(trip_locations)).all()


    return render_template('create_list.html', location=location, flying=flying,
                                               num_formal=num_formal, num_casual=num_casual,
                                               num_active=num_active, num_going_out=num_going_out,
                                               passport=passport, sunglasses=sunglasses,
                                               jacket=jacket, umbrella=umbrella,
                                               categories=categories, trip_name=trip_name,
                                               items=items, activities_items_list = activities_items_list,
                                               misc_items=misc_items)


@app.route('/create_list', methods=['POST'])
def add_item():
    """Add item for location visit to database."""

    # get user input from html
    item_category = request.form.get('category')
    item_description = request.form.get('description')
    item_location = request.form.get('location')

    # query db for id associated with item_category
    category_id = db.session.query(Category.category_id).filter_by(category_name=item_category).one()

    # query db for item matching category and description from user
    new_item = db.session.query(Item).filter_by(category_id=category_id, description=item_description).first()

    # create new item if not in db
    if new_item is None:
        new_item = helper_functions.get_new_item(item_category, item_description)

    # if this is an additional item added to a completed trip list
    if item_location:
        trip_id = session['trip_id']
        # get location_id and location_visit_id from db using trip_id
        location_id = db.session.query(Location.location_id).filter_by(location_name=item_location)
        location_visit_id = db.session.query(LocationVisit.location_visit_id).filter_by(location_id=location_id, trip_id=trip_id).one()
    else:
        location_visit_id = session['location_visit_id']

    #create new location_visit_items instance and add to db.
    new_location_visit_item = LocationVisitItem(location_visit_id=location_visit_id, item_id=new_item.item_id)

    db.session.add(new_location_visit_item)
    db.session.commit()

    # get new item id
    item_id = new_location_visit_item.location_visit_items_id

    # get item details
    item_details = db.session.query(Item.description, Category.category_name).join(Category, LocationVisitItem).filter_by(location_visit_items_id=item_id).one()

    item_dict = {}

    item_dict['location_visit_items_id'] = item_id
    item_dict['category'] = item_details[1]
    item_dict['description'] = item_details[0]
    
    if item_location:
        item_dict['location'] = item_location
    else: 
        item_dict['location'] = session['location']

    return jsonify(item_dict)


@app.route('/remove_item')
def remove_item():
    """Remove item from location visit list."""

    item_id = request.args.get('item_id')
    
    # get item from db
    item = db.session.query(LocationVisitItem).filter_by(location_visit_items_id=item_id).first()

    # delete item from location_visit_items table
    db.session.delete(item)
    db.session.commit()

    return "Item deleted"


@app.route('/packing_list/<trip_name>', methods=['GET'])
def complete_list(trip_name):
    """Display complete packing list for trip."""
    
    user_id = session['user_id']

    trip_id = db.session.query(Trip.trip_id).filter_by(trip_name=trip_name).one()
    location_list = db.session.query(Location.location_name).join(LocationVisit, Trip).filter_by(trip_id=trip_id).all()

    session['trip_id'] = trip_id

    # get list of categories from db
    categories = db.session.query(Category.category_name).order_by(Category.category_name).all()

    # query db for location weather
    location_weather_list = db.session.query(Weather.temperature_high, Weather.temperature_low, WeatherSummary.icon_url, Location.location_name).join(WeatherSummary, LocationVisit, Location).filter(LocationVisit.trip_id==trip_id).all()

    # query db for trip items
    trip_locations = db.session.query(LocationVisit.location_visit_id).join(Trip).filter_by(trip_name=trip_name).all()
    items = db.session.query(Item.description, LocationVisitItem.location_visit_items_id, Location.location_name, Category.category_name).join(LocationVisitItem, LocationVisit, Category, Location).filter(LocationVisit.location_visit_id.in_(trip_locations)).all()
    core_list = db.session.query(Item.description, Category.category_name).join(CoreListItem, CoreList, Category).filter(CoreList.user_id==user_id).all()

    return render_template('packing_list.html', items=items, trip_name=trip_name, core_list=core_list, 
                                                location_weather_list=location_weather_list, categories=categories,
                                                location_list=location_list)


@app.route('/reset_trip')
def reset_trip():
    """Reset session to create new trip."""

    user_id = session['user_id']

    if 'trip_name' in session:
        del session['trip_name']

    return redirect('user_landing/' + user_id)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")













