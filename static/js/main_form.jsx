class Mainform extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      last_details: 'supposed to show last activity',
      last_hour: 'Last Hour',
      last_mins: 'LastMin'
    };

    this.onActivityChange = this.onActivityChange.bind(this)
    this.onHourChange = this.onHourChange.bind(this)
    this.onMinChange = this.onMinChange.bind(this)
  }

  componentDidMount() {
    $.get("/default-form.json", results => {
      console.log(results)
      this.setState({ 
        e_id: results.e_id,
        last_ename: results.last_ename,
        last_enumber: results.last_enumber,
        last_details: results.last_details,
        last_hour: results.last_hours,
        last_mins: results.last_mins
      });
    });
  }

  onActivityChange(evt){
    this.setState({last_details: evt.target.value});
  }

  onHourChange(evt){
    this.setState({last_hour: evt.target.value});
  }

  onMinChange(evt){
    this.setState({last_mins: evt.target.value});
  }

  render() {
    const hours = [];
    for (let i = 0; i < 24; i += 1) {
      hours.push(<option key={i} value={i}>{i}</option>);
    }

    const mins = [];
    for (let i = 0; i < 59; i += 1) {
      mins.push(<option key={i} value={i}>{i}</option>);
    }

    return (
      <div>
        <h1> Please enter your information </h1>
        <h3>If you don't check in, we will alert your default emergency contact:</h3>
        Emergency Contact: { this.state.last_ename} ({ this.state.last_enumber }) <br/> <br/>

          <form action="/returning-user-success" method="POST">
            New Activity:
            <TextInput
              name="details"
              id="details"
              onChange={this.onActivityChange}
              value={this.state.last_details}
              
            />
            <br/><br/>
            HR:
            <select name="hours" value={this.state.last_hour} onChange={this.onHourChange}>
              {hours}
            </select>
            MIN:
            <select name="minutes" value={this.state.last_mins} onChange={this.onMinChange}>
              {mins}
            </select><br/><br/>
            <input type="submit" name="submit"/>
          </form><br/><br/><br/>
        <a href="/change-emergency-contact">Change Emergency Contact Here</a>
      </div>
    );
  }
}


ReactDOM.render(
  <Mainform />,
  document.getElementById('root')
);
