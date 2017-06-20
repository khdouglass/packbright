"use strict";
console.log("HERE")

function sendEmail(evt) {
    evt.preventDefault();

    var formInputs = {
        "email": $('#email').val(),
    };
    console.log(formInputs)

    $.post("/send_email", formInputs);
    $("#email").val("");
    $("#email-sent").css("display", "inline-block");
};

$('#send_email').on('submit', sendEmail);
