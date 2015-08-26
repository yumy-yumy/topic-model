var $ = require('jquery');
var _ = require('lodash');

require('jquery-ui/slider');

var renderDiagram = require('./diagram');
var renderClasses = require('./classes');
var renderTree = require('./tree');

var Router = require('prouter').Router;
var Api = require('./api');

const DEFAULT_YEAR_RANGE = { from: 1993, to: 2006 };

function generateLabels(range){
  return _.range(range.from, range.to + 1);
}

function initTopicDiagram(){
  if($('#chart').find('svg').length == 0){
    Api.getTopicsForYears(DEFAULT_YEAR_RANGE)
      .done(function(data){
        renderDiagram({
          data: JSON.parse(data),
          target: document.getElementById('chart'),
          timelineTarget: document.getElementById('chart-timeline'),
          labels: generateLabels(DEFAULT_YEAR_RANGE),
          height: $(window).height() - 110
        });
      });
  }
}

function updateTopicDiagram(range){
  Api.getTopicsForYears(range)
    .done(function(data){
      renderDiagram({
        data: JSON.parse(data),
        target: document.getElementById('chart'),
        timelineTarget: document.getElementById('chart-timeline'),
        labels: generateLabels(range),
        height: $(window).height() - 110
      });
    });
}

function initClasses(year, selectedClass){
  Api.getClasses()
    .done(function(data){
      renderClasses({
        target: document.getElementById('class-list'),
        classes: JSON.parse(data).classes,
        year,
        selectedClass
      });
    });
}

function initTopicTree(year){
  var $container = $('#topic-tree-container');
  $container.addClass('show');
  $container.find('h1').html(`Topics in year ${year}`);
  $container.find('#class-chart-timeline').hide();

  Api.getTopicsForYear({ year })
    .done(function(data){
      var tree = JSON.parse(data);

      tree.name = `Topics in year ${year}`;

      renderTree({
        target: document.getElementById('tree-canvas'),
        data: tree,
        height: $(window).height() - 60
      });

      initClasses(year, null);
    });
}

function initClassDiagram(year, className){
  var $container = $('#topic-tree-container');
  $container.addClass('show');
  $container.find('#class-container-toggle i').removeClass('fa-chevron-left').addClass('fa-chevron-right');
  $container.find('h1').html(`Topics of class "${className}"`);
  $container.find('#class-chart-timeline').show();

  Api.getTopicsForClass({ className })
    .done(function(data){
      var decoded = JSON.parse(data);

      renderDiagram({
        data: decoded.topics,
        target: document.getElementById('tree-canvas'),
        timelineTarget: document.getElementById('class-chart-timeline'),
        labels: decoded.years,
        height: $(window).height() - 110
      });
    });


  /*Api.getTopicsForYears(DEFAULT_YEAR_RANGE)
    .done(function(data){
      renderDiagram({
        data: JSON.parse(data),
        target: document.getElementById('tree-canvas'),
        timelineTarget: document.getElementById('class-chart-timeline'),
        labels: generateLabels({ from: 1993, to: 2006 }),
        height: $(window).height() - 110
      });
    });*/

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
  $('#settings-years-title').html(`Show me topics between ${DEFAULT_YEAR_RANGE.from} and ${DEFAULT_YEAR_RANGE.to}.`);

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
    max: 2015,
    step: 1,
    values: [DEFAULT_YEAR_RANGE.from, DEFAULT_YEAR_RANGE.to],
    slide: function(event, ui){
      var start = ui.values[0];
      var end = ui.values[1];

      if(end - start < 4){
        return false;
      }

      $('#settings-years-title').html(`Show me topics between ${start} and ${end}.`);
    },
    stop: function(event, ui){
      updateTopicDiagram({ from: ui.values[0], to: ui.values[1] });
    }
  });
});
