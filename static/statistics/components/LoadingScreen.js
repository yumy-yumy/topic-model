import React from 'react';

var LoadingScreen = React.createClass({
  propTypes(){
    return {
      loading: React.propTypes.boolean.isRequired
    }
  },

  render(){
    let classes = this.props.loading ? 'loading' : ''

    return (
      <div id="loading-container" className={classes}>
        <div id="loading-text">
          Loading<span className="one">.</span><span className="two">.</span><span className="three">.</span>
        </div>
      </div>
    )
  }
});

export default LoadingScreen;
