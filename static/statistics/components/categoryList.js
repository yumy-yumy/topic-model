import React from 'react';

var CategoryList = React.createClass({
  propTypes(){
    return {
      categories: React.propTypes.array.isRequired,
      activeCategory: React.propTypes.string,
      onClick: React.propTypes.func
    }
  },

  getDefaultProps(){
    return {
      activeCategory: ''
    }
  },

  renderLinks(){
    return this.props.categories.map(category => {
      let classes = category === this.props.activeCategory ? 'active' : '';

      return (
        <li className={classes}>
          <a style={{ cursor: 'pointer' }} onClick={this.props.onClick.bind(this, category)}>{category}</a>
        </li>
      )
    });
  },

  render(){
    let links = this.renderLinks();

    return (
      <div id="category-list" style={{ borderLeft: '1px solid rgb(220,220,220)'}}>
        <h4>Categories ({this.props.categories.length})</h4>
        <ul className="nav nav-pills nav-stacked" id="category-links">
          {links}
        </ul>
      </div>
    );
  }
});

export default CategoryList;
