class Homepage extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      name: '',
      number: '',
    };

    this.onNameChange = this.onNameChange.bind(this);
    this.onNumChange = this.onNumChange.bind(this);
  }

  alertLogin = (evt) => {
    evt.preventDefault
    $.get('/check-phone-num.json', this.state, (results) => {
      console.log(results);
      if (results.msg == 'name not with number'){
        
        alert("This phone is registered to another name, please try again!");
      } else if (results.msg == 
        'not registered'){
        
        alert("We do not have your number registered. Please register!");
      } else if (results.msg == 'okay'){
    
        window.location.replace("/default-form")
        console.log(evt.target);
      } 
  });
  }

  onNameChange(evt) {
    console.log(this.state.name)
    this.setState({ name: evt.target.value });
  }

  onNumChange(evt) {
    console.log(this.state.number)
    this.setState({ number: evt.target.value });
  }

  render() {
    // console.log(this.props)
    return (
      <div> 
        <h1>{this.props.title}</h1>
        {console.log(this.props)}
        

        <h5> Enter your information here if you have registered before:</h5>
          
          <form action="/" method="POST" id="login-form" onSubmit={this.alertLogin}>
            Enter Full Name: <br/>
            <TextInput
              name="name"
              id="login-name"
              onChange={this.onNameChange}
              value={this.state.name}
            />
            <br/>
            Phone Number:<br/>
            <TextInput
              name="number"
              id="login-number"
              onChange={this.onNumChange}
              value={this.state.number}
            />
            <br/>
            
            <input type="submit" name="Submit" id="submit-login-form"/>
          </form>
        

        <p><a href="/register-form">Click here to register!</a></p>
      </div>
    );
  }
}


ReactDOM.render(
  <Homepage title="Stay Safe"/>,
  document.getElementById('root')
);