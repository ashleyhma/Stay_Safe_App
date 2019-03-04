class EContactChange extends React.Component {
  constructor() {
    super();
    this.state = {
      e_name: '',
      e_number: ''
    };

    this.onENameChange = this.onENameChange.bind(this);
    this.onENumberChange = this.onENumberChange.bind(this);
  }

  alertECChange = (evt) => {
    evt. preventDefault
    $.get('/check-ec-contact.json', this.state, (results) => {
      console.log(results);

      if (results == results.msg) {
        alert("This phone number already exists, please try again");
      } else {
        window.location.replace("/default-form");
      }
    });
  }

  onENameChange(evt){
    console.log(this.state.name)
    this.setState({ e_name: evt.target.value });
  }

  onENumberChange(evt){
    this.setState({ e_number: evt.target.value })
  }

  render() {
    return (
      <div>
        <h1>Change Emergency Contact </h1>
        <form action="/change-emergency-contact" method="POST" id="change_ec_form">

          Emergency Contact Name: 
          <TextInput
            name="e_name"
            id="e_name"
            onChange={this.onENameChange}
            value={this.state.eName}
          /><br/>
          Emergency Contact Number: 
          <TextInput
            name="e_number"
            id="e_number"
            onChange={this.onENumberChange}
            value={this.state.eNumber}
          /><br/><br/>
          <input type="submit" name="submit"/>
        </form>
        <a href="/default-form"> Click here to go back to default form</a>
      </div>
    );
  }
}

ReactDOM.render(
  <EContactChange />,
  document.getElementById('ec_change')
);
