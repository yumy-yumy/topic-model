var Handlebars = require('handlebars');
var Chart = require('./chart');

const categoryListTemplate = `
  {{#each categories}}
    <li data-name="{{name}}"><a href="#categories/{{name}}">{{name}}</a></li>
  {{/each}}
`;

const topicListTemplate = `
  <h2>All together {{topicCount}} topics</h2>
  {{topics}}
  {{#if more}}
    ... <button class="btn btn-xs btn-default" id="show-all-topics">Show all</button>
  {{/if}}
`

const Renderer = {
  categoryList(options){
    options.target.html(Handlebars.compile(categoryListTemplate)({ categories: options.categories }));
  },
  topicList(options){
    let topics = options.topics.join(', ');
    options.target.html(Handlebars.compile(topicListTemplate)({ more: options.more, topics, topicCount: options.topicCount }));
  },
  topicChart(options){
    Chart({ target: options.target, data: options.data, width: 1000, height: 500 });
  }
}

module.exports = Renderer;
