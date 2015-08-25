var $ = require('jquery');
var _ = require('lodash')

function getTopicsForYears(options){
  return $.get(`/topics_for_years/${options.from}/${options.to}`);
}

function getTopicsForYear(options){
  return $.get(`/topics_for_year/${options.year}`);
}

function getTopicsForClass(options){
  var className = options.className.toLowerCase().replace(/ /g, '+');
  return $.get(`/topics_for_class/${className}`);
}

function getClasses(options){
  var category = options && options.category ? options.category : 'arxiv-category';
  return $.get(`/class/${category}`);
}

module.exports = {
  getTopicsForYears,
  getTopicsForYear,
  getTopicsForClass,
  getClasses
};
