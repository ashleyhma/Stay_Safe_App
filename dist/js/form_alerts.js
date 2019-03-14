'use strict';

$('#submit').click(function () {
    var eNumbers = {
        ename: $('#ename').val(),
        enumber: $('#enum').val()
    };

    $.post('/change-emergency-contact', eNumbers, function (results) {
        $('#change_econtact').modal('hide');
    });

    window.location.replace("/default-form");
});