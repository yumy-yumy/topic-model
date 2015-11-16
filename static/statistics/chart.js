import Raphael from 'raphael';
import _ from 'lodash';

const Chart = (options) => {

  const showTooltip = (title, event) => {
    let tooltip =  document.getElementById('topic-tooltip');
    tooltip.innerHTML = title;
    tooltip.style.left = ( event.clientX + 10 ) + 'px';
    tooltip.style.top = ( event.clientY + 10 ) + 'px';
    tooltip.style.display = 'initial';
  }

  const hideTooltip = () => {
    let tooltip =  document.getElementById('topic-tooltip');
    tooltip.style.display = 'none';
  }

  const darkenColor = (color, percent) => {
    var num = parseInt(color.slice(1),16), amt = Math.round(2.55 * percent), R = (num >> 16) + amt, G = (num >> 8 & 0x00FF) + amt, B = (num & 0x0000FF) + amt;
    return "#" + (0x1000000 + (R<255?R<1?0:R:255)*0x10000 + (G<255?G<1?0:G:255)*0x100 + (B<255?B<1?0:B:255)).toString(16).slice(1);
  }

  const generateColor = () => {
    var r = (Math.round(Math.random()* 127) + 127).toString(16);
    var g = (Math.round(Math.random()* 127) + 127).toString(16);
    var b = (Math.round(Math.random()* 127) + 127).toString(16);
    var color = '#' + r + g + b;

    return color;
  }

  var colorUsage = {};
  var topicsToColor = {}

  const nextColor = () => {
    var color = generateColor();

    while(colorUsage[color]){
      color = generateColor();
    }

    colorUsage[color] = true;

    return color;
  }

  var target = options.target;
  var width = options.width;
  var height = options.height;

  var data = options.data;

  target.innerHTML='';

  const raphael = Raphael(target, width, height);
  const textColor = '#777';
  const lineColor = '#DDD';
  const barWidth = 20;

  const render = () => {
    var labelWidth = width / data.length;
    var dummyLabel = raphael.text(0, 0, data[0].year)
    var textWidth = dummyLabel.getBBox().width;
    dummyLabel.remove();

    var topicBartStartY = height - 30;
    var maxHeight = height - 34;
    var labelY = height - 15;

    var scaleHeight = (height - 35) / 10;

    for(let y = labelY - 15; y >= 0; y -= scaleHeight){
      raphael.path(`M 0 ${y}L${width} ${y}`).attr({ stroke: lineColor });
    }

    for(let i = 0; i < data.length; i++){
      var year = data[i];

      var labelX = textWidth / 2 + labelWidth * i;
      raphael.path(`M ${labelX} ${labelY - 10}L${labelX} 0`).attr({ stroke: lineColor });
      raphael.text(labelX, labelY, year.year).attr({ fill: textColor })
      .mousemove(function(event){
        var pluralized = data[i].doc == 1 ? 'document' : 'documents';
        showTooltip(`${data[i].doc} ${pluralized} from this year`, event);
      })
      .mouseout(function(){
        hideTooltip();
      });

      var yPointer = topicBartStartY;

      year.topics.forEach(topic => {
        var barHeight = topic.weight * maxHeight;
        var barX = labelX - barWidth / 2;

        var bgColor;

        if(!topicsToColor[topic.title.join(', ')]){
          bgColor = nextColor();
        }else{
          bgColor = topicsToColor[topic.title.join(', ')];
        }

        var bar = raphael.rect(barX, yPointer - barHeight, barWidth, barHeight).attr({ fill: bgColor, 'stroke-width': 0 });
        bar
          .mousemove(function(event){
            showTooltip(`${topic.title.join(', ')} (${Math.round(topic.weight * 100)}%)`, event);
            bar.attr('fill', darkenColor(bgColor, -10));
          })
          .mouseout(function(){
            hideTooltip();
            bar.attr('fill', bgColor);
          });

        yPointer -= barHeight;
      });
    }

  }

  render();
}

export default Chart;
