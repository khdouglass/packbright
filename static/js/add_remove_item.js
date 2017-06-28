"use strict";

console.log("HERE")

// add outfit to db on submit
function addOutfit(evt) {
    evt.preventDefault();
    console.log('SUBMIT');
    debugger;

    var formInputs = {
        "shirt-category": $($(this).find('.shirt-category')[0]).val(),
        "shirt-description": $($(this).find('.shirt-description')[0]).val(),
        "pants-category": $($(this).find('.pants-category')[0]).val(),
        "pants-description": $($(this).find('.pants-description')[0]).val(),
        "shoes-category": $($(this).find('.shoes-category')[0]).val(),
        "shoes-description": $($(this).find('.shoes-description')[0]).val(),
        "location": $('.item-location').val()
    };
    console.log(formInputs);
    console.log(this);

    $.post("/create_outfits", formInputs);
    $(this).children().fadeTo("fast", 0.4);
    $(this.parentElement).find('.added-response').css("display", "inline-block");
}

$('.new-outfit').on('submit', addOutfit);


// display item after it's added
function displayItem(result) {
    console.log(result.location_visit_items_id);
    $('#packing-list tbody').append(
        '<tr id='+result.location_visit_items_id+'><td>'+result.category+'</td><td>'
        +result.description+'</td><td>'+result.location+'</td><td><div class="remove"><span class="glyphicon glyphicon-remove" aria-hidden="true"></span></div></td></tr>');
}

// add individual item to db
function addItem(evt) {
    evt.preventDefault();

    var formInputs = {
        "category": $('#item-category').val(),
        "description": $('#item-description').val(),
        "location": $('#item-location').val()
    };

    $.post("/add_item", formInputs, displayItem);
    $("#item-description").val("");
}

$('#new-item').on('submit', addItem);


// remove item when displayed in a table
$(document).on('click','.remove',function(){
    var id = $(this).closest('tr').attr("id");        
    $.get('/remove_item', {item_id: id});    
    $(this).closest("tr").remove();
    console.log(id);
    });


// remove item field
$(document).on('click','.remove',function(){
    $(this.parentElement).remove();
    });


// tablesorter functionality
$(document).ready(function() { 
    $('#packing-list').tablesorter({ 
    }); 
});


// functionality for adding suggested items - not currently needed

// function addSuggItem(evt) {
//     evt.preventDefault();
//     var row = $(this).closest("tr");
//     var formInputs = {
//         "category": row.children('td.sugg-item-category')[0].innerHTML,
//         "description": row.find('.sugg-item-description')[0].value,
//     };

//     $.post("/create_list", formInputs, displayItem);
// }

// $('.add').on('click', addSuggItem);

// $(document).on('click','.add',function(){
//     var id = $(this).closest('tr').attr("id");        
//     $.get('/remove_item', {item_id: id});    
//     $(this).closest("tr").remove();
//     console.log(id);
//     });

// tablesorter functionality for suggested items - not currently needed
// $(document).ready(function() { 
//     $('#suggested-items').tablesorter({ 
//         sortList: [[0,0]]
//     }); 
// });
