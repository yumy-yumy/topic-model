var $ = require('jquery');
var _ = require('lodash')

function getTopicsForYears(options){
  return $.get('/topics_for_years', _.pick(options, 'from', 'to'));
}

module.exports = {
  getTopicsForYears
}
