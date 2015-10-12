import React from 'react';
import Chart from '../chart';

var TopicChart = React.createClass({
  propTypes(){
    return {
      years: React.propTypes.array.isRequired
    }
  },

  componentDidUpdate(){
    this._createChart();
  },

  componentDidMount(){
    this._createChart();
  },

  render(){
    return <div ref="canvas"></div>;
  },

  _createChart(){
    if(this.props.years.length > 0){
      let node = React.findDOMNode(this.refs.canvas);
      Chart({ target: node, data: this.props.years, width: 1000, height: 500 });
    }
  }
});

export default TopicChart;
