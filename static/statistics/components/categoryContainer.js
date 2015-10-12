import React from 'react';
import _ from 'lodash';
import CategoryTopics from './categoryTopics';
import TopicChart from './topicChart';

var CategoryContainer = React.createClass({
  propTypes(){
    return {
      category: React.propTypes.string,
      years: React.propTypes.array
    }
  },

  render(){
    let topics =
    this.props.years
      .reduce((allTopics, year) => {
        return allTopics.concat(year.topics);
      }, [])
      .map(topic => topic.title);

    topics = _.unique(topics);

    let content;

    if(this.props.category && !this.props.loading){
      content = (
        <div>
          <h1>Topics from category <i>{this.props.category}</i></h1>

          <h2>Frequency of topics each year</h2>

          <TopicChart years={this.props.years} />

          <hr/>

          <CategoryTopics topics={topics} />
        </div>
      );
    }else{
      content = (
        <h1 className="text-muted">Please, choose a category.</h1>
      )
    }

    return (
      <div id="category-chart">
        {content}
      </div>
    );
  }
});

export default CategoryContainer;
