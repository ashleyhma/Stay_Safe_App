class TextInput extends React.Component {
  render() {
    return (
      <input
        type="text"
        name={this.props.name}
        id={this.props.id}
        onChange={this.props.onChange}
        value={this.props.value}
      />
    );
  }
}

class Mainform extends React.Component {
  constructor() {
    super(props);
    this.state = {
      inputECName: 'Last EC',
      inputECNum: 'Last EC Num'
      inputActivity: 'Last Activity'
      inputTime: 'Last Time'
    };

    this.onECNameChange = this.onECNameChange.bind(this);
  this.onNumChange = this.onNumChange.bind(this);

  }

  onECNameChange(evt) {
    this.setState({inputECName: evt.target.value});
  }

  onECNumChange(evt) {
    this.setState({inputECNum: evt.target.value});
  }

  onActivityChange(evt) {
    this.setState({inputActivity: evt.target.value});
  }

  onTimeChange(evt) {
    this.setState({inputTime: evt.target.value});
  }

  render() {
    return (
      <div>
        <h1> Default Form </h1>

        <h3>If you don't check in, we will alert your default emergency contact:</h3>
        <h5> ( This is the last used emergency contact )</h5>

        <p>Emergency Contact: {{ last_ename }} ( {{ last_enumber }}) </p><br/>
          <form action="/returning-user-success" method="POST">
            New Activity: 
            <input type="text" name="details" value="{{ last_details }}"><br/>

            HR:
            <select name="hours" id="hours">
              <option value=" {{ hours }}"> {{ hours }} </option>
                {% for i in range(24) %}
                  <option value=" {{ i }} "> {{ i }}</option>  
                {% endfor %}
            </select>
            MIN:
            <select name ="minutes" id="minutes">
              <option value="{{ minutes }}"> {{ minutes }}</option>
                {% for i in range(60) %}
                  <option value=" {{ i }}"> {{ i }}</option>
                {% endfor %}
            </select><br/><br/>
            <input type="submit" name="submit">
          </form><br/><br/><br/>
        <a href="/change-emergency-contact">Change Emergency Contact Here</a>
      </div>

    )
  }

}

  


ReactDOM.render(
    <Mainform />,
    document.getElementById('main')
  );


{/* // import React from 'react';
// import { Button, Form, FormGroup, Label, Input, FormText } from 'reactstrap'; */}

{/* // export default class Example extends React.Component {
//   render() {
//     return (
//       <Form>
//         <FormGroup>
//           <Label for="emergencyContact">Emergency Contact</Label>
//           <Input type="ecName" name="ecName" id="ecName" placeholder="NAME"></Input>
//         </FormGroup>
//         <FormGroup>
//         <Label for="emergencyContactNumber">Emergency Contact Number</Label>
//           <Input type="ecNum" name="ecNum" id="ecNum" placeholder="NUM"></Input>
//         </FormGroup>
//         <FormGroup>
//         <Label for="Activity">Activity</Label>
//           <Input type="activity" name="activity" id="activity" placeholder="ACTIVITY"></Input>
//         </FormGroup>
//         <FormGroup>
//           <Label for="Hour">Hour</Label>
//           <Input type="select" name="hour" id="hour" multiple>
//             <option>1</option>
//             <option>2</option>
//             <option>3</option>
//             <option>4</option>
//             <option>5</option>
//           </Input>
//         </FormGroup>
//         <FormGroup>
//           <Label for="Minutes">Minutes</Label>
//           <Input type="select" name="min" id="min" multiple>
//             <option>1</option>
//             <option>2</option>
//             <option>3</option>
//             <option>4</option>
//             <option>5</option>
//           </Input>
//         </FormGroup>
//       </Form>
//     );
//   }
// } */}