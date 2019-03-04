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