"use strict";

console.log("HERE")

// tablesorter functionality 
$(document).ready(function() { 
    $("#core-list").tablesorter(); 
} 
); 

// display items as they're manually added
function displayItem(result) {
    console.log(result.core_item_id);
    $('#core-list tbody').prepend(
        '<tr id='+result.core_item_id+'>'+
        '<td>'+result.category+'</td><td>'+result.description+'</td>'+
        '<td><div class="remove"><span class="glyphicon glyphicon-remove" aria-hidden="true">\
            </span></div></td>');
}

// add indivudial items to db as they're manually added
function addItem(evt) {
    evt.preventDefault();

    var formInputs = {
        "category": $('#item-category').val(),
        "description": $('#item-description').val()
    };

    $.post("/create_core_list", formInputs, displayItem);
    $("#item-description").val("");

}

$('#new-item').on('submit', addItem);

// remove items manually
$(document).on('click','.remove',function(){
    console.log('hi');
    var id = $(this).closest('tr').attr("id");        
    $.get('/remove_core_item', {item_id: id});    
    $(this).closest("tr").remove();
    console.log(id);

});

