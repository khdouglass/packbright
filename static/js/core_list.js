"use strict";

console.log("HERE")

$(document).ready(function() { 
    $("#core-list").tablesorter(); 
} 
); 

function displayItem(result) {
    console.log(result.core_item_id);
    $('#core-list tbody').prepend(
        '<tr id='+result.core_item_id+'>'+
        '<td>'+result.category+'</td><td>'+result.description+'</td>'+
        '<td><div class="remove"><span class="glyphicon glyphicon-remove" aria-hidden="true">\
            </span></div></td>');
}

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


$(document).on('click','.remove',function(){
    console.log('hi');
    var id = $(this).closest('tr').attr("id");        
    $.get('/remove_core_item', {item_id: id});    
    $(this).closest("tr").remove();
    console.log(id);

});

