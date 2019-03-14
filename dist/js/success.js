'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var Success = function (_React$Component) {
  _inherits(Success, _React$Component);

  function Success(props) {
    _classCallCheck(this, Success);

    var _this = _possibleConstructorReturn(this, (Success.__proto__ || Object.getPrototypeOf(Success)).call(this, props));

    _this.state = {
      user_name: '',
      number: '',
      e_name: '',
      e_number: '',
      details: '',
      datetime_time: '',
      okay_text: '',
      check_text: '',
      address: ''
    };
    return _this;
  }

  _createClass(Success, [{
    key: 'componentDidMount',
    value: function componentDidMount() {
      var _this2 = this;

      var route = void 0;
      if (this.props.isNewUser === 'True') {
        route = 'new-user-success.json';
      } else {
        route = '/returning-user-success.json';
      }
      $.get(route, function (results) {
        console.log(results);

        _this2.setState({
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
  }, {
    key: 'render',
    value: function render() {
      return React.createElement(
        'div',
        { className: 'info-txt' },
        React.createElement(
          'center',
          null,
          React.createElement(
            'h4',
            null,
            'This will sent to your number (',
            this.state.number,
            ') at ',
            this.state.time,
            ':'
          ),
          this.state.okay_text,
          ' ',
          React.createElement('br', null),
          React.createElement('br', null),
          React.createElement(
            'h4',
            null,
            ' This will be sent to your emergency contact (',
            this.state.e_name,
            ') if you do not respond within 5 min after ',
            this.state.time,
            ':'
          ),
          React.createElement(
            'p',
            { id: 'ec_txt' },
            ' '
          )
        )
      );
    }
  }]);

  return Success;
}(React.Component);

var successEl = document.getElementById('success');

ReactDOM.render(React.createElement(Success, { isNewUser: successEl.dataset.isNewUser }), document.getElementById('success'));