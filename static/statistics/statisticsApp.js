import React from 'react';
import _ from 'lodash';
import CategoryList from './components/categoryList';
import CategoryContainer from './components/categoryContainer';
import LoadingScreen from './components/loadingScreen'

import Api from './api';
import CategoryStore from './stores/categoryStore';
import CategoryActions from './actions/categoryActions';

var StatisticsApp = React.createClass({
  getInitialState(){
    return CategoryStore.getAll();
  },

  componentDidMount(){
    let component = this;

    CategoryStore.addChangeListener(this._onChange);
    CategoryActions.loadCategories();
  },

  componentWillUnMount(){
    CategoryStore.removeChangeListener(this._onChange);
  },

  render(){
    return (
      <div>
        <LoadingScreen loading={this.state.loadingTopics} />
        <div id="statistics-container">
          <CategoryContainer category={this.state.chosenCategory} years={this.state.years} loading={this.state.loadingTopics} />
          <CategoryList categories={this.state.categories} activeCategory={this.state.chosenCategory} onClick={CategoryActions.setCategory} />
        </div>
      </div>
    );
  },

  _onChange(){
    console.log(CategoryStore.getAll());
    this.setState(CategoryStore.getAll());
  }
});

React.render(
  <StatisticsApp/>,
  document.getElementById('root')
)

export default StatisticsApp;
