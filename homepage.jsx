class Homepage extends React.Component {
    checkPhoneNumber() {
        fetch('/check-phone-num.json')
      .then(response => response.json())
      .then(data => alert(`The weather will be ${data.forecast}`));
    }

    onSubmitForm(e) {
        // call check phone number
        // what happens when you submit?
    }

  render() {
    return (
        <div> 
        <h1> Let's Keep Each Other Safe </h1>

<h5> Enter your information here if you have registered before:</h5>
<p class="form">


    <form action="/" method="POST" id="login-form">
        
            Enter Full Name: 
            <br>
            <input type="text" name="name" id="name">
            <br>

        
            Phone Number:
            <br>
            <input type="text" name="number" id="number">
            <br>

            <input type="submit" name="Submit" id="submit-login-form">
    </form>
</p>

<p> <a href="/register-form">Click here to register!</a></p>
    </div>
    );
  }
}