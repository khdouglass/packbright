"use strict";

function sendEmail(evt) {
    evt.preventDefault();

    var formInputs = {
        "email": $('#email').val(),
    };

    $.post("/send_email", formInputs);
    $("#email").val("");
    $("#email-sent").css("display", "inline-block");
    // $('#email-btn').prop("disabled",true);
};

$('#send_email').on('submit', sendEmail);
