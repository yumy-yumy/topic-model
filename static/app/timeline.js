var handlebars = require('handlebars');
var $ = require('jquery');

var templateHTML = `
  <ul class="timeline">
    {{#each labels}}
      <li class="timeline-item">
        <a href="#" class="year-trigger" data-year="{{this}}">{{this}}</a>
      </li>
    {{/each}}
  </ul>
`;

var template = handlebars.compile(templateHTML);

module.exports = (options) => {
  options.target.innerHTML = template({ labels: options.labels });

  var $ul = $(options.target).find('ul');

  $ul.css('width', `${options.width}px`);
  $ul.find('.timeline-item').css('width', `${options.itemWidth}px`);
};
