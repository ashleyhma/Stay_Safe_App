'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var Mainform = function (_React$Component) {
  _inherits(Mainform, _React$Component);

  function Mainform(props) {
    _classCallCheck(this, Mainform);

    var _this = _possibleConstructorReturn(this, (Mainform.__proto__ || Object.getPrototypeOf(Mainform)).call(this, props));

    _this.state = {
      last_details: 'supposed to show last activity',
      last_hour: 'Last Hour',
      last_mins: 'LastMin'
    };

    _this.onActivityChange = _this.onActivityChange.bind(_this);
    _this.onHourChange = _this.onHourChange.bind(_this);
    _this.onMinChange = _this.onMinChange.bind(_this);
    return _this;
  }

  _createClass(Mainform, [{
    key: 'componentDidMount',
    value: function componentDidMount() {
      var _this2 = this;

      $.get("/default-form.json", function (results) {
        console.log(results);
        _this2.setState({
          e_id: results.e_id,
          last_ename: results.last_ename,
          last_enumber: results.last_enumber,
          last_details: results.last_details,
          last_hour: results.last_hours,
          last_mins: results.last_mins
        });
      });
    }
  }, {
    key: 'onActivityChange',
    value: function onActivityChange(evt) {
      this.setState({ last_details: evt.target.value });
    }
  }, {
    key: 'onHourChange',
    value: function onHourChange(evt) {
      this.setState({ last_hour: evt.target.value });
    }
  }, {
    key: 'onMinChange',
    value: function onMinChange(evt) {
      this.setState({ last_mins: evt.target.value });
    }
  }, {
    key: 'render',
    value: function render() {
      var hours = [];
      for (var i = 0; i < 24; i += 1) {
        hours.push(React.createElement(
          'option',
          { key: i, value: i },
          i
        ));
      }

      var mins = [];
      for (var _i = 0; _i < 59; _i += 1) {
        mins.push(React.createElement(
          'option',
          { key: _i, value: _i },
          _i
        ));
      }

      return React.createElement(
        'div',
        { className: 'main' },
        React.createElement(
          'center',
          null,
          React.createElement(
            'h3',
            null,
            ' Going Out? Enter Your Trip Information '
          )
        ),
        React.createElement(
          'form',
          { action: '/returning-user-success', method: 'POST', 'class': 'main_form' },
          React.createElement(
            'b',
            null,
            'Emergency Contact Name'
          ),
          ' ',
          React.createElement('br', null),
          this.state.last_ename,
          React.createElement('br', null),
          ' ',
          React.createElement('br', null),
          React.createElement(
            'b',
            null,
            'Emergency Contact Number'
          ),
          React.createElement('br', null),
          ' ',
          this.state.last_enumber,
          ' ',
          React.createElement('br', null),
          React.createElement('br', null),
          React.createElement(
            'b',
            null,
            'Activity'
          ),
          React.createElement('br', null),
          React.createElement(TextInput, {
            name: 'details',
            id: 'details',
            onChange: this.onActivityChange,
            value: this.state.last_details,
            'class': 'form-control'
          }),
          ' ',
          React.createElement('br', null),
          React.createElement(
            'b',
            null,
            'Text Sent (Military) Time: '
          ),
          ' ',
          React.createElement('br', null),
          React.createElement(
            'select',
            { name: 'hours', value: this.state.last_hour, onChange: this.onHourChange },
            hours
          ),
          React.createElement(
            'select',
            { name: 'minutes', value: this.state.last_mins, onChange: this.onMinChange },
            mins
          ),
          React.createElement('br', null),
          React.createElement('br', null),
          React.createElement('input', { type: 'submit', name: 'submit', 'class': 'btn btn-secondary button-main' })
        )
      );
    }
  }]);

  return Mainform;
}(React.Component);

ReactDOM.render(React.createElement(Mainform, null), document.getElementById('homepage'));