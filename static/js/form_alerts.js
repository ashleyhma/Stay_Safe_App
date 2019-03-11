'use strict';

$('#submit').click(function(){
  const eNumbers = {
      ename: $('#ename').val(),
      enumber: $('#enum').val()
  }

  $.post('/change-emergency-contact', eNumbers, (results) => {
      $('#change_econtact').modal('hide');
  });

  window.location.replace("/default-form");

});

