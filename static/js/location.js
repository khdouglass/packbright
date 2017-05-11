"use strict";


var input = document.getElementById('autocomplete');
var autocomplete = new google.maps.places.Autocomplete(input, {types: ['(cities)']});


google.maps.event.addListener(autocomplete, 'place_changed', function(){
 var place = autocomplete.getPlace();
// $.get('/process_location', place, routeNewTrip)
console.log(place);
});

// function routeNewTrip (results) {
//     console.log("results");
// };

// var place = autocomplete.getPlace();
// console.log(place)

// $.post('/new_trip', place)

// function getLocation() {
//   google.maps.event.addListener(autocomplete, 'place_changed', function() {
//     var place = autocomplete.getPlace();
//     console.log(place)
//     $.post('/user_landing', place);
//   })
//   };

// $('#submit_location').on('submit', getLocation);


