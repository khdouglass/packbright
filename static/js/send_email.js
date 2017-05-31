"use strict";

function sendEmail(evt) {
    evt.preventDefault();

    var formInputs = {
        "email": $('#email').val(),
    };

    $.post("/send_email", formInputs);
    $("#email").val("");
};

$('#send_email').on('submit', sendEmail);
