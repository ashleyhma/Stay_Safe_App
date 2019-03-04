class Success extends React.Component {
  constructor() {
    super(props);
    this.state = {
      user_name: '',
      number: '',
      e_name: '',
      e_number: '',
      details: '',
      datetime_time: '',
      okay_text: '',
      check_text: '',
      GOOGLE_KEY: '',
      address: ''
    }
  }
  
  componentDidMount() {
    $.get("/returning-user-success.json", results => {
      console.log(results)
      this.setState({
        user_name: results.user_name,
        number: results.number,
        e_name: results.e_name,
        e_number: results.e_number,
        details: results.details,
        datetime_time: results.datetime_time,
        okay_text: results.okay_text,
        check_text: results.check_text,
        GOOGLE_KEY: results.GOOGLE_KEY,
        address: results.address
      });
    });
  }

  render() {
    return(
      <div>
      <h1> Thank you for using Stay Safe! </h1>

      <p> <h3>Make sure you entered the right information! This is what we have: </h3>
        Your Number: { this.state.number }
        <br/>
        Emergency Contact: { this.state.e_name }
        <br/>
        Emergency Contact Number: { this.state.e_number }
        <br/>
        Check Time: { this.state.datetime_time }
      </p>
      
      
      <p> <h4>This is the text that we will send you at { this.state.datetime_time }:</h4>
        { this.state.okay_text }
      </p>
      <p> <h4> This is the text that will send to your emergency contact if you do not respond 5 min after { this.state.datetime_time }:</h4>
          { this.state.check_text }
      </p>
      
      </div>
    );
  }
}

ReactDOM.render(
  <Success />,
  docuument.getElementById('success')
);

