'use strict';


$('#login-form').on('submit', (evt) => {
  console.log("hello");
  evt.preventDefault();

  const phoneNumbers = {
    name: $('#name').val(),
    number: $('#number').val()
  };
  // console.log(phoneNumbers.name);
  // console.log(phoneNumbers.number);

  $.get('/check-phone-num.json', phoneNumbers, (results) => {
      console.log(results);
      if (results.msg == 'name not with number'){
        // evt.preventDefault();
        alert("This phone is registered to another name, please try again!");
      } else if (results.msg == 
        'not registered'){
        // evt.preventDefault();
        alert("We do not have your number registered. Please register!");
      } else if (results.msg == 'okay'){
        // $(evt.target).submit();
        window.location.replace("/default-form")
        console.log(evt.target);
      } 

  });
});

$('#change_ec_form').on('submit', (evt) => {
  evt.preventDefault();

  const eNumbers = {
    ename: $('#ename').val(),
    enumber: $('#enumber').val()
  }
  $.get('/check-ec-contact.json', eNumbers, (results) => {
    console.log(results.emsg);
    if (results.emsg == 'existing'){
      alert("This phone number already exists, please try again");
    } else {
      window.location.replace("/default-form");

    }
    
  });
});

