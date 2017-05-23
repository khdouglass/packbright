    
from flask import Flask, render_template, request, flash, redirect, session, jsonify
from model import (connect_to_db, db, User, Trip, Location, Image, LocationVisit, 
                   Weather, WeatherSummary, LocationVisitItem, CoreList, CoreListItem,
                   Item, Category)


def get_new_item(item_category, item_description):
    """Create new_item in db, if one does not alreay exist."""

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

#create new core_list_items instance
def get_core_item(core_list_id, item_id):
    """Create new core list item in db."""

    new_core_item = CoreListItem(core_list_id=core_list_id, item_id=item_id)
    db.session.add(new_core_item)
    db.session.commit()

    return new_core_item
