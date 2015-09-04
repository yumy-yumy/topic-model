var $ = require('jquery');
var _ = require('lodash');
var d3 = require('../../node_modules/d3/d3.min');
var sankeySetup = require('./sankey');
var renderTimeline = require('./timeline');

sankeySetup(d3);

module.exports = (options) => {
  options.target.innerHTML = '';

  var widthForItem = 480;

  var margin = {top: 1, right: 1, bottom: 6, left: 1},
      width = (widthForItem * (options.labels.length - 1)) - margin.left - margin.right,
      height = options.height - margin.top - margin.bottom;

  $(options.target).css('height', options.height);

  renderTimeline({
    target: options.timelineTarget,
    labels: options.labels,
    width: widthForItem * ( options.labels.length - 1 ) + 100,
    itemWidth: widthForItem - 2,
    events: options.events
  });

  var formatNumber = d3.format(",.0f"),
      format = function(d) { return formatNumber(d) + " TWh"; },
      color = d3.scale.category20();

  var sankey = d3.sankey()
      .nodeWidth(15)
      .nodePadding(10)
      .size([width, height]);

  var path = sankey.link();

  var svg = d3.select(options.target).append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
    .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  sankey
      .nodes(options.data.nodes)
      .links(options.data.links)
      .layout(32);

  var link = svg.append("g").selectAll(".link")
      .data(options.data.links)
    .enter().append("path")
      .attr("class", "link")
      .attr("data-id", function(l){
        l.id = _.uniqueId();
        return l.id;
      })
      .attr("d", path)
      .style("stroke-width", function(d) { return Math.max(1, d.dy); })
      .sort(function(a, b) { return b.dy - a.dy; });

  link.append("title")
      .text(function(d) { return d.source.name + " → " + d.target.name + "\n" + format(d.value); });

  var node = svg.append("g").selectAll(".node")
      .data(options.data.nodes)
    .enter().append("g")
      .attr("class", function(d){
        var classes = "node";

        if(d.targetLinks.length == 0 || _.where(d.targetLinks, { source: { name: '' } }).length > 0){
          classes += " new";
        }

        return classes;
      })
      .attr("transform", function(d) {
        return "translate(" + d.x + "," + d.y + ")";
      })
    .call(d3.behavior.drag()
      .origin(function(d) { return d; })
      .on("dragstart", function() { this.parentNode.appendChild(this); })
      .on("drag", dragmove));

  node.append("rect")
      .attr("height", function(d) { return d.dy; })
      .attr("width", sankey.nodeWidth())
      .style("fill", function(d) { return d.color = color(d.name.replace(/ .*/, "")); })
      .style("stroke", function(d) { return d3.rgb(d.color).darker(2); })
    .append("title")
      .text(function(d) { return d.name + "\n" + format(d.value); });

  $('.new rect').each(function(){
    var $elem = $(this);
    $elem.css('filter', 'drop-shadow(0px 0px 5px ' + $elem.css('fill') + ')');
  });

  function highlightPath(node){
    if(!node){
      return;
    }

    node.sourceLinks.forEach(function(l){
      var $linkElems = $('path[data-id=' + l.id + ']');

      $linkElems.css({
        'stroke': node.color,
        'stroke-opacity': '1'
      });

      highlightPath(l.target)
    });
  }

  node
    .on('mouseover', function(d){
      highlightPath(d);
    })
    .on('mouseout', function(d){
      $(options.target).find('path').css({
        'stroke': 'white',
        'stroke-opacity': '0.2'
      });
    });

  node.append("text")
      .attr("x", -6)
      .attr("y", function(d) { return d.dy / 2; })
      .attr("dy", ".35em")
      .attr("text-anchor", "end")
      .attr("transform", null)
      .text(function(d) { return d.name; })
    .filter(function(d) { return d.x < width / 2; })
      .attr("x", 6 + sankey.nodeWidth())
      .attr("text-anchor", "start");

  function dragmove(d) {
    d3.select(this).attr("transform", "translate(" + d.x + "," + (d.y = Math.max(0, Math.min(height - d.dy, d3.event.y))) + ")");
    sankey.relayout();
    link.attr("d", path);
  }
}
