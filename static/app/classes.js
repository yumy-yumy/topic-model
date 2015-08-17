var handlebars = require('handlebars');
var $ = require('jquery');
var _ = require('lodash');

var templateHTML = `
  <ul class="list-unstyled">
    <% classes.forEach(function(className){ %>
      <li>
        <a href="#/topics/<%= year %>/classes/<%= className %>" class="<% if(selectedClass == className){ %>selected<% } %>">
          <%= className %>
        </a>
      </li>
    <% }) %>
  </ul>
`;

var template = _.template(templateHTML);

module.exports = (options) => {
  options.target.innerHTML = template({ year: options.year, classes: options.classes, selectedClass: options.selectedClass });
};
