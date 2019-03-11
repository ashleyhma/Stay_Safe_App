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
    evt.preventDefault();
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
      <div className="container">
        <div className="row">
          <div className="col">
        
            </div>
            </div>


            <form action="/" method="POST" id="login-form" onSubmit={this.alertLogin}>
            <div className="row">
              <div className="col-md-5">
                Full Name: <br/>
                <TextInput
                  name="name"
                  id="login-name"
                  onChange={this.onNameChange}
                  value={this.state.name}
                  placeholder="John Doe"
                  class="form-control"
                />
              <br/>
            </div>

            <div className="col-md-5">
              Phone Number:<br/>
              <TextInput
                name="number"
                id="login-number"
                onChange={this.onNumChange}
                value={this.state.number}
                placeholder="5101238888"
                class="form-control"
              />
            </div>
            <br/>
            <div className="col">
              <br/>
              <input className="btn btn-primary" type="submit" name="Submit" id="submit-login-form"/>
            </div>
          </div>

            </form>

        
        </div> 
    );
  }
}


ReactDOM.render(
  <Homepage title="Stay Safe"/>,
  document.getElementById('root')
);