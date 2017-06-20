    
from flask import Flask, render_template, request, flash, redirect, session, jsonify
from model import (connect_to_db, db, User, Trip, Location, Image, LocationVisit, 
                   Weather, WeatherSummary, LocationVisitItem, CoreList, CoreListItem,
                   Item, Category)


def get_new_item(item_category, item_description):
    """Create item in db, if it does not already exist."""

    # query db for id associated with item_category
    category_id = db.session.query(Category.category_id).filter_by(category_name=item_category).one()

    # query db for item matching category and description from user
    new_item = db.session.query(Item).filter_by(category_id=category_id, description=item_description).first()

    # create new item if not in db
    if new_item is None:
        new_item = Item(category_id=category_id, description=item_description)
        db.session.add(new_item)
        db.session.commit()

    return new_item


def get_core_item(core_list_id, item_id):
    """Create new core list item in db."""

    new_core_item = CoreListItem(core_list_id=core_list_id, item_id=item_id)
    db.session.add(new_core_item)
    db.session.commit()

    return new_core_item
    

def get_trip_name():
    """Create new trip in db, if one does not already exist."""

    user_id = session['user_id']

    if 'trip_name' in session:
        trip_name = session['trip_name']
        new_trip = db.session.query(Trip).filter_by(trip_name=trip_name, user_id=user_id).one()
    else:
        # if not, get name from html and add to db
        trip_name = request.form.get('trip_name')
        new_trip = Trip(user_id=user_id, trip_name=trip_name)
        db.session.add(new_trip)
        session['trip_name'] = trip_name

    return new_trip


def get_location(location):
    """Create new location in db, if one does not already exist."""

    db_location = db.session.query(Location).filter_by(location_name=location).first()
    if db_location is None:
        new_location = Location(location_name=location)
        db.session.add(new_location)
    else:
        new_location = db_location

    return new_location


def get_weather(weather_list, weather_high_avg, weather_low_avg):
    """Add weather summary in db."""

    new_weather = Weather(weather_summary_id=weather_list[2][1], temperature_high=(weather_high_avg / 3), 
                              temperature_low=(weather_low_avg / 3))
    db.session.add(new_weather)
    db.session.commit()

    return new_weather
