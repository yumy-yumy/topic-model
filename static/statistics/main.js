var $ = require('jquery');
var _ = require('lodash');
var Router = require('prouter').Router;
var Api = require('./api');
var Renderer = require('./renderer');

const $categoryLinks = $('#category-links');
const $categoryTitle = $('#category-title');
const $topicList = $('#category-topic-list');
const $topicChart = $('#topic-chart');

Router.use('/categories/:category', function (req) {
  $categoryTitle.html(`Topics from category "${req.params.category}"`);
  $categoryLinks
    .find('li').removeClass('active');
  $categoryLinks
    .find(`li[data-name="${req.params.category}"]`)
    .addClass('active');

  Api.getTopicsFromCategory(req.params.category)
    .done((data) => {
      let topics =
      data
        .reduce((allTopics, year) => {
          return allTopics.concat(year.topics);
        }, [])
        .map(topic => topic.title);

      topics = _.unique(topics);

      Renderer.topicList({ target: $topicList, topics: topics.slice(0, 20), more: topics.length > 20, topicCount: topics.length });
      Renderer.topicChart({ target: $topicChart, data: data });

      $('#show-all-topics')
        .on('click', function(){
          Renderer.topicList({ target: $topicList, topics: topics, more: false, topicCount: topics.length });
        });
    });
});

Router.listen({
  root: '/',
  usePushState: false,
  hashChange: true,
  silent: false
});

Api.getAllCategories()
  .done((data) => {
    let categories = JSON.parse(data).classes.map(c => { return { name: c } });

    Renderer.categoryList({ target: $categoryLinks, categories });

    Router.navigate(`categories/${categories[0].name}`);
  });
