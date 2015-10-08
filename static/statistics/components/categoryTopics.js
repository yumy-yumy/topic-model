import React from 'react';
import _ from 'lodash';

var CategoryTopics = React.createClass({
  getInitialState(){
    return {
      showAll: false
    }
  },

  propTypes(){
    return {
      topics: React.propTypes.array.isRequired
    }
  },

  componentWillReceiveProps(){
    this.setState({ showAll: false });
  },

  render(){
    let topicsShowing = this.state.showAll ? this.props.topics : _.take(this.props.topics, 80);

    let topicList = topicsShowing.map(topic => {
      return (
        <span className="label label-default" style={{ display: 'inline-block', marginRight: '4px' }}>{topic.join(', ')}</span>
      );
    });

    let ellipsis;
    let more;

    if(topicsShowing.length < this.props.topics.length){
      more = this.props.topics.length - topicsShowing.length;
      ellipsis = (
        <button className="btn btn-default btn-xs" onClick={this._showAll}>Show {more} more</button>
      )
    }

    return (
      <div>
        <h2>All topics ({this.props.topics.length})</h2>
        {topicList}
        {ellipsis}
      </div>
    );
  },

  _showAll(){
    this.setState({ showAll: true });
  }
});

export default CategoryTopics;
