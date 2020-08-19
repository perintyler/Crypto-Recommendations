import React from 'react';
import '../stylesheets/navbar.style.css';
import PropTypes from 'prop-types';
class Navbar extends React.Component {

  static defaultProps = {items: []}

  static propTypes = {
    items: PropTypes.array
  }

  get_item_elements() {
    return this.props.items.map(item => {
      return <li><a href={item.link}>{item.title}</a></li>;
    });
  }

  render() {
    return (
      <div id="navbar">
        <h1>{ this.props.children }</h1>
        <ul>{ this.get_item_elements() }</ul>
      </div>
    )
  }
}

export default Navbar;
