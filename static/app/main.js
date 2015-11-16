var $ = require('jquery');
var _ = require('lodash');

require('jquery-ui/slider');

var renderDiagram = require('./diagram');
var renderClasses = require('./classes');
var renderTree = require('./tree');

var Api = require('./api');

const DEFAULT_YEAR_RANGE = { from: 1993, to: 2006 };
const PULP_URL = 'http://localhost:8000/search';

var chosenKeywords = [];
var chosenYearRange = Object.assign({}, DEFAULT_YEAR_RANGE);

const $loadingContainer = $('#loading-container');

function clickTopicInSankey(text, chosen){
  if (chosen) {
    chosenKeywords.push(text)
  } else {
    var removedIndex = 0;
    chosenKeywords.forEach(function(keyword, i){
      if(keyword == text){
        removedIndex = i;
      }
    });

    chosenKeywords.splice(removedIndex, 1);
  }
}

function generateLabels(range){
  return _.range(range.from, range.to + 1);
}

function initTopicDiagram(){
  $loadingContainer.addClass('show');

  Api.getTopicsForYears(DEFAULT_YEAR_RANGE)
    .done(function(data){
      renderDiagram({
        data: JSON.parse(data),
        target: document.getElementById('chart'),
        timelineTarget: document.getElementById('chart-timeline'),
        labels: generateLabels(DEFAULT_YEAR_RANGE),
        height: $(window).height() - 110,
        nodeOnClick: clickTopicInSankey
      });

      $loadingContainer.removeClass('show');
    });
}

function updateTopicDiagram(range){
  Api.getTopicsForYears(range)
    .done(function(data){
      renderDiagram({
        data: JSON.parse(data),
        target: document.getElementById('chart'),
        timelineTarget: document.getElementById('chart-timeline'),
        labels: generateLabels(range),
        height: $(window).height() - 110,
        nodeOnClick: clickTopicInSankey
      });
    });
}

function initClasses(selectedClass){
  Api.getClasses()
    .done(function(data){
      renderClasses({
        target: document.getElementById('class-list'),
        classes: JSON.parse(data).classes,
        selectedClass
      });
    });
}

function initTopicTree(year){
  var $container = $('#topic-tree-container');
  $container.addClass('show');
  var $heading = $container.find('h1')
  $heading.html(`Topics in year ${year}`);

  Api.getTopicsForYear({ year })
    .done(function(data){
      var tree = JSON.parse(data);

      tree.name = `${year}`;

      renderTree({
        target: document.getElementById('tree-canvas'),
        data: tree,
        height: $(window).height() - 60
      });

      initClasses(null);
    });
}

function initClassDiagram(className){
  $loadingContainer.addClass('show');

  Api.getTopicsForClass({ className })
    .done(function(data){
      var decoded = JSON.parse(data);

      renderDiagram({
        data: decoded.topics,
        target: document.getElementById('chart'),
        timelineTarget: document.getElementById('chart-timeline'),
        labels: decoded.years,
        height: $(window).height() - 110
      });

      $loadingContainer.removeClass('show');
    });
}

var states = {
  'TOPIC_DIAGRAM': function(){
    $('.background-layer').removeClass('show');
    $('#visualization-settings-toggle').addClass('bring-right');
    $('#back-to-topic-diagram').removeClass('bring-right');

    initClasses(null);
    initTopicDiagram();
  },
  'CLASS_DIAGRAM': function(className){
    $('#visualization-settings-toggle').removeClass('bring-right');
    $('#back-to-topic-diagram').addClass('bring-right');
    $('#class-container').addClass('bring-left');

    initClasses(className);
    initClassDiagram(className);
  },
  'YEAR_DIAGRAM': function(year){
    initTopicTree(year);
  }
}

$(function(){
  states['TOPIC_DIAGRAM']();

  $('body')
    .on('click', '.class-trigger', function(e){
      e.preventDefault();
      states['CLASS_DIAGRAM']($(this).data('name'));
    })
    .on('click', '.year-trigger', function(e){
      e.preventDefault();
      states['YEAR_DIAGRAM']($(this).data('year'));
    });

  $('#to-pulp-trigger').on('click', function(){
    var query = _.uniq(_.uniq(chosenKeywords).join(' ').split(' ')).join(' ').replace(/\s/g, '+');
    console.log(query)
    console.log(chosenKeywords);
    var year_from = chosenYearRange.from;
    var year_to = chosenYearRange.to;

    window.open(`${PULP_URL}#/?query=${query}&year_from=${year_from}&year_to=${year_to}`, '_blank');
  });

  $('#back-to-topic-diagram').on('click', function(){
    states['TOPIC_DIAGRAM']();
  });

  $('.background-layer .close-button').on('click', function(e){
    e.preventDefault();
    $(this).parent('.background-layer').removeClass('show');
  });

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

      chosenYearRange = Object.assign(chosenYearRange, { from: start, to: end });

      $('#settings-years-title').html(`Show me topics between ${start} and ${end}.`);
    },
    stop: function(event, ui){
      updateTopicDiagram({ from: ui.values[0], to: ui.values[1] });
    }
  });
});
