"use strict";

console.log("HERE")

/*
hgggghghhg
*/
function addOutfit(evt) {
    evt.preventDefault();
    console.log('SUBMIT');

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


function displayItem(result) {
    console.log(result.location_visit_items_id);
    $('#packing-list tbody').append(
        '<tr id='+result.location_visit_items_id+'><td>'+result.category+'</td><td>'
        +result.description+'</td><td>'+result.location+'</td><td><div class="remove">X</div></td></tr>');
}

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

function addSuggItem(evt) {
    evt.preventDefault();
    var row = $(this).closest("tr");
    var formInputs = {
        "category": row.children('td.sugg-item-category')[0].innerHTML,
        "description": row.find('.sugg-item-description')[0].value,
    };

    $.post("/create_list", formInputs, displayItem);
}

$('.add').on('click', addSuggItem);

// $(document).on('click','.add',function(){
//     var id = $(this).closest('tr').attr("id");        
//     $.get('/remove_item', {item_id: id});    
//     $(this).closest("tr").remove();
//     console.log(id);
//     });


$(document).on('click','.remove',function(){
    var id = $(this).closest('tr').attr("id");        
    $.get('/remove_item', {item_id: id});    
    $(this).closest("tr").remove();
    console.log(id);
    });

$(document).on('click','.delete',function(){
    // debugger;       
    $(this.parentElement).remove();
    });


$(document).ready(function() { 
    $('#packing-list').tablesorter({ 
    }); 
});

$(document).ready(function() { 
    $('#suggested-items').tablesorter({ 
        sortList: [[0,0]]
    }); 
});
