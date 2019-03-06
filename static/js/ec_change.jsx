class EContactChange extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      ename: '',
      enumber: ''
    };

    this.onENameChange = this.onENameChange.bind(this);
    this.onENumberChange = this.onENumberChange.bind(this);
  }

  alertECChange = (evt) => {
    evt.preventDefault();
    console.log(this.state);
    $.get('/check-ec-contact.json', this.state, (results) => {
      console.log(results);

      if (results.msg == 'This phone number already exists, please try again') {
        alert("This phone number already exists, please try again");
      } else {
        window.location.replace("/default-form");
      }
    });
  }

  onENameChange(evt){
    console.log(this.state.ename)
    this.setState({ ename: evt.target.value });
  }

  onENumberChange(evt){
    this.setState({ enumber: evt.target.value })
  }

  render() {
    return (
      <div>
        <h1>Change Emergency Contact </h1>
        <form action="/change-emergency-contact" method="POST" id="change_ec_form" onSubmit={this.alertECChange}>

          Emergency Contact Name: 
          <TextInput
            name="ename"
            id="ename"
            onChange={this.onENameChange}
            value={this.state.ename}
          /><br/>
          Emergency Contact Number: 
          <TextInput
            name="enumber"
            id="enumber"
            onChange={this.onENumberChange}
            value={this.state.enumber}
          /><br/><br/>
          <input type="submit" name="Submit"/>
        </form>
        <a href="/default-form"> Click here to go back to default form</a>
      </div>
    );
  }
}

// ReactDOM.render(
//   <EContactChange />,
//   document.getElementById('ec_change')
// );
