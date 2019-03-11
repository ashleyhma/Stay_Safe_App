class Success extends React.Component {
  constructor(props) {
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
      address: ''
    }
  }
  
  componentDidMount() {
    let route;
    if (this.props.isNewUser === 'True') {
      route = 'new-user-success.json';
    } else {
      route = '/returning-user-success.json';
    }
    $.get(route, results => {
      console.log(results)

      this.setState({
        user_name: results.user_name,
        number: results.number,
        e_name: results.e_name,
        e_number: results.e_number,
        time: moment(results.time, 'H:m').format('H:mm A'),
        details: results.details,
        okay_text: results.okay_text,
        check_text: results.check_text
      });
    });
  }

  render() {
    return(

      <div>
       
          <h3>Make sure you entered the right information! This is what we have: </h3>
          Your Number: { this.state.number } <br/>
          Emergency Contact: { this.state.e_name } <br/>
          Emergency Contact Number: { this.state.e_number } <br/>

          <h4>This will sent to you at { this.state.time }:</h4>
          { this.state.okay_text } <br/>

          <h4> This will be sent to your emergency contact if you do not respond within 5 min after { this.state.time }:</h4>
          
          <p id="ec_txt"> </p> 
        
      </div>
    );
  }
}

const successEl = document.getElementById('success');

ReactDOM.render(
  <Success isNewUser={successEl.dataset.isNewUser}/>,
  document.getElementById('success')
);

