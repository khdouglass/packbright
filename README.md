![](https://github.com/khdouglass/packbright/blob/master/static/img/logo7.png?raw=true "Login Image")

Packbright takes the stress out of preparing for a trip by creating and managing packing lists. 
Users are asked to submit a location and complete a short survey, which informs the app to display 
weather details and generate a list of items to pack. The user can dynamically customize their outfits, 
edit their lists and email completed lists to themselves or other recipients.  Additionally users have 
the option of saving a core list of items to their profile to be included in future trips. Packbright 
stores all past trip data so lists are easily referenced.

## Table of Contents
* [Technologies](#technologies)
* [Features](#features)
* [To Do](#todo)

## <a name="technologies"></a>Technologies
__Backend:__ Python, Flask, PostgreSQL, SQLAlchemy<br>
__Frontend:__ Javascript, jQuery, AJAX, Bootstrap, HTML, CSS<br>
__APIs:__ Google Places, Wunderground, Flickr, SendGrid<br>

## <a name="features"></a>Features
To begin using Packbright, users must log in or create an account. Passwords are hashed with bcrypt 
before they are stored in the database.

![](https://github.com/khdouglass/packbright/blob/master/static/img/homepage.png?raw=true "Homepage")

After logging in, users can view packing lists from previous trips through links on the bottom carousel 
or create a new trip. Locations are autocompleted using the Google Places API.

![](https://github.com/khdouglass/packbright/blob/master/static/img/login.png?raw=true "Log in")

Next, users complete a short survey to provide futher details on their time at a given location. A three 
day forecast is shown using the Wunderground API and a background image of the city is displayed through 
the Flickr API.

![](https://github.com/khdouglass/packbright/blob/master/static/img/survey.png?raw=true "Survey")

Users have the opportunity to customize outfits they would like to pack. Additional items can be 
added individually at the bottom of the page.

![](https://github.com/khdouglass/packbright/blob/master/static/img/add_outfit.png?raw=true "Add outfit")

Users can view their complete packing list for final editing. This list includes items that were automatically 
added based on user survey input and items from a user's core list. Items can be added or removed until the list is 
customized to the user's liking. At that point users can email a copy of the list to themselves or another recipient.

![](https://github.com/khdouglass/packbright/blob/master/static/img/list.png?raw=true "List")

## <a name="todo"></a>To Do

* Suggest popular items from previous trips
* Explore alternate weather APIs and display forecasts for custom dates
* Implement JavaScript testing

## <a name="aboutme"></a>About Me
Hi, my name is Kathryn and I'm a software engineer. Packbright is my first full stack application which I created in four weeks 
as my final project at Hackbright, a 12-week accelerated software engineering fellowship. Feel free to connect on [LinkedIn](http://www.linkedin.com/in/khdouglass)!<br> 