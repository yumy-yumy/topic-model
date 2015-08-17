var $ = require('jquery');

require('jquery-ui/slider');

var renderDiagram = require('./diagram');
var renderClasses = require('./classes');
var renderTree = require('./tree');

var Router = require('prouter').Router;
var Api = require('./api');

function initTopicDiagram(){
  Api.getTopicsForYears({ from: 1990, to: 2000 })
    .done(function(data){
      console.log(data);
    });

  if($('#chart').find('svg').length == 0){
    renderDiagram({
      data: 'static/data/1993_2002.json',
      target: document.getElementById('chart'),
      timelineTarget: document.getElementById('chart-timeline'),
      labels: ['1993', '1994', '1995', '1996', '1997', '1998', '1999', '2000', '2001', '2002']
    });
  }
}

function initClasses(year, selectedClass){
  renderClasses({
    target: document.getElementById('class-list'),
    classes: ['Class A', 'Class B', 'Class C', 'Class D', 'Class E'],
    year: year,
    selectedClass: selectedClass
  });
}

function initTopicTree(year){
  var $container = $('#topic-tree-container');
  $container.addClass('show');
  $container.find('h1').html(`Topics in year ${year}`);

  renderTree({
    target: document.getElementById('tree-canvas')
  });

  initClasses(year, null);
}

function initClassDiagram(year, className){
  var $container = $('#topic-tree-container');
  $container.addClass('show');
  $container.find('#class-container-toggle i').removeClass('fa-chevron-left').addClass('fa-chevron-right');
  $container.find('h1').html(`Topics of class "${className}"`);

  renderDiagram({
    data: 'data/1993_2002.json',
    target: document.getElementById('tree-canvas'),
    timelineTarget: document.getElementById('chart-timeline'),
    labels: ['1993', '1994', '1995', '1996', '1997', '1998', '1999', '2000', '2001', '2002']
  });

  initClasses(year, className);
}

Router
  .use('/', function(req) {
    $('.background-layer').removeClass('show');

    initTopicDiagram();
  })
  .use('/topics/:year', function(req){
    initTopicDiagram();
    initTopicTree(req.params.year);
  })
  .use('/topics/:year/classes/:className', function(req){
    initTopicDiagram();
    initClassDiagram(req.params.year, req.params.className);

    $('#class-container').addClass('bring-left');
  })
  .use(function(req){
    $('.background-layer').removeClass('show');

    initTopicDiagram();
  });

Router.listen({
  root: '/',
  usePushState: false,
  hashChange: true,
  silent: false
});

$(function(){
  $('#visualization-settings-toggle').on('click', function(){
    $(this).toggleClass('active');
    $('#visualization-settings-container').toggleClass('show');
  });

  $('#class-container-toggle').on('click', function(){
    var $icon = $(this).find('i.fa');

    $icon.hasClass('fa-chevron-left') ? $icon.removeClass('fa-chevron-left').addClass('fa-chevron-right') : $icon.removeClass('fa-chevron-right').addClass('fa-chevron-left')

    $('#class-container').toggleClass('bring-left');
  });

  $('#settings-years-slider').slider({
    range: true,
    min: 1993,
    max: 2002,
    step: 1,
    values: [1993, 2002],
    slide: function(event, ui){
      var start = ui.values[0];
      var end = ui.values[1];

      if(end - start < 2){
        return false;
      }

      $('#settings-years-title').html(`Show me topics between ${start} and ${end}.`);
    }
  });
});
